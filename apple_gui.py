#!/usr/bin/env python3
"""
Universal Video Downloader - Apple风格简洁GUI
简洁、美观、易用
"""

import sys
import os
from pathlib import Path
import threading

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
    """Apple风格按钮"""
    
    def __init__(self, text: str, primary: bool = False):
        super().__init__(text)
        self.primary = primary
        self.setMinimumHeight(44)
        self.setFont(QFont("Segoe UI", 15) if primary else QFont("Segoe UI", 14))
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


class SimpleVideoDownloader(QMainWindow):
    """Apple风格简洁视频下载器"""
    
    def __init__(self):
        super().__init__()
        self.download_paused = False
        self.current_downloads = {}
        
        # 初始化下载器
        self.init_downloader()
        self.init_ui()
        self.center_window()
    
    def init_downloader(self):
        """初始化下载器"""
        try:
            from universal_downloader import DownloadManager
            self.downloader = DownloadManager(max_workers=4)
            self.downloader.add_progress_callback(self._on_download_progress)
            self.downloader_available = True
            print("✅ Downloader initialized")
        except Exception as e:
            print(f"❌ Downloader initialization failed: {e}")
            self.downloader = None
            self.downloader_available = False
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("Universal Video Downloader")
        self.setFixedSize(600, 450)
        
        # 主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 主布局
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(24)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # 标题
        self.create_title(layout)
        
        # URL输入
        self.create_url_input(layout)
        
        # 进度显示
        self.create_progress(layout)
        
        # 控制按钮
        self.create_controls(layout)
        
        # 应用样式
        self.apply_styles()
    
    def create_title(self, layout):
        """创建标题"""
        title_layout = QVBoxLayout()
        
        # 主标题
        title = QLabel("🎬 Video Downloader")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #1D1D1F; margin-bottom: 8px;")
        
        # 副标题
        subtitle = QLabel("Simple • Fast • Beautiful")
        subtitle.setFont(QFont("Segoe UI", 16))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #86868B; margin-bottom: 20px;")
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        layout.addLayout(title_layout)
    
    def create_url_input(self, layout):
        """创建URL输入框"""
        # URL输入框
        self.url_input = QTextEdit()
        self.url_input.setPlaceholderText("Paste video URLs here (one per line)\n\nSupports: YouTube, TikTok, Twitter, Instagram, and 1800+ sites")
        self.url_input.setMaximumHeight(100)
        self.url_input.setMinimumHeight(80)
        self.url_input.setFont(QFont("Segoe UI", 14))
        self.url_input.textChanged.connect(self.on_url_changed)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.paste_btn = AppleButton("📋 Paste")
        self.paste_btn.clicked.connect(self.paste_url)
        
        self.clear_btn = AppleButton("🗑️ Clear")
        self.clear_btn.clicked.connect(self.clear_urls)
        
        button_layout.addWidget(self.paste_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        
        layout.addWidget(self.url_input)
        layout.addLayout(button_layout)
    
    def create_progress(self, layout):
        """创建进度显示"""
        progress_widget = QWidget()
        progress_widget.setFixedHeight(80)
        progress_layout = QVBoxLayout(progress_widget)
        progress_layout.setContentsMargins(20, 16, 20, 16)
        
        # 状态标签
        self.status_label = QLabel("Ready to download")
        self.status_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Medium))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #1D1D1F; margin-bottom: 8px;")
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(8)
        
        progress_layout.addWidget(self.status_label)
        progress_layout.addWidget(self.progress_bar)
        
        layout.addWidget(progress_widget)
    
    def create_controls(self, layout):
        """创建控制按钮"""
        # 主要按钮
        main_layout = QHBoxLayout()
        
        self.download_btn = AppleButton("⬇️ Download", primary=True)
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.start_download)
        
        self.audio_btn = AppleButton("🎵 Audio Only")
        self.audio_btn.setEnabled(False)
        self.audio_btn.clicked.connect(self.download_audio)
        
        main_layout.addWidget(self.download_btn)
        main_layout.addWidget(self.audio_btn)
        
        # 控制按钮
        control_layout = QHBoxLayout()
        
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
            QPushButton:hover { background: #E6850E; }
            QPushButton:disabled { background: #C7C7CC; color: #8E8E93; }
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
            QPushButton:hover { background: #2FB344; }
            QPushButton:disabled { background: #C7C7CC; color: #8E8E93; }
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
            QPushButton:hover { background: #E6342A; }
            QPushButton:disabled { background: #C7C7CC; color: #8E8E93; }
        """)
        
        self.folder_btn = AppleButton("📁 Open Folder")
        self.folder_btn.clicked.connect(self.open_downloads_folder)
        
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.resume_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addStretch()
        control_layout.addWidget(self.folder_btn)
        
        layout.addLayout(main_layout)
        layout.addLayout(control_layout)
    
    def apply_styles(self):
        """应用样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
            }
            QWidget {
                background-color: transparent;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QTextEdit {
                background-color: #F8F9FA;
                border: 2px solid #E9ECEF;
                border-radius: 12px;
                padding: 12px;
                color: #212529;
                font-size: 14px;
            }
            QTextEdit:focus {
                border-color: #007AFF;
                background-color: #FFFFFF;
            }
            QProgressBar {
                background-color: #F1F3F4;
                border: none;
                border-radius: 4px;
                text-align: center;
                color: #5F6368;
            }
            QProgressBar::chunk {
                background-color: #007AFF;
                border-radius: 4px;
            }
        """)
    
    def center_window(self):
        """居中窗口"""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def on_url_changed(self):
        """URL输入变化"""
        text = self.url_input.toPlainText().strip()
        urls = self._extract_urls(text)
        
        has_urls = len(urls) > 0
        self.download_btn.setEnabled(has_urls and self.downloader_available)
        self.audio_btn.setEnabled(has_urls and self.downloader_available)
        
        if has_urls:
            if len(urls) == 1:
                platform = self._detect_platform(urls[0])
                self.status_label.setText(f"Ready to download from {platform}")
            else:
                self.status_label.setText(f"Ready to download {len(urls)} videos")
        else:
            self.status_label.setText("Ready to download")
    
    def _extract_urls(self, text: str) -> list:
        """提取URL"""
        if not text:
            return []
        
        urls = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('http://') or line.startswith('https://')):
                urls.append(line)
        
        return urls
    
    def _detect_platform(self, url: str) -> str:
        """检测平台"""
        url_lower = url.lower()
        if "youtube.com" in url_lower or "youtu.be" in url_lower:
            return "YouTube"
        elif "tiktok.com" in url_lower:
            return "TikTok"
        elif "twitter.com" in url_lower or "x.com" in url_lower:
            return "Twitter"
        elif "instagram.com" in url_lower:
            return "Instagram"
        else:
            return "Web"
    
    def paste_url(self):
        """粘贴URL"""
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text:
            current_text = self.url_input.toPlainText().strip()
            if current_text:
                self.url_input.setPlainText(current_text + '\n' + text.strip())
            else:
                self.url_input.setPlainText(text.strip())
    
    def clear_urls(self):
        """清空URL"""
        self.url_input.clear()
    
    def start_download(self):
        """开始下载"""
        if not self.downloader_available:
            QMessageBox.warning(self, "Error", "Downloader not available")
            return
        
        text = self.url_input.toPlainText().strip()
        urls = self._extract_urls(text)
        
        if not urls:
            QMessageBox.warning(self, "Error", "Please enter at least one valid URL")
            return
        
        # 禁用按钮
        self.download_btn.setEnabled(False)
        self.audio_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        
        # 开始下载
        threading.Thread(target=self._download_worker, args=(urls, False), daemon=True).start()
    
    def download_audio(self):
        """下载音频"""
        if not self.downloader_available:
            QMessageBox.warning(self, "Error", "Downloader not available")
            return
        
        text = self.url_input.toPlainText().strip()
        urls = self._extract_urls(text)
        
        if not urls:
            QMessageBox.warning(self, "Error", "Please enter at least one valid URL")
            return
        
        # 禁用按钮
        self.download_btn.setEnabled(False)
        self.audio_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        
        # 开始下载
        threading.Thread(target=self._download_worker, args=(urls, True), daemon=True).start()
    
    def pause_download(self):
        """暂停下载"""
        self.download_paused = True
        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(True)
        self.status_label.setText("Download paused")
    
    def resume_download(self):
        """恢复下载"""
        self.download_paused = False
        self.pause_btn.setEnabled(True)
        self.resume_btn.setEnabled(False)
        self.status_label.setText("Resuming download...")
    
    def stop_download(self):
        """停止下载"""
        self.download_paused = False
        self.current_downloads.clear()
        
        # 重置按钮
        text = self.url_input.toPlainText().strip()
        urls = self._extract_urls(text)
        has_urls = len(urls) > 0
        
        self.download_btn.setEnabled(has_urls and self.downloader_available)
        self.audio_btn.setEnabled(has_urls and self.downloader_available)
        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        
        self.status_label.setText("Download stopped")
        self.progress_bar.setValue(0)
    
    def _download_worker(self, urls: list, audio_only: bool):
        """下载工作线程"""
        try:
            total_urls = len(urls)
            completed = 0
            
            for i, url in enumerate(urls):
                if self.download_paused:
                    return
                
                self.status_label.setText(f"Downloading {i+1}/{total_urls}...")
                
                # 添加下载任务
                task_id = self.downloader.add_task(url, audio_only=audio_only)
                self.current_downloads[task_id] = url
                
                # 开始下载
                future = self.downloader.start_download(task_id)
                success = future.result()
                
                if success:
                    completed += 1
                
                # 更新进度
                progress = int(((i + 1) / total_urls) * 100)
                self.progress_bar.setValue(progress)
                
                # 清理
                if task_id in self.current_downloads:
                    del self.current_downloads[task_id]
            
            # 完成
            self.status_label.setText(f"Completed: {completed}/{total_urls}")
            
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
        finally:
            # 重置按钮
            text = self.url_input.toPlainText().strip()
            urls = self._extract_urls(text)
            has_urls = len(urls) > 0
            
            self.download_btn.setEnabled(has_urls and self.downloader_available)
            self.audio_btn.setEnabled(has_urls and self.downloader_available)
            self.pause_btn.setEnabled(False)
            self.resume_btn.setEnabled(False)
            self.stop_btn.setEnabled(False)
    
    def _on_download_progress(self, task_id: str, progress: float, speed: float):
        """下载进度回调"""
        if not self.download_paused and task_id in self.current_downloads:
            speed_text = f"{speed/1024/1024:.1f} MB/s" if speed > 0 else ""
            self.status_label.setText(f"Downloading... {speed_text}")
            self.progress_bar.setValue(int(progress))
    
    def open_downloads_folder(self):
        """打开下载文件夹"""
        try:
            from portable.path_manager import PathManager
            path_manager = PathManager(silent=True)
            downloads_path = path_manager.resolve_relative_path("./downloads")
        except ImportError:
            downloads_path = Path("./downloads")
        
        downloads_path.mkdir(exist_ok=True)
        
        import subprocess
        if sys.platform == "win32":
            subprocess.run(["explorer", str(downloads_path)], shell=True)
        elif sys.platform == "darwin":
            subprocess.run(["open", str(downloads_path)])
        else:
            subprocess.run(["xdg-open", str(downloads_path)])


def main():
    """主函数"""
    print("🔍 Starting Apple GUI...")
    
    if not PYQT_AVAILABLE:
        print("❌ PyQt6 or PySide6 not available. Please install one of them:")
        print("  uv pip install PyQt6")
        input("Press Enter to exit...")
        return 1
    
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Universal Video Downloader")
        app.setApplicationVersion("2.0")
        
        print("✅ QApplication created")
        
        # 设置应用样式
        app.setStyle("Fusion")
        
        # 创建并显示主窗口
        print("🔧 Creating main window...")
        window = SimpleVideoDownloader()
        
        print("📱 Showing window...")
        window.show()
        
        print("🚀 Starting event loop...")
        return app.exec()
        
    except Exception as e:
        print(f"❌ GUI Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        return 1


if __name__ == "__main__":
    sys.exit(main())