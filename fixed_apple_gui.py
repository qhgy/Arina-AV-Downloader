#!/usr/bin/env python3
"""
Universal Video Downloader - Fixed Apple Style GUI
Clean, Beautiful, No Black Background Issues
"""

import sys
import os
import threading
import time
from pathlib import Path
from typing import Optional, List

try:
    from PySide6.QtWidgets import *
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False
    print("❌ PySide6 not available. Please install: uv pip install PySide6")


class FixedAppleButton(QPushButton):
    """修复的Apple风格按钮"""
    
    def __init__(self, text: str, button_type: str = "secondary"):
        super().__init__(text)
        self.button_type = button_type
        self.setMinimumHeight(40)
        self.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._apply_style()
    
    def _apply_style(self):
        """应用按钮样式"""
        base_style = """
            QPushButton {
                border: none;
                border-radius: 12px;
                font-weight: 600;
                padding: 12px 24px;
            }
            QPushButton:disabled {
                background-color: #C7C7CC;
                color: #8E8E93;
            }
        """
        
        if self.button_type == "primary":
            style = base_style + """
                QPushButton {
                    background-color: #007AFF;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #0056CC;
                }
                QPushButton:pressed {
                    background-color: #004499;
                }
            """
        elif self.button_type == "danger":
            style = base_style + """
                QPushButton {
                    background-color: #FF3B30;
                    color: white;
                    padding: 10px 20px;
                }
                QPushButton:hover { background-color: #E6342A; }
            """
        elif self.button_type == "warning":
            style = base_style + """
                QPushButton {
                    background-color: #FF9500;
                    color: white;
                    padding: 10px 20px;
                }
                QPushButton:hover { background-color: #E6850E; }
            """
        elif self.button_type == "success":
            style = base_style + """
                QPushButton {
                    background-color: #34C759;
                    color: white;
                    padding: 10px 20px;
                }
                QPushButton:hover { background-color: #2FB344; }
            """
        else:  # secondary
            style = base_style + """
                QPushButton {
                    background-color: #FFFFFF;
                    border: 1px solid #D1D1D6;
                    color: #007AFF;
                    font-weight: 500;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #F2F2F7;
                    border-color: #007AFF;
                }
            """
        
        self.setStyleSheet(style)


class FixedAppleDownloader(QMainWindow):
    """修复的Apple风格视频下载器"""
    
    # 信号定义
    progress_updated = Signal(str, float, str)
    download_completed = Signal(bool, str)
    
    def __init__(self):
        super().__init__()
        
        # 下载状态
        self.is_downloading = False
        self.is_paused = False
        self.current_task_id = None
        
        # 初始化下载器
        self.init_downloader()
        
        # 初始化UI
        self.init_ui()
        
        # 连接信号
        self.progress_updated.connect(self.on_progress_updated)
        self.download_completed.connect(self.on_download_completed)
        
        # 居中窗口
        self.center_window()
    
    def init_downloader(self):
        """初始化下载器"""
        try:
            from universal_downloader import DownloadManager
            self.downloader = DownloadManager(max_workers=4)
            self.downloader.add_progress_callback(self._on_download_progress)
            self.downloader_available = True
            print("✅ Downloader initialized successfully")
        except Exception as e:
            print(f"❌ Downloader initialization failed: {e}")
            self.downloader = None
            self.downloader_available = False
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("Universal Video Downloader")
        self.setMinimumSize(600, 500)
        self.resize(700, 600)
        
        # 设置窗口背景色 - 最重要的修复
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F7;
            }
            * {
                background-color: #F5F5F7;
            }
        """)
        
        # 主窗口部件
        main_widget = QWidget()
        main_widget.setAutoFillBackground(True)
        palette = main_widget.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#F5F5F7"))
        main_widget.setPalette(palette)
        self.setCentralWidget(main_widget)
        
        # 主布局
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(24)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # 创建各个部分
        self.create_header(layout)
        self.create_url_input(layout)
        self.create_status_section(layout)
        self.create_controls(layout)
    
    def create_header(self, layout):
        """创建标题区域"""
        header_widget = QWidget()
        header_widget.setStyleSheet("background-color: #F5F5F7;")
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(8)
        
        # 主标题
        title = QLabel("🎬 Video Downloader")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #1D1D1F; background-color: #F5F5F7;")
        
        # 副标题
        subtitle = QLabel("Simple • Fast • Beautiful")
        subtitle.setFont(QFont("Segoe UI", 18))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #86868B; background-color: #F5F5F7;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_widget)
    
    def create_url_input(self, layout):
        """创建URL输入区域"""
        input_widget = QWidget()
        input_widget.setStyleSheet("background-color: #F5F5F7;")
        input_layout = QVBoxLayout(input_widget)
        input_layout.setSpacing(16)
        
        # URL输入框
        self.url_input = QTextEdit()
        self.url_input.setPlaceholderText(
            "Paste video URLs here (one per line)\n\n"
            "Supports:\n"
            "• YouTube, TikTok, Instagram, Twitter\n"
            "• PornHub and other adult sites\n"
            "• 1800+ websites via yt-dlp"
        )
        self.url_input.setMaximumHeight(140)
        self.url_input.setMinimumHeight(120)
        self.url_input.setFont(QFont("Segoe UI", 15))
        self.url_input.setStyleSheet("""
            QTextEdit {
                background-color: #FFFFFF;
                border: 2px solid #E5E5E7;
                border-radius: 16px;
                padding: 16px;
                color: #1D1D1F;
            }
            QTextEdit:focus {
                border-color: #007AFF;
            }
        """)
        self.url_input.textChanged.connect(self.on_url_changed)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(16)
        
        self.paste_btn = FixedAppleButton("📋 Paste", "secondary")
        self.paste_btn.clicked.connect(self.paste_url)
        
        self.clear_btn = FixedAppleButton("🗑️ Clear", "secondary")
        self.clear_btn.clicked.connect(self.clear_urls)
        
        button_layout.addWidget(self.paste_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        
        input_layout.addWidget(self.url_input)
        input_layout.addLayout(button_layout)
        
        layout.addWidget(input_widget)

    def create_status_section(self, layout):
        """创建状态显示区域"""
        status_widget = QWidget()
        status_widget.setFixedHeight(120)
        status_widget.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border: 1px solid #E5E5E7;
                border-radius: 16px;
            }
        """)

        status_layout = QVBoxLayout(status_widget)
        status_layout.setContentsMargins(24, 20, 24, 20)
        status_layout.setSpacing(12)

        # 状态标题
        self.status_title = QLabel("Ready to Download")
        self.status_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Medium))
        self.status_title.setStyleSheet("color: #1D1D1F; background-color: transparent;")
        self.status_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(25)  # 设置一个默认值让进度条可见
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #E5E5EA;
                border: 2px solid #D1D1D6;
                border-radius: 6px;
                text-align: center;
                color: #1D1D1F;
                font-size: 11px;
            }
            QProgressBar::chunk {
                background-color: #007AFF;
                border-radius: 4px;
            }
        """)

        # 状态详情
        self.status_detail = QLabel("Paste URLs and click Download")
        self.status_detail.setFont(QFont("Segoe UI", 14))
        self.status_detail.setStyleSheet("color: #86868B; background-color: transparent;")
        self.status_detail.setAlignment(Qt.AlignmentFlag.AlignCenter)

        status_layout.addWidget(self.status_title)
        status_layout.addWidget(self.progress_bar)
        status_layout.addWidget(self.status_detail)

        layout.addWidget(status_widget)

    def create_controls(self, layout):
        """创建控制按钮区域"""
        controls_widget = QWidget()
        controls_widget.setStyleSheet("background-color: #F5F5F7;")
        controls_layout = QVBoxLayout(controls_widget)
        controls_layout.setSpacing(16)

        # 主要操作按钮
        main_controls = QHBoxLayout()
        main_controls.setSpacing(16)

        self.download_btn = FixedAppleButton("⬇️ Download Video", "primary")
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.start_download)

        self.audio_btn = FixedAppleButton("🎵 Audio Only", "secondary")
        self.audio_btn.setEnabled(False)
        self.audio_btn.clicked.connect(self.download_audio)

        main_controls.addWidget(self.download_btn)
        main_controls.addWidget(self.audio_btn)

        # 下载控制按钮
        control_layout = QHBoxLayout()
        control_layout.setSpacing(12)

        self.pause_btn = FixedAppleButton("⏸️ Pause", "warning")
        self.pause_btn.setEnabled(False)
        self.pause_btn.clicked.connect(self.pause_download)

        self.resume_btn = FixedAppleButton("▶️ Resume", "success")
        self.resume_btn.setEnabled(False)
        self.resume_btn.clicked.connect(self.resume_download)

        self.stop_btn = FixedAppleButton("⏹️ Stop", "danger")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_download)

        self.folder_btn = FixedAppleButton("📁 Open Folder", "secondary")
        self.folder_btn.clicked.connect(self.open_downloads_folder)

        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.resume_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addStretch()
        control_layout.addWidget(self.folder_btn)

        controls_layout.addLayout(main_controls)
        controls_layout.addLayout(control_layout)

        layout.addWidget(controls_widget)

    def center_window(self):
        """居中窗口"""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )

    def on_url_changed(self):
        """URL输入变化处理"""
        text = self.url_input.toPlainText().strip()
        urls = self._extract_urls(text)

        has_urls = len(urls) > 0 and self.downloader_available
        self.download_btn.setEnabled(has_urls and not self.is_downloading)
        self.audio_btn.setEnabled(has_urls and not self.is_downloading)

        if has_urls:
            if len(urls) == 1:
                platform = self._detect_platform(urls[0])
                self.update_status("Ready to Download", 0, f"Platform: {platform}")
            else:
                self.update_status("Batch Download Ready", 0, f"{len(urls)} URLs ready")
        else:
            self.update_status("Ready to Download", 0, "Paste URLs and click Download")

    def _extract_urls(self, text: str) -> List[str]:
        """从文本中提取有效URL"""
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
        """检测URL平台"""
        url_lower = url.lower()
        if "youtube.com" in url_lower or "youtu.be" in url_lower:
            return "YouTube"
        elif "tiktok.com" in url_lower:
            return "TikTok"
        elif "twitter.com" in url_lower or "x.com" in url_lower:
            return "Twitter/X"
        elif "instagram.com" in url_lower:
            return "Instagram"
        elif "pornhub.com" in url_lower:
            return "PornHub"
        else:
            return "Web"

    def update_status(self, title: str, progress: float, detail: str):
        """更新状态显示"""
        self.status_title.setText(title)
        self.progress_bar.setValue(int(progress))
        self.status_detail.setText(detail)

    def paste_url(self):
        """粘贴URL"""
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()
        if text:
            current_text = self.url_input.toPlainText().strip()
            if current_text:
                self.url_input.setPlainText(current_text + '\n' + text)
            else:
                self.url_input.setPlainText(text)

    def clear_urls(self):
        """清空URL"""
        self.url_input.clear()

    def start_download(self):
        """开始视频下载"""
        QMessageBox.information(self, "Test", "Download function works!\nThis is the fixed version.")

    def download_audio(self):
        """开始音频下载"""
        QMessageBox.information(self, "Test", "Audio download function works!")

    def pause_download(self):
        """暂停下载"""
        QMessageBox.information(self, "Test", "Pause function works!")

    def resume_download(self):
        """恢复下载"""
        QMessageBox.information(self, "Test", "Resume function works!")

    def stop_download(self):
        """停止下载"""
        QMessageBox.information(self, "Test", "Stop function works!")

    def open_downloads_folder(self):
        """打开下载文件夹"""
        downloads_path = Path("./downloads")
        downloads_path.mkdir(exist_ok=True)

        import subprocess
        try:
            if sys.platform == "win32":
                subprocess.run(["explorer", str(downloads_path)], shell=True)
            else:
                QMessageBox.information(self, "Downloads", f"Downloads folder: {downloads_path.absolute()}")
        except Exception as e:
            QMessageBox.information(self, "Downloads", f"Downloads folder: {downloads_path.absolute()}")

    def on_progress_updated(self, title: str, progress: float, detail: str):
        """处理进度更新信号（主线程）"""
        self.update_status(title, progress, detail)

    def on_download_completed(self, success: bool, message: str):
        """处理下载完成信号（主线程）"""
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", message)

    def _on_download_progress(self, task_id: str, progress: float, speed: float):
        """下载进度回调（线程安全）"""
        pass  # 简化版本暂时不实现


def main():
    """主函数"""
    print("🚀 Starting Fixed Apple GUI...")

    if not PYSIDE6_AVAILABLE:
        print("❌ PySide6 not available")
        return 1

    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Universal Video Downloader")
        app.setApplicationVersion("3.0")

        # 设置应用程序样式
        app.setStyle("Fusion")

        window = FixedAppleDownloader()
        window.show()

        print("✅ Fixed Apple GUI started successfully!")
        return app.exec()

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
