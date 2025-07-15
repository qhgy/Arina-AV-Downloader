#!/usr/bin/env python3
"""
Simple GUI Test with Pre-filled PornHub URL
"""

import sys
import os
from pathlib import Path

# Add PyQt6 compatibility check
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

class SimpleDownloadTest(QMainWindow):
    """Simple test window with pre-filled URL"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PornHub Download Test")
        self.setFixedSize(600, 400)
        
        # Center widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("PornHub Download Test")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # URL input (pre-filled)
        self.url_input = QLineEdit()
        self.url_input.setText("https://cn.pornhub.com/view_video.php?viewkey=68543d832ddd2")
        self.url_input.setStyleSheet("padding: 8px; font-size: 12px;")
        layout.addWidget(QLabel("Test URL:"))
        layout.addWidget(self.url_input)
        
        # Test buttons
        button_layout = QHBoxLayout()
        
        self.info_btn = QPushButton("Test Info Extraction")
        self.info_btn.clicked.connect(self.test_info)
        self.info_btn.setStyleSheet("padding: 10px; background: #3498db; color: white; border: none; border-radius: 5px;")
        
        self.download_btn = QPushButton("Test Download")
        self.download_btn.clicked.connect(self.test_download)
        self.download_btn.setStyleSheet("padding: 10px; background: #27ae60; color: white; border: none; border-radius: 5px;")
        
        button_layout.addWidget(self.info_btn)
        button_layout.addWidget(self.download_btn)
        layout.addLayout(button_layout)
        
        # Results area
        self.results = QTextEdit()
        self.results.setReadOnly(True)
        self.results.setStyleSheet("background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 8px;")
        layout.addWidget(QLabel("Test Results:"))
        layout.addWidget(self.results)
        
        # Status
        self.statusBar().showMessage("Ready to test")
        
        self.log("GUI initialized. Click 'Test Info Extraction' to start.")
    
    def log(self, message):
        """Add message to results area"""
        self.results.append(f"[{QTime.currentTime().toString()}] {message}")
        QApplication.processEvents()
    
    def test_info(self):
        """Test video info extraction"""
        url = self.url_input.text().strip()
        if not url:
            self.log("❌ No URL provided")
            return
        
        self.log(f"🔍 Testing info extraction for: {url}")
        self.info_btn.setEnabled(False)
        self.statusBar().showMessage("Testing info extraction...")
        
        try:
            import yt_dlp
            self.log(f"✓ yt-dlp version: {yt_dlp.__version__}")
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            
            self.log(f"✓ Title: {info.get('title', 'Unknown')}")
            self.log(f"✓ Duration: {info.get('duration', 0)} seconds")
            self.log(f"✓ Uploader: {info.get('uploader', 'Unknown')}")
            self.log(f"✓ Available formats: {len(info.get('formats', []))}")
            self.log("🎉 Info extraction successful!")
            
            # Enable download button
            self.download_btn.setEnabled(True)
            self.statusBar().showMessage("Info extraction successful")
            
        except Exception as e:
            error_msg = str(e)
            self.log(f"❌ Info extraction failed: {error_msg}")
            
            if "age" in error_msg.lower() or "restricted" in error_msg.lower():
                self.log("⚠️ This appears to be age-restricted content")
                self.log("💡 You may need to import cookies for authentication")
            elif "region" in error_msg.lower() or "geo" in error_msg.lower():
                self.log("⚠️ This appears to be region-restricted")
                self.log("💡 Trying geo-bypass...")
                self.test_geo_bypass(url)
            
            self.statusBar().showMessage("Info extraction failed")
        
        self.info_btn.setEnabled(True)
    
    def test_geo_bypass(self, url):
        """Test with geo-bypass"""
        try:
            import yt_dlp
            ydl_opts = {
                'geo_bypass': True,
                'geo_bypass_country': 'US',
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            
            self.log("✓ Geo-bypass successful!")
            self.log(f"✓ Title: {info.get('title', 'Unknown')}")
            self.download_btn.setEnabled(True)
            
        except Exception as e:
            self.log(f"❌ Geo-bypass also failed: {str(e)}")
    
    def test_download(self):
        """Test actual download"""
        url = self.url_input.text().strip()
        if not url:
            self.log("❌ No URL provided")
            return
        
        self.log(f"📥 Starting test download for: {url}")
        self.download_btn.setEnabled(False)
        self.statusBar().showMessage("Testing download...")
        
        try:
            import yt_dlp
            
            # Create test downloads directory
            downloads_dir = Path("./test_downloads")
            downloads_dir.mkdir(exist_ok=True)
            self.log(f"📁 Downloads directory: {downloads_dir}")
            
            # Use worst quality for faster testing
            ydl_opts = {
                'outtmpl': str(downloads_dir / '%(title)s.%(ext)s'),
                'format': 'worst',  # Fastest download for testing
                'noplaylist': True,
                'geo_bypass': True,  # Enable geo-bypass by default
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.log("🎉 Download completed successfully!")
            
            # List downloaded files
            files = list(downloads_dir.glob("*"))
            if files:
                self.log("📂 Downloaded files:")
                for file in files:
                    self.log(f"   - {file.name}")
            
            self.statusBar().showMessage("Download successful")
            
        except Exception as e:
            self.log(f"❌ Download failed: {str(e)}")
            self.statusBar().showMessage("Download failed")
        
        self.download_btn.setEnabled(True)

def main():
    if not PYQT_AVAILABLE:
        print("PyQt6/PySide6 not available. Installing...")
        os.system("pip install PyQt6")
        try:
            from PyQt6 import QtWidgets, QtCore, QtGui
        except ImportError:
            print("Failed to install PyQt6. Please install manually.")
            return
    
    app = QApplication(sys.argv)
    window = SimpleDownloadTest()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()