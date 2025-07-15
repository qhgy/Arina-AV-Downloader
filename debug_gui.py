#!/usr/bin/env python3
"""
Debug GUI - Shows exactly what's happening during download
"""

import sys
import os
from pathlib import Path
import threading
import time

try:
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
    PYQT_AVAILABLE = True
except ImportError:
    try:
        from PySide6.QtWidgets import *
        from PySide6.QtCore import *
        from PySide6.QtGui import *
        PYQT_AVAILABLE = True
    except ImportError:
        PYQT_AVAILABLE = False

class DebugDownloadGUI(QMainWindow):
    """Debug GUI to test download functionality"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Debug Download Test")
        self.setFixedSize(800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("Debug Download Test")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # URL input (pre-filled with test URL)
        self.url_input = QLineEdit()
        self.url_input.setText("https://cn.pornhub.com/view_video.php?viewkey=68543d832ddd2")
        self.url_input.setStyleSheet("padding: 8px; font-size: 12px;")
        layout.addWidget(QLabel("Test URL:"))
        layout.addWidget(self.url_input)
        
        # Downloader type selection
        downloader_layout = QHBoxLayout()
        self.downloader_group = QButtonGroup()
        
        self.simple_radio = QRadioButton("Simple Downloader")
        self.simple_radio.setChecked(True)
        self.advanced_radio = QRadioButton("Advanced Downloader")
        
        self.downloader_group.addButton(self.simple_radio, 0)
        self.downloader_group.addButton(self.advanced_radio, 1)
        
        downloader_layout.addWidget(self.simple_radio)
        downloader_layout.addWidget(self.advanced_radio)
        layout.addLayout(downloader_layout)
        
        # Test buttons
        button_layout = QHBoxLayout()
        
        self.info_btn = QPushButton("Test Info")
        self.info_btn.clicked.connect(self.test_info)
        self.info_btn.setStyleSheet("padding: 10px; background: #3498db; color: white; border: none; border-radius: 5px;")
        
        self.download_btn = QPushButton("Test Download")
        self.download_btn.clicked.connect(self.test_download)
        self.download_btn.setStyleSheet("padding: 10px; background: #27ae60; color: white; border: none; border-radius: 5px;")
        
        self.clear_btn = QPushButton("Clear Log")
        self.clear_btn.clicked.connect(self.clear_log)
        self.clear_btn.setStyleSheet("padding: 10px; background: #e74c3c; color: white; border: none; border-radius: 5px;")
        
        button_layout.addWidget(self.info_btn)
        button_layout.addWidget(self.download_btn)
        button_layout.addWidget(self.clear_btn)
        layout.addLayout(button_layout)
        
        # Debug log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("background: #2c3e50; color: #ecf0f1; font-family: 'Consolas', monospace; font-size: 10px;")
        layout.addWidget(QLabel("Debug Log:"))
        layout.addWidget(self.log_area)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status
        self.statusBar().showMessage("Ready for testing")
        
        self.log("Debug GUI initialized")
        self.log("Testing URL: https://cn.pornhub.com/view_video.php?viewkey=68543d832ddd2")
        self.log("Select downloader type and click 'Test Info' to start")
    
    def log(self, message):
        """Add timestamped message to log"""
        timestamp = QTime.currentTime().toString("hh:mm:ss")
        self.log_area.append(f"[{timestamp}] {message}")
        self.log_area.verticalScrollBar().setValue(self.log_area.verticalScrollBar().maximum())
        QApplication.processEvents()
    
    def clear_log(self):
        """Clear the log area"""
        self.log_area.clear()
        self.log("Log cleared")
    
    def test_info(self):
        """Test video info extraction"""
        url = self.url_input.text().strip()
        if not url:
            self.log("ERROR: No URL provided")
            return
        
        self.log(f"=== Testing Info Extraction ===")
        self.log(f"URL: {url}")
        
        downloader_type = "simple" if self.simple_radio.isChecked() else "advanced"
        self.log(f"Downloader type: {downloader_type}")
        
        self.info_btn.setEnabled(False)
        self.statusBar().showMessage("Testing info extraction...")
        
        # Run in background thread
        threading.Thread(target=self._info_worker, args=(url, downloader_type), daemon=True).start()
    
    def _info_worker(self, url: str, downloader_type: str):
        """Background worker for info extraction"""
        try:
            self.log("Initializing downloader...")
            
            if downloader_type == "simple":
                from simple_fallback import SimpleYtDlpDownloader
                downloader = SimpleYtDlpDownloader()
                if not downloader.available:
                    raise Exception("yt-dlp not available")
                
                self.log("Using SimpleYtDlpDownloader")
                self.log("Extracting video info...")
                info = downloader.get_video_info(url)
                
            else:
                try:
                    from speed_optimizer import HighSpeedDownloader
                    downloader = HighSpeedDownloader(speed_profile='balanced', max_workers=4)
                    self.log("Using HighSpeedDownloader")
                    self.log("Extracting video info...")
                    info = downloader.extractor.extract_info(url)
                except ImportError:
                    self.log("Advanced downloader not available, falling back to simple")
                    from simple_fallback import SimpleYtDlpDownloader
                    downloader = SimpleYtDlpDownloader()
                    info = downloader.get_video_info(url)
            
            # Format results
            title = info.get('title', 'Unknown')
            uploader = info.get('uploader', 'Unknown')
            duration = info.get('duration', 0)
            view_count = info.get('view_count', 0)
            
            duration_str = "Unknown"
            if duration:
                minutes, seconds = divmod(duration, 60)
                duration_str = f"{minutes:02d}:{seconds:02d}"
            
            self.log("=== INFO EXTRACTION SUCCESS ===")
            self.log(f"Title: {title}")
            self.log(f"Uploader: {uploader}")
            self.log(f"Duration: {duration_str}")
            self.log(f"Views: {view_count:,}" if view_count else "Views: Unknown")
            self.log(f"Available formats: {len(info.get('formats', []))}")
            
            # Update UI in main thread
            QTimer.singleShot(0, lambda: self._info_completed(True, "Info extraction successful!"))
            
        except Exception as e:
            error_msg = str(e)
            self.log(f"=== INFO EXTRACTION FAILED ===")
            self.log(f"Error: {error_msg}")
            
            # Update UI in main thread
            QTimer.singleShot(0, lambda: self._info_completed(False, error_msg))
    
    def _info_completed(self, success: bool, message: str):
        """Handle info completion in main thread"""
        self.info_btn.setEnabled(True)
        if success:
            self.statusBar().showMessage("Info extraction successful")
            self.download_btn.setEnabled(True)
        else:
            self.statusBar().showMessage("Info extraction failed")
    
    def test_download(self):
        """Test actual download"""
        url = self.url_input.text().strip()
        if not url:
            self.log("ERROR: No URL provided")
            return
        
        self.log(f"=== Testing Download ===")
        self.log(f"URL: {url}")
        
        downloader_type = "simple" if self.simple_radio.isChecked() else "advanced"
        self.log(f"Downloader type: {downloader_type}")
        
        self.download_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.statusBar().showMessage("Testing download...")
        
        # Run in background thread
        threading.Thread(target=self._download_worker, args=(url, downloader_type), daemon=True).start()
    
    def _download_worker(self, url: str, downloader_type: str):
        """Background worker for download"""
        try:
            self.log("Initializing downloader for download...")
            
            # Create downloads directory
            downloads_dir = Path("./debug_downloads")
            downloads_dir.mkdir(exist_ok=True)
            self.log(f"Downloads directory: {downloads_dir}")
            
            if downloader_type == "simple":
                from simple_fallback import SimpleYtDlpDownloader
                downloader = SimpleYtDlpDownloader()
                if not downloader.available:
                    raise Exception("yt-dlp not available")
                
                self.log("Using SimpleYtDlpDownloader for download")
                
                def progress_callback(progress, speed):
                    speed_mb = speed / 1024 / 1024 if speed > 0 else 0
                    QTimer.singleShot(0, lambda: self._update_progress(progress, speed_mb))
                
                self.log("Starting download with simple downloader...")
                success = downloader.download(url, str(downloads_dir), audio_only=False, progress_callback=progress_callback)
                
            else:
                try:
                    from speed_optimizer import HighSpeedDownloader
                    downloader = HighSpeedDownloader(speed_profile='balanced', max_workers=4)
                    self.log("Using HighSpeedDownloader for download")
                    
                    # Add progress callback
                    def progress_cb(task_id, progress, speed):
                        speed_mb = speed / 1024 / 1024 if speed > 0 else 0
                        QTimer.singleShot(0, lambda: self._update_progress(progress, speed_mb))
                    
                    downloader.add_progress_callback(progress_cb)
                    
                    self.log("Adding download task...")
                    task_id = downloader.add_task(url, str(downloads_dir), audio_only=False)
                    
                    self.log("Starting download with advanced downloader...")
                    future = downloader.start_download(task_id)
                    success = future.result()
                    
                except ImportError:
                    self.log("Advanced downloader not available, falling back to simple")
                    from simple_fallback import SimpleYtDlpDownloader
                    downloader = SimpleYtDlpDownloader()
                    
                    def progress_callback(progress, speed):
                        speed_mb = speed / 1024 / 1024 if speed > 0 else 0
                        QTimer.singleShot(0, lambda: self._update_progress(progress, speed_mb))
                    
                    success = downloader.download(url, str(downloads_dir), audio_only=False, progress_callback=progress_callback)
            
            if success:
                self.log("=== DOWNLOAD SUCCESS ===")
                self.log("Download completed successfully!")
                
                # List downloaded files
                files = list(downloads_dir.glob("*"))
                if files:
                    self.log("Downloaded files:")
                    for file in files:
                        self.log(f"  - {file.name}")
                
                QTimer.singleShot(0, lambda: self._download_completed(True, "Download successful!"))
            else:
                self.log("=== DOWNLOAD FAILED ===")
                self.log("Download returned False")
                QTimer.singleShot(0, lambda: self._download_completed(False, "Download failed"))
                
        except Exception as e:
            error_msg = str(e)
            self.log(f"=== DOWNLOAD EXCEPTION ===")
            self.log(f"Error: {error_msg}")
            
            import traceback
            self.log("Full traceback:")
            for line in traceback.format_exc().split('\n'):
                if line.strip():
                    self.log(f"  {line}")
            
            QTimer.singleShot(0, lambda: self._download_completed(False, error_msg))
    
    def _update_progress(self, progress: float, speed_mb: float):
        """Update progress in main thread"""
        self.progress_bar.setValue(int(progress))
        self.log(f"Progress: {progress:.1f}% | Speed: {speed_mb:.1f} MB/s")
    
    def _download_completed(self, success: bool, message: str):
        """Handle download completion in main thread"""
        self.download_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            self.statusBar().showMessage("Download completed successfully")
            QMessageBox.information(self, "Success", "Download completed successfully!\n\nCheck the debug_downloads folder.")
        else:
            self.statusBar().showMessage("Download failed")
            QMessageBox.warning(self, "Error", f"Download failed:\n\n{message}")

def main():
    if not PYQT_AVAILABLE:
        print("PyQt6/PySide6 not available. Please install.")
        return
    
    app = QApplication(sys.argv)
    window = DebugDownloadGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()