#!/usr/bin/env python3
"""
Universal Video Downloader - Modern PyQt6 GUI
Professional desktop interface with material design
"""

import sys
import os
from pathlib import Path
from typing import Optional
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


class AppleButton(QPushButton):
    """Apple风格按钮 - 简洁美观"""
    
    def __init__(self, text: str, primary: bool = False):
        super().__init__(text)
        self.primary = primary
        self.setMinimumHeight(44)  # Apple标准高度
        self.setFont(QFont("SF Pro Display", 15) if primary else QFont("SF Pro Display", 14))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(self._get_style())
    
    def _get_style(self) -> str:
        if self.primary:
            return """
                QPushButton {
                    background: #007AFF;
                    border: none;
                    border-radius: 12px;
                    color: white;
                    font-weight: 600;
                    padding: 12px 24px;
                }
                QPushButton:hover {
                    background: #0056CC;
                }
                QPushButton:pressed {
                    background: #004499;
                    transform: scale(0.98);
                }
                QPushButton:disabled {
                    background: #C7C7CC;
                    color: #8E8E93;
                }
            """
        else:
            return """
                QPushButton {
                    background: rgba(255, 255, 255, 0.8);
                    border: 1px solid rgba(0, 0, 0, 0.1);
                    border-radius: 12px;
                    color: #007AFF;
                    font-weight: 500;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.95);
                    border-color: rgba(0, 122, 255, 0.3);
                }
                QPushButton:pressed {
                    background: rgba(0, 122, 255, 0.1);
                }
                QPushButton:disabled {
                    background: rgba(255, 255, 255, 0.5);
                    color: #8E8E93;
                }
            """


class ProgressCard(QWidget):
    """Modern progress display card"""
    
    def __init__(self):
        super().__init__()
        self.setFixedHeight(120)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.95), stop:1 rgba(255, 255, 255, 0.8));
                border: 2px solid #4682B4;
                border-radius: 12px;
                margin: 4px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # Title
        self.title_label = QLabel("Ready to download")
        self.title_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.title_label.setStyleSheet("color: #2c3e50; margin-bottom: 4px;")
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 6px;
                background-color: #ecf0f1;
                height: 12px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                border-radius: 6px;
            }
        """)
        
        # Status
        self.status_label = QLabel("Waiting for URL...")
        self.status_label.setFont(QFont("Segoe UI", 9))
        self.status_label.setStyleSheet("color: #7f8c8d; margin-top: 4px;")
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)
    
    def update_progress(self, title: str, progress: int, status: str):
        """Update progress display"""
        self.title_label.setText(title)
        self.progress_bar.setValue(progress)
        self.status_label.setText(status)


class PlatformCard(QWidget):
    """Platform selection card"""
    
    def __init__(self, platform: str, icon: str, description: str):
        super().__init__()
        self.platform = platform
        self.setFixedSize(200, 100)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9), stop:1 rgba(255, 255, 255, 0.7));
                border: 2px solid #4682B4;
                border-radius: 12px;
                margin: 4px;
            }
            QWidget:hover {
                border-color: #1e40af;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 1.0), stop:1 rgba(240, 248, 255, 0.9));
            }
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Icon (using text symbols for Windows compatibility)
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("color: #3498db;")
        
        # Platform name
        name_label = QLabel(platform)
        name_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("color: #2c3e50;")
        
        # Description
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Segoe UI", 8))
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #7f8c8d;")
        desc_label.setWordWrap(True)
        
        layout.addWidget(icon_label)
        layout.addWidget(name_label)
        layout.addWidget(desc_label)
    
    def mousePressEvent(self, event):
        """Handle click events"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.parent().parent().parent().show_platform_info(self.platform)


class ModernVideoDownloader(QMainWindow):
    """Modern PyQt6 video downloader interface"""
    
    def __init__(self):
        super().__init__()
        self.downloads = {}
        
        # Initialize downloader - 使用内置的universal_downloader
        try:
            from universal_downloader import DownloadManager
            print("Creating DownloadManager...")
            self.downloader = DownloadManager(max_workers=4)
            print("Adding progress callback...")
            self.downloader.add_progress_callback(self._on_download_progress)
            self.downloader_available = True
            self.downloader_type = "universal"
            print("Universal downloader initialized successfully!")
        except ImportError as e:
            print(f"Universal downloader import error: {e}")
            print("Trying simple fallback downloader...")
            try:
                from simple_fallback import SimpleYtDlpDownloader
                self.downloader = SimpleYtDlpDownloader()
                if hasattr(self.downloader, 'available') and self.downloader.available:
                    self.downloader_available = True
                    self.downloader_type = "simple"
                    print("Simple fallback downloader initialized!")
                else:
                    self.downloader_available = False
                    self.downloader_type = "none"
                    print("No downloader available")
            except Exception as e2:
                print(f"Fallback downloader error: {e2}")
                self.downloader = None
                self.downloader_available = False
                self.downloader_type = "none"
        except Exception as e:
            print(f"Universal downloader initialization error: {e}")
            print("Trying simple fallback downloader...")
            try:
                from simple_fallback import SimpleYtDlpDownloader
                self.downloader = SimpleYtDlpDownloader()
                if hasattr(self.downloader, 'available') and self.downloader.available:
                    self.downloader_available = True
                    self.downloader_type = "simple"
                    print("Simple fallback downloader initialized!")
                else:
                    self.downloader_available = False
                    self.downloader_type = "none"
                    print("No downloader available")
            except Exception as e2:
                print(f"Fallback downloader error: {e2}")
                self.downloader = None
                self.downloader_available = False
                self.downloader_type = "none"
        
        self.init_ui()
        self.center_window()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Universal Video Downloader")
        self.setMinimumSize(600, 500)
        self.setMaximumSize(800, 600)
        
        # Set application icon
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main layout with Apple-style spacing
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(32, 32, 32, 32)
        
        # Header - 简洁标题
        self.create_header(main_layout)
        
        # URL input section - 主要功能区
        self.create_url_input(main_layout)
        
        # Progress section - 进度显示
        self.create_progress_section(main_layout)
        
        # Controls - 操作按钮
        self.create_controls(main_layout)
        
        # Status bar - 简洁状态栏
        self.statusBar().showMessage("Ready")
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                color: #666;
                font-size: 12px;
            }
        """)
        
        # Apply Apple-style global theme
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F5F5F7, stop:1 #FAFAFA);
            }
            QWidget {
                background: transparent;
                font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
            }
            QGroupBox {
                font-weight: 600;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 16px;
                margin-top: 12px;
                padding-top: 12px;
                background: rgba(255, 255, 255, 0.8);
                backdrop-filter: blur(20px);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
                color: #1D1D1F;
                font-size: 17px;
                font-weight: 600;
            }
        """)
    
    def create_header(self, layout):
        """Create header section"""
        header_widget = QWidget()
        header_widget.setStyleSheet("background: transparent;")
        header_layout = QHBoxLayout(header_widget)
        
        # Title
        title = QLabel("Universal Video Downloader")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin: 0;")
        
        # Subtitle
        subtitle = QLabel("Simple • Fast • Clean")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #7f8c8d; margin-left: 16px;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.addStretch()
        
        # Settings and Cookies buttons
        cookies_btn = ModernButton("[Cookie] Cookies")
        cookies_btn.clicked.connect(self.show_cookies)
        header_layout.addWidget(cookies_btn)
        
        settings_btn = ModernButton("[Set] Settings")
        settings_btn.clicked.connect(self.show_settings)
        header_layout.addWidget(settings_btn)
        
        layout.addWidget(header_widget)
    
    def create_url_input(self, layout):
        """Create URL input section"""
        url_group = QGroupBox("Video URL")
        url_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        url_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #4682B4;
                border-radius: 12px;
                margin-top: 8px;
                padding-top: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9), stop:1 rgba(255, 255, 255, 0.7));
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                color: #1e3a8a;
                font-weight: bold;
            }
        """)
        
        url_layout = QVBoxLayout(url_group)
        
        # URL input
        input_layout = QHBoxLayout()
        
        self.url_input = QTextEdit()  # Changed from QLineEdit to QTextEdit for multiple lines
        self.url_input.setPlaceholderText("Paste video URLs here (one per line):\n\nhttps://youtube.com/watch?v=...\nhttps://pornhub.com/view_video.php?viewkey=...\nhttps://twitter.com/user/status/...")
        self.url_input.setMaximumHeight(120)  # Set reasonable height
        self.url_input.setMinimumHeight(60)
        self.url_input.setFont(QFont("Segoe UI", 10))
        self.url_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #4682B4;
                border-radius: 10px;
                padding: 8px 12px;
                background: rgba(255, 255, 255, 0.95);
                line-height: 1.4;
                color: #1e3a8a;
            }
            QTextEdit:focus {
                border-color: #1e40af;
                background: rgba(255, 255, 255, 1.0);
            }
        """)
        self.url_input.textChanged.connect(self.on_url_changed)
        
        button_layout = QVBoxLayout()
        
        self.paste_btn = ModernButton("[Paste]")
        self.paste_btn.clicked.connect(self.paste_url)
        
        self.clear_btn = ModernButton("[Clear]")
        self.clear_btn.clicked.connect(self.clear_urls)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ef4444, stop:1 #dc2626);
                border: none;
                border-radius: 10px;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f87171, stop:1 #ef4444);
            }
            QPushButton:pressed {
                background: #dc2626;
            }
        """)
        
        button_layout.addWidget(self.paste_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        
        input_layout.addWidget(self.url_input)
        input_layout.addLayout(button_layout)
        
        url_layout.addLayout(input_layout)
        layout.addWidget(url_group)
    
    def create_platform_cards(self, layout):
        """Create platform selection cards"""
        platforms_group = QGroupBox("Supported Platforms")
        platforms_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        platforms_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #4682B4;
                border-radius: 12px;
                margin-top: 8px;
                padding-top: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9), stop:1 rgba(255, 255, 255, 0.7));
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                color: #1e3a8a;
                font-weight: bold;
            }
        """)
        
        platforms_layout = QVBoxLayout(platforms_group)
        
        # Platform cards in grid
        cards_widget = QWidget()
        cards_widget.setStyleSheet("background: transparent;")
        cards_layout = QGridLayout(cards_widget)
        
        platforms = [
            ("YouTube", "▶", "Videos & Music"),
            ("PornHub", "[18+]", "Adult Content"),
            ("Twitter", "@", "Social Media"),
            ("Instagram", "IG", "Photos & Stories"),
            ("TikTok", "♪", "Short Videos"),
            ("Generic", "WEB", "1800+ Sites")
        ]
        
        for i, (name, icon, desc) in enumerate(platforms):
            card = PlatformCard(name, icon, desc)
            cards_layout.addWidget(card, i // 3, i % 3)
        
        platforms_layout.addWidget(cards_widget)
        layout.addWidget(platforms_group)
    
    def create_progress_section(self, layout):
        """Create progress section"""
        progress_group = QGroupBox("Download Progress")
        progress_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        progress_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #4682B4;
                border-radius: 12px;
                margin-top: 8px;
                padding-top: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9), stop:1 rgba(255, 255, 255, 0.7));
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                color: #1e3a8a;
                font-weight: bold;
            }
        """)
        
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_card = ProgressCard()
        progress_layout.addWidget(self.progress_card)
        
        layout.addWidget(progress_group)
    
    def create_controls(self, layout):
        """Create control buttons"""
        controls_layout = QVBoxLayout()
        
        # 主要控制按钮行
        main_controls = QHBoxLayout()
        
        self.download_btn = AppleButton("▼ Download", primary=True)
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.start_download)
        
        self.audio_btn = AppleButton("♪ Audio Only")
        self.audio_btn.setEnabled(False)
        self.audio_btn.clicked.connect(self.download_audio)
        
        self.info_btn = AppleButton("ℹ️ Info")
        self.info_btn.setEnabled(False)
        self.info_btn.clicked.connect(self.show_video_info)
        
        main_controls.addWidget(self.download_btn)
        main_controls.addWidget(self.audio_btn)
        main_controls.addWidget(self.info_btn)
        main_controls.addStretch()
        
        # 下载控制按钮行
        download_controls = QHBoxLayout()
        
        self.pause_btn = AppleButton("⏸️ Pause")
        self.pause_btn.setEnabled(False)
        self.pause_btn.clicked.connect(self.pause_download)
        self.pause_btn.setStyleSheet("""
            QPushButton {
                background: #FF9500;
                border: none;
                border-radius: 12px;
                color: white;
                font-weight: 600;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background: #E6850E;
            }
            QPushButton:pressed {
                background: #CC7A0D;
            }
            QPushButton:disabled {
                background: #C7C7CC;
                color: #8E8E93;
            }
        """)
        
        self.resume_btn = AppleButton("▶️ Resume")
        self.resume_btn.setEnabled(False)
        self.resume_btn.clicked.connect(self.resume_download)
        self.resume_btn.setStyleSheet("""
            QPushButton {
                background: #34C759;
                border: none;
                border-radius: 12px;
                color: white;
                font-weight: 600;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background: #2FB344;
            }
            QPushButton:pressed {
                background: #28A03D;
            }
            QPushButton:disabled {
                background: #C7C7CC;
                color: #8E8E93;
            }
        """)
        
        self.stop_btn = AppleButton("⏹️ Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_download)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background: #FF3B30;
                border: none;
                border-radius: 12px;
                color: white;
                font-weight: 600;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background: #E6342A;
            }
            QPushButton:pressed {
                background: #CC2E25;
            }
            QPushButton:disabled {
                background: #C7C7CC;
                color: #8E8E93;
            }
        """)
        
        self.folder_btn = AppleButton("📁 Open Folder")
        self.folder_btn.clicked.connect(self.open_downloads_folder)
        
        download_controls.addWidget(self.pause_btn)
        download_controls.addWidget(self.resume_btn)
        download_controls.addWidget(self.stop_btn)
        download_controls.addStretch()
        download_controls.addWidget(self.folder_btn)
        
        controls_layout.addLayout(main_controls)
        controls_layout.addLayout(download_controls)
        
        layout.addLayout(controls_layout)
        
        # 初始化下载状态
        self.download_paused = False
        self.current_downloads = {}
    
    def center_window(self):
        """Center window on screen"""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def on_url_changed(self):
        """Handle URL input changes"""
        text = self.url_input.toPlainText().strip()
        urls = self._extract_urls(text)
        
        has_urls = len(urls) > 0
        self.download_btn.setEnabled(has_urls)
        self.audio_btn.setEnabled(has_urls)
        self.info_btn.setEnabled(has_urls)
        
        if has_urls:
            if len(urls) == 1:
                # Single URL - detect platform
                platform = self._detect_platform(urls[0])
                self.statusBar().showMessage(f"Platform detected: {platform}")
                self.progress_card.update_progress("Ready to download", 0, f"Platform: {platform}")
            else:
                # Multiple URLs
                platforms = set(self._detect_platform(url) for url in urls)
                platform_str = ", ".join(platforms) if len(platforms) <= 3 else f"{len(platforms)} platforms"
                self.statusBar().showMessage(f"Found {len(urls)} URLs ({platform_str})")
                self.progress_card.update_progress("Ready for batch download", 0, f"{len(urls)} URLs ready")
        else:
            self.statusBar().showMessage("Ready")
            self.progress_card.update_progress("Ready to download", 0, "Waiting for URL...")
    
    def _extract_urls(self, text: str) -> list:
        """Extract valid URLs from text"""
        if not text:
            return []
        
        urls = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('http://') or line.startswith('https://')):
                # Basic URL validation
                if any(domain in line.lower() for domain in ['youtube.com', 'youtu.be', 'pornhub.com', 'twitter.com', 'x.com', 'instagram.com', 'tiktok.com', 'bilibili.com', 'twitch.tv']):
                    urls.append(line)
        
        return urls
    
    def _detect_platform(self, url: str) -> str:
        """Detect platform from URL"""
        url_lower = url.lower()
        if "youtube.com" in url_lower or "youtu.be" in url_lower:
            return "YouTube"
        elif "pornhub.com" in url_lower:
            return "PornHub"
        elif "twitter.com" in url_lower or "x.com" in url_lower:
            return "Twitter"
        elif "instagram.com" in url_lower:
            return "Instagram"
        elif "tiktok.com" in url_lower:
            return "TikTok"
        elif "bilibili.com" in url_lower:
            return "Bilibili"
        elif "twitch.tv" in url_lower:
            return "Twitch"
        else:
            return "Generic"
    
    def clear_urls(self):
        """Clear all URLs"""
        self.url_input.clear()
    
    def paste_url(self):
        """Paste URL from clipboard"""
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text:
            # If there's already text, append new URLs
            current_text = self.url_input.toPlainText().strip()
            if current_text:
                self.url_input.setPlainText(current_text + '\n' + text.strip())
            else:
                self.url_input.setPlainText(text.strip())
    
    def start_download(self):
        """Start video download(s)"""
        text = self.url_input.toPlainText().strip()
        urls = self._extract_urls(text)
        
        if not urls:
            QMessageBox.warning(self, "Error", "Please enter at least one valid URL")
            return
        
        if not self.downloader_available:
            QMessageBox.warning(self, "Error", "Downloader not available. Please check your installation.")
            return
        
        if len(urls) == 1:
            # Single download
            self.progress_card.update_progress("Starting download...", 0, "Initializing...")
            self.statusBar().showMessage("Download started")
            
            # Disable buttons during download
            self.download_btn.setEnabled(False)
            self.audio_btn.setEnabled(False)
            
            # Start download in background thread
            threading.Thread(target=self._download_worker, args=(urls[0], False), daemon=True).start()
        else:
            # Batch download
            reply = QMessageBox.question(self, "Batch Download", 
                                       f"Start batch download of {len(urls)} videos?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                self.progress_card.update_progress("Starting batch download...", 0, f"Processing {len(urls)} URLs...")
                self.statusBar().showMessage(f"Batch download started ({len(urls)} URLs)")
                
                # Disable buttons during download
                self.download_btn.setEnabled(False)
                self.audio_btn.setEnabled(False)
                
                # Start batch download in background thread
                threading.Thread(target=self._batch_download_worker, args=(urls, False), daemon=True).start()
    
    def download_audio(self):
        """Download audio only"""
        text = self.url_input.toPlainText().strip()
        urls = self._extract_urls(text)
        
        if not urls:
            QMessageBox.warning(self, "Error", "Please enter at least one valid URL")
            return
        
        if not self.downloader_available:
            QMessageBox.warning(self, "Error", "Downloader not available. Please check your installation.")
            return
        
        if len(urls) == 1:
            # Single audio download
            self.progress_card.update_progress("Starting audio download...", 0, "Initializing...")
            self.statusBar().showMessage("Audio download started")
            
            # Disable buttons during download
            self.download_btn.setEnabled(False)
            self.audio_btn.setEnabled(False)
            
            # Start download in background thread
            threading.Thread(target=self._download_worker, args=(urls[0], True), daemon=True).start()
        else:
            # Batch audio download
            reply = QMessageBox.question(self, "Batch Audio Download", 
                                       f"Start batch audio download of {len(urls)} videos?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                self.progress_card.update_progress("Starting batch audio download...", 0, f"Processing {len(urls)} URLs...")
                self.statusBar().showMessage(f"Batch audio download started ({len(urls)} URLs)")
                
                # Disable buttons during download
                self.download_btn.setEnabled(False)
                self.audio_btn.setEnabled(False)
                
                # Start batch download in background thread
                threading.Thread(target=self._batch_download_worker, args=(urls, True), daemon=True).start()
    
    def show_video_info(self):
        """Show video information"""
        text = self.url_input.toPlainText().strip()
        urls = self._extract_urls(text)
        
        if not urls:
            QMessageBox.warning(self, "Error", "Please enter at least one valid URL")
            return
        
        if not self.downloader_available:
            QMessageBox.warning(self, "Error", "Downloader not available. Please check your installation.")
            return
        
        # Show info for first URL only
        url = urls[0]
        
        # Get video info in background thread
        self.info_btn.setEnabled(False)
        self.statusBar().showMessage("Getting video info...")
        threading.Thread(target=self._info_worker, args=(url,), daemon=True).start()
    
    def show_platform_info(self, platform: str):
        """Show platform information"""
        QMessageBox.information(self, f"{platform} Support", f"{platform} platform is fully supported!\n\nClick on a platform card to see more details.")
    
    def open_downloads_folder(self):
        """Open downloads folder"""
        # 使用可移植路径管理器
        try:
            from portable.path_manager import PathManager
            path_manager = PathManager(silent=True)
            downloads_path = path_manager.resolve_relative_path("./downloads")
        except ImportError:
            # 回退到原始方式
            downloads_path = Path("./downloads")
            
        downloads_path.mkdir(exist_ok=True)
        
        # Open folder in file explorer
        import subprocess
        if sys.platform == "win32":
            subprocess.run(["explorer", str(downloads_path)], shell=True)
        elif sys.platform == "darwin":
            subprocess.run(["open", str(downloads_path)])
        else:
            subprocess.run(["xdg-open", str(downloads_path)])
    
    def _on_download_progress(self, task_id: str, progress: float, speed: float):
        """Handle download progress updates - THREAD SAFE VERSION"""
        try:
            if hasattr(self, 'downloader') and self.downloader and hasattr(self.downloader, 'get_task_status'):
                task = self.downloader.get_task_status(task_id)
                if task and hasattr(task, 'title'):
                    speed_mb = speed / 1024 / 1024 if speed > 0 else 0
                    status = f"Speed: {speed_mb:.1f} MB/s"
                    
                    # Create local variables to avoid lambda closure issues
                    title = task.title[:50] + "..." if len(task.title) > 50 else task.title
                    
                    # Update UI in main thread with proper variable capture
                    def update_ui():
                        try:
                            self.progress_card.update_progress(title, progress, status)
                        except Exception as e:
                            print(f"UI update error: {e}")
                    
                    QTimer.singleShot(0, update_ui)
                    
                    print(f"Progress: {progress:.1f}% | Speed: {speed_mb:.1f} MB/s | Task: {task.title[:30]}")
                    
                    if progress >= 100:
                        print(f"Download completed: {task.title}")
                else:
                    # Fallback for when task info is not available
                    speed_mb = speed / 1024 / 1024 if speed > 0 else 0
                    status = f"Speed: {speed_mb:.1f} MB/s"
                    
                    def update_ui():
                        try:
                            self.progress_card.update_progress("Downloading...", progress, status)
                        except Exception as e:
                            print(f"UI update error: {e}")
                    
                    QTimer.singleShot(0, update_ui)
                    print(f"Progress: {progress:.1f}% | Speed: {speed_mb:.1f} MB/s")
        except Exception as e:
            print(f"Progress update error: {e}")
    
    def _download_worker(self, url: str, audio_only: bool):
        """Background download worker - FIXED VERSION"""
        try:
            print(f"=== GUI DOWNLOAD WORKER START ===")
            print(f"URL: {url}")
            print(f"Audio only: {audio_only}")
            print(f"Downloader type: {self.downloader_type}")
            print(f"Current working directory: {os.getcwd()}")
            
            # Ensure we're in the right directory
            os.chdir("D:\\000cc")
            print(f"Changed to directory: {os.getcwd()}")
            
            # Create downloads directory
            downloads_dir = Path("./downloads")
            downloads_dir.mkdir(exist_ok=True)
            downloads_dir = downloads_dir.resolve()  # Get absolute path
            print(f"Downloads directory: {downloads_dir}")
            
            if self.downloader_type == "simple":
                print("=== USING SIMPLE DOWNLOADER ===")
                
                # Create progress callback that works in threads
                def safe_progress_callback(progress, speed):
                    try:
                        speed_mb = speed / 1024 / 1024 if speed > 0 else 0
                        print(f"Progress callback: {progress:.1f}% | {speed_mb:.1f} MB/s")
                        
                        # Use QTimer.singleShot to update UI safely
                        QTimer.singleShot(0, lambda p=progress, s=speed_mb: self.progress_card.update_progress(
                            "Downloading...",
                            p,
                            f"Speed: {s:.1f} MB/s"
                        ))
                    except Exception as e:
                        print(f"Progress callback error: {e}")
                
                print("Calling simple downloader...")
                success = self.downloader.download(
                    url, 
                    str(downloads_dir), 
                    audio_only=audio_only, 
                    progress_callback=safe_progress_callback
                )
                print(f"Simple downloader result: {success}")
                
            elif self.downloader_type == "advanced":
                print("=== USING ADVANCED DOWNLOADER ===")
                
                print("Adding download task...")
                task_id = self.downloader.add_task(url, str(downloads_dir), audio_only=audio_only)
                print(f"Task ID: {task_id}")
                
                # Update UI to show task started
                QTimer.singleShot(0, lambda: self.progress_card.update_progress(
                    "Initializing download...", 1, "Connecting..."
                ))
                
                print("Starting download...")
                future = self.downloader.start_download(task_id)
                
                # Monitor progress while waiting
                import time
                start_time = time.time()
                while not future.done():
                    try:
                        # Check task status and update UI
                        task = self.downloader.get_task_status(task_id)
                        if task and hasattr(task, 'title'):
                            elapsed = time.time() - start_time
                            QTimer.singleShot(0, lambda t=task.title: self.progress_card.update_progress(
                                f"Downloading: {t[:30]}...", 
                                min(50, elapsed * 2),  # Fake progress until real progress comes
                                "Downloading..."
                            ))
                        time.sleep(0.5)  # Check every 0.5 seconds
                    except:
                        pass
                
                print("Waiting for final result...")
                success = future.result(timeout=300)  # 5 minute timeout
                print(f"Advanced downloader result: {success}")
                
                if not success:
                    task = self.downloader.get_task_status(task_id)
                    error_msg = task.error_message if task else "Unknown error"
                    print(f"Task error: {error_msg}")
                    raise Exception(error_msg)
            else:
                raise Exception("No downloader available")
            
            print("=== DOWNLOAD SUCCESS ===")
            
            # Update UI to show completion immediately
            QTimer.singleShot(0, lambda: self.progress_card.update_progress(
                "Download Complete!", 100, "[OK] Processing files..."
            ))
            
            # Check if files were actually downloaded
            downloaded_files = list(downloads_dir.glob("*"))
            if downloaded_files:
                print("Downloaded files:")
                for file in downloaded_files:
                    print(f"  - {file.name}")
                
                # Show final success with file info
                largest_file = max(downloaded_files, key=lambda f: f.stat().st_size)
                file_size = largest_file.stat().st_size / 1024 / 1024  # MB
                
                QTimer.singleShot(500, lambda: self.progress_card.update_progress(
                    "Download Complete!", 100, f"[OK] {largest_file.name[:20]}... ({file_size:.1f}MB)"
                ))
            else:
                print("WARNING: No files found in downloads directory")
                QTimer.singleShot(0, lambda: self.progress_card.update_progress(
                    "Download Complete?", 100, "[Warning] No files found"
                ))
            
            # Update UI in main thread
            QTimer.singleShot(1000, lambda: self._download_completed(True, "Download completed successfully!"))
                
        except Exception as e:
            print(f"=== DOWNLOAD WORKER EXCEPTION ===")
            print(f"Exception type: {type(e).__name__}")
            print(f"Exception message: {str(e)}")
            
            import traceback
            print("Full traceback:")
            traceback.print_exc()
            
            # Update UI in main thread
            QTimer.singleShot(0, lambda: self._download_completed(False, f"Error: {str(e)}"))
    
    def _batch_download_worker(self, urls: list, audio_only: bool):
        """Background batch download worker"""
        try:
            print(f"=== BATCH DOWNLOAD WORKER START ===")
            print(f"URLs: {len(urls)}")
            print(f"Audio only: {audio_only}")
            
            # Ensure we're in the right directory
            os.chdir("D:\\000cc")
            
            # Create downloads directory
            downloads_dir = Path("./downloads")
            downloads_dir.mkdir(exist_ok=True)
            downloads_dir = downloads_dir.resolve()
            
            successful_downloads = 0
            failed_downloads = 0
            
            for i, url in enumerate(urls, 1):
                try:
                    print(f"\n=== DOWNLOADING {i}/{len(urls)} ===")
                    print(f"URL: {url}")
                    
                    # Update UI progress
                    overall_progress = (i - 1) / len(urls) * 100
                    QTimer.singleShot(0, lambda p=overall_progress, curr=i, total=len(urls): 
                                    self.progress_card.update_progress(
                                        f"Batch Download ({curr}/{total})",
                                        p,
                                        f"Processing: {self._detect_platform(url)}"
                                    ))
                    
                    # Download using the appropriate method
                    if self.downloader_type == "simple":
                        success = self.downloader.download(url, str(downloads_dir), audio_only=audio_only)
                    else:
                        # Advanced downloader
                        task_id = self.downloader.add_task(url, str(downloads_dir), audio_only=audio_only)
                        future = self.downloader.start_download(task_id)
                        success = future.result(timeout=300)
                    
                    if success:
                        successful_downloads += 1
                        print(f"✓ Download {i} successful")
                    else:
                        failed_downloads += 1
                        print(f"✗ Download {i} failed")
                        
                except Exception as e:
                    failed_downloads += 1
                    print(f"✗ Download {i} exception: {str(e)}")
                
                # Update progress
                completed_progress = i / len(urls) * 100
                QTimer.singleShot(0, lambda p=completed_progress, curr=i, total=len(urls): 
                                self.progress_card.update_progress(
                                    f"Batch Download ({curr}/{total})",
                                    p,
                                    f"Completed: {curr}/{total}"
                                ))
            
            print(f"\n=== BATCH DOWNLOAD COMPLETE ===")
            print(f"Successful: {successful_downloads}")
            print(f"Failed: {failed_downloads}")
            
            # Final UI update
            QTimer.singleShot(0, lambda: self.progress_card.update_progress(
                "Batch Download Complete!",
                100,
                f"[OK] {successful_downloads} successful, {failed_downloads} failed"
            ))
            
            # Show completion message
            message = f"Batch download completed!\n\nSuccessful: {successful_downloads}\nFailed: {failed_downloads}"
            if successful_downloads > 0:
                QTimer.singleShot(1000, lambda: self._download_completed(True, message))
            else:
                QTimer.singleShot(1000, lambda: self._download_completed(False, "All downloads failed"))
                
        except Exception as e:
            print(f"=== BATCH DOWNLOAD EXCEPTION ===")
            print(f"Exception: {str(e)}")
            import traceback
            traceback.print_exc()
            
            QTimer.singleShot(0, lambda: self._download_completed(False, f"Batch download error: {str(e)}"))
    
    def _download_completed(self, success: bool, message: str):
        """Handle download completion in main thread"""
        if success:
            self.progress_card.update_progress("Download Complete", 100, "[OK] Saved to downloads folder")
            self.statusBar().showMessage("Download completed successfully")
            QMessageBox.information(self, "Success", message)
        else:
            self.progress_card.update_progress("Download Failed", 0, "[ERROR] Check error details")
            self.statusBar().showMessage("Download failed")
            QMessageBox.warning(self, "Error", message)
        
        # Re-enable buttons
        url_has_text = bool(self.url_input.text().strip())
        self.download_btn.setEnabled(url_has_text)
        self.audio_btn.setEnabled(url_has_text)
    
    def _info_worker(self, url: str):
        """Background info worker"""
        try:
            print(f"Getting info for: {url}")
            
            if self.downloader_type == "advanced":
                # Use advanced downloader
                info = self.downloader.extractor.extract_info(url)
            elif self.downloader_type == "simple":
                # Use simple downloader with improved error handling
                info = self.downloader.get_video_info(url)
            else:
                raise Exception("No downloader available")
            
            # Format info for display
            title = info.get('title', 'Unknown')
            uploader = info.get('uploader', 'Unknown')
            duration = info.get('duration', 0)
            view_count = info.get('view_count', 0)
            
            duration_str = "Unknown"
            if duration:
                minutes, seconds = divmod(duration, 60)
                duration_str = f"{minutes:02d}:{seconds:02d}"
            
            view_str = f"{view_count:,}" if view_count else "Unknown"
            
            info_text = f"Title: {title}\n\nUploader: {uploader}\nDuration: {duration_str}\nViews: {view_str}"
            
            # Show in main thread
            QTimer.singleShot(0, lambda: self._show_info_result(info_text))
            
        except Exception as e:
            error_msg = str(e)
            print(f"Info extraction error: {error_msg}")
            QTimer.singleShot(0, lambda: self._show_info_result(f"Error getting video info:\n\n{error_msg}"))
    
    def _show_info_result(self, info_text: str):
        """Show info result in main thread"""
        QMessageBox.information(self, "Video Information", info_text)
        self.info_btn.setEnabled(True)
        self.statusBar().showMessage("Ready")
    
    def show_settings(self):
        """Show settings dialog"""
        if not self.downloader_available:
            QMessageBox.warning(self, "Error", "Downloader not available. Settings cannot be configured.")
            return
        
        # Simple settings dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        # Speed profile setting
        speed_group = QGroupBox("Speed Profile")
        speed_layout = QVBoxLayout(speed_group)
        
        current_profile = getattr(self.downloader, 'speed_profile', 'balanced')
        
        self.speed_radio_buttons = {}
        profiles = ['conservative', 'balanced', 'aggressive', 'ultra']
        for profile in profiles:
            radio = QRadioButton(profile.title())
            if profile == current_profile:
                radio.setChecked(True)
            self.speed_radio_buttons[profile] = radio
            speed_layout.addWidget(radio)
        
        layout.addWidget(speed_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = ModernButton("Save", primary=True)
        cancel_btn = ModernButton("Cancel")
        
        save_btn.clicked.connect(lambda: self._save_settings(dialog))
        cancel_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        dialog.exec()
    
    def _save_settings(self, dialog):
        """Save settings and restart downloader"""
        # Get selected speed profile
        new_profile = 'balanced'
        for profile, radio in self.speed_radio_buttons.items():
            if radio.isChecked():
                new_profile = profile
                break
        
        # Restart downloader with new settings
        try:
            if self.downloader:
                self.downloader.shutdown()
            
            from universal_downloader import DownloadManager
            self.downloader = HighSpeedDownloader(speed_profile=new_profile, max_workers=4)
            self.downloader.add_progress_callback(self._on_download_progress)
            
            QMessageBox.information(dialog, "Success", f"Settings saved! Speed profile: {new_profile}")
            dialog.accept()
            
        except Exception as e:
            QMessageBox.warning(dialog, "Error", f"Failed to apply settings: {str(e)}")
    
    def show_cookies(self):
        """Show cookie management dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Cookie Management")
        dialog.setFixedSize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Info
        info_label = QLabel("Import cookies to access age-restricted content")
        info_label.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(info_label)
        
        # Cookie list
        cookies_group = QGroupBox("Installed Cookies")
        cookies_layout = QVBoxLayout(cookies_group)
        
        self.cookies_list = QListWidget()
        self._refresh_cookies_list()
        cookies_layout.addWidget(self.cookies_list)
        
        layout.addWidget(cookies_group)
        
        # Import section
        import_group = QGroupBox("Import New Cookies")
        import_layout = QVBoxLayout(import_group)
        
        # Platform selection
        platform_layout = QHBoxLayout()
        platform_layout.addWidget(QLabel("Platform:"))
        self.platform_combo = QComboBox()
        self.platform_combo.addItems(["pornhub", "youtube", "twitter", "instagram", "custom"])
        platform_layout.addWidget(self.platform_combo)
        platform_layout.addStretch()
        import_layout.addLayout(platform_layout)
        
        # JSON input
        self.cookies_text = QTextEdit()
        self.cookies_text.setPlaceholderText("Paste your JSON cookies here...")
        self.cookies_text.setMaximumHeight(100)
        import_layout.addWidget(self.cookies_text)
        
        layout.addWidget(import_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        import_btn = ModernButton("Import Cookies", primary=True)
        import_btn.clicked.connect(lambda: self._import_cookies_gui(dialog))
        
        delete_btn = ModernButton("Delete Selected")
        delete_btn.clicked.connect(self._delete_selected_cookies)
        
        close_btn = ModernButton("Close")
        close_btn.clicked.connect(dialog.accept)
        
        button_layout.addWidget(import_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
        
        dialog.exec()
    
    def _refresh_cookies_list(self):
        """Refresh the cookies list display"""
        self.cookies_list.clear()
        
        try:
            from cookie_manager import CookieManager
            manager = CookieManager()
            cookies = manager.list_cookies()
            
            if cookies:
                for platform, file_path in cookies.items():
                    item_text = f"{platform} - {Path(file_path).name}"
                    self.cookies_list.addItem(item_text)
            else:
                self.cookies_list.addItem("No cookies installed")
                
        except Exception as e:
            self.cookies_list.addItem(f"Error loading cookies: {str(e)}")
    
    def _import_cookies_gui(self, dialog):
        """Import cookies from GUI"""
        try:
            from cookie_manager import CookieManager
            
            platform = self.platform_combo.currentText()
            cookies_json = self.cookies_text.toPlainText().strip()
            
            if not cookies_json:
                QMessageBox.warning(dialog, "Error", "Please paste your JSON cookies")
                return
            
            if platform == "custom":
                platform, ok = QInputDialog.getText(dialog, "Custom Platform", "Enter platform name:")
                if not ok or not platform:
                    return
            
            manager = CookieManager()
            cookies_file = manager.save_json_cookies(cookies_json, platform)
            
            if cookies_file:
                QMessageBox.information(dialog, "Success", f"Cookies imported for {platform}!")
                self._refresh_cookies_list()
                self.cookies_text.clear()
                
                # Refresh downloader cookies
                if self.downloader_available:
                    self.downloader.extractor._setup_cookies()
            else:
                QMessageBox.warning(dialog, "Error", "Failed to import cookies. Check JSON format.")
                
        except Exception as e:
            QMessageBox.warning(dialog, "Error", f"Import failed: {str(e)}")
    
    def _delete_selected_cookies(self):
        """Delete selected cookies"""
        current_item = self.cookies_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select cookies to delete")
            return
        
        item_text = current_item.text()
        if "No cookies" in item_text or "Error" in item_text:
            return
        
        # Extract platform name
        platform = item_text.split(" - ")[0]
        
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   f"Delete cookies for {platform}?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                from cookie_manager import CookieManager
                manager = CookieManager()
                manager.delete_cookies(platform)
                
                QMessageBox.information(self, "Success", f"Cookies deleted for {platform}")
                self._refresh_cookies_list()
                
                # Refresh downloader cookies
                if self.downloader_available:
                    self.downloader.extractor._setup_cookies()
                    
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Delete failed: {str(e)}")


def create_gui_installer():
    """Create GUI installer script"""
    installer_code = '''
@echo off
echo Installing PyQt6 for GUI interface...
echo.

pip install PyQt6
if %errorlevel% neq 0 (
    echo PyQt6 installation failed, trying PySide6...
    pip install PySide6
    if %errorlevel% neq 0 (
        echo Both PyQt6 and PySide6 installation failed.
        echo Please install manually: pip install PyQt6
        pause
        exit /b 1
    )
)

echo.
echo GUI framework installed successfully!
echo You can now run: python gui_downloader.py
pause
'''
    
    with open("install_gui.bat", "w") as f:
        f.write(installer_code)


def main():
    """Main entry point"""
    if not PYQT_AVAILABLE:
        print("PyQt6/PySide6 not installed!")
        print("Please install with: pip install PyQt6")
        print("Or run: install_gui.bat")
        
        # Create installer
        create_gui_installer()
        return
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern style
    
    # Set application properties
    app.setApplicationName("Universal Video Downloader")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("VideoDownloader")
    
    # Create and show main window
    window = ModernVideoDownloader()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()