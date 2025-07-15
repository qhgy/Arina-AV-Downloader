#!/usr/bin/env python3
"""
Universal Video Downloader - PySide6 Apple风格GUI
简洁、美观、傻瓜化操作
"""

import sys
import os
import threading
import time
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass

try:
    from PySide6.QtWidgets import *
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False
    print("❌ PySide6 not available. Please install: uv pip install PySide6")


@dataclass
class DownloadState:
    """下载状态管理"""
    is_downloading: bool = False
    is_paused: bool = False
    current_task_id: Optional[str] = None
    current_urls: List[str] = None
    total_progress: float = 0.0
    current_speed: float = 0.0
    status_text: str = "Ready"


class AppleProgressBar(QProgressBar):
    """Apple风格进度条"""
    
    def __init__(self):
        super().__init__()
        self.setRange(0, 100)
        self.setValue(0)
        self.setFixedHeight(8)
        self.setTextVisible(False)
        self.setStyleSheet("""
            QProgressBar {
                background-color: rgba(0, 0, 0, 0.1);
                border: none;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #007AFF, stop:1 #5AC8FA);
                border-radius: 4px;
            }
        """)


class AppleButton(QPushButton):
    """Apple风格按钮"""
    
    def __init__(self, text: str, button_type: str = "secondary"):
        super().__init__(text)
        self.button_type = button_type
        self.setMinimumHeight(44)
        self.setFont(QFont("SF Pro Display", 16, QFont.Weight.Medium))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._apply_style()
    
    def _apply_style(self):
        """应用按钮样式"""
        if self.button_type == "primary":
            style = """
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
        elif self.button_type == "danger":
            style = """
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
            """
        elif self.button_type == "warning":
            style = """
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
            """
        elif self.button_type == "success":
            style = """
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
            """
        else:  # secondary
            style = """
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
        
        self.setStyleSheet(style)


class StatusCard(QWidget):
    """状态显示卡片"""
    
    def __init__(self):
        super().__init__()
        self.setFixedHeight(120)
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border: 1px solid #E5E5E7;
                border-radius: 16px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)
        
        # 状态标题
        self.title_label = QLabel("Ready to Download")
        self.title_label.setFont(QFont("SF Pro Display", 18, QFont.Weight.Medium))
        self.title_label.setStyleSheet("color: #1D1D1F;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 进度条
        self.progress_bar = AppleProgressBar()
        
        # 状态详情
        self.detail_label = QLabel("Paste URLs and click Download")
        self.detail_label.setFont(QFont("SF Pro Display", 14))
        self.detail_label.setStyleSheet("color: #86868B;")
        self.detail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.detail_label)
    
    def update_status(self, title: str, progress: float, detail: str):
        """更新状态显示"""
        self.title_label.setText(title)
        self.progress_bar.setValue(int(progress))
        self.detail_label.setText(detail)


class AppleVideoDownloader(QMainWindow):
    """Apple风格视频下载器主窗口"""
    
    # 信号定义
    progress_updated = Signal(str, float, str)  # title, progress, detail
    download_completed = Signal(bool, str)  # success, message
    
    def __init__(self):
        super().__init__()
        
        # 下载状态
        self.download_state = DownloadState()
        
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
        self.setFixedSize(700, 600)
        
        # 设置窗口图标
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        
        # 主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 主布局
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(32)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # 创建各个部分
        self.create_header(layout)
        self.create_url_input(layout)
        self.create_status_section(layout)
        self.create_controls(layout)
        
        # 应用全局样式
        self.apply_global_styles()
    
    def create_header(self, layout):
        """创建标题区域"""
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)
        
        # 主标题
        title = QLabel("🎬 Video Downloader")
        title.setFont(QFont("SF Pro Display", 32, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #1D1D1F; margin-bottom: 4px;")
        
        # 副标题
        subtitle = QLabel("Simple • Fast • Beautiful")
        subtitle.setFont(QFont("SF Pro Display", 18))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #86868B;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        
        layout.addLayout(header_layout)

    def create_url_input(self, layout):
        """创建URL输入区域"""
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
        self.url_input.setFont(QFont("SF Pro Display", 15))
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
                background-color: #FFFFFF;
            }
        """)
        self.url_input.textChanged.connect(self.on_url_changed)

        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(16)

        self.paste_btn = AppleButton("📋 Paste", "secondary")
        self.paste_btn.clicked.connect(self.paste_url)

        self.clear_btn = AppleButton("🗑️ Clear", "secondary")
        self.clear_btn.clicked.connect(self.clear_urls)

        button_layout.addWidget(self.paste_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()

        layout.addWidget(self.url_input)
        layout.addLayout(button_layout)

    def create_status_section(self, layout):
        """创建状态显示区域"""
        self.status_card = StatusCard()
        layout.addWidget(self.status_card)

    def create_controls(self, layout):
        """创建控制按钮区域"""
        # 主要操作按钮
        main_controls = QHBoxLayout()
        main_controls.setSpacing(16)

        self.download_btn = AppleButton("⬇️ Download Video", "primary")
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.start_download)

        self.audio_btn = AppleButton("🎵 Audio Only", "secondary")
        self.audio_btn.setEnabled(False)
        self.audio_btn.clicked.connect(self.download_audio)

        main_controls.addWidget(self.download_btn)
        main_controls.addWidget(self.audio_btn)

        # 下载控制按钮
        control_layout = QHBoxLayout()
        control_layout.setSpacing(12)

        self.pause_btn = AppleButton("⏸️ Pause", "warning")
        self.pause_btn.setEnabled(False)
        self.pause_btn.clicked.connect(self.pause_download)

        self.resume_btn = AppleButton("▶️ Resume", "success")
        self.resume_btn.setEnabled(False)
        self.resume_btn.clicked.connect(self.resume_download)

        self.stop_btn = AppleButton("⏹️ Stop", "danger")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_download)

        self.folder_btn = AppleButton("📁 Open Folder", "secondary")
        self.folder_btn.clicked.connect(self.open_downloads_folder)

        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.resume_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addStretch()
        control_layout.addWidget(self.folder_btn)

        layout.addLayout(main_controls)
        layout.addLayout(control_layout)

    def apply_global_styles(self):
        """应用全局样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F7;
            }
            QWidget {
                background-color: transparent;
                font-family: 'Segoe UI', Arial, sans-serif;
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
        """URL输入变化处理"""
        text = self.url_input.toPlainText().strip()
        urls = self._extract_urls(text)

        has_urls = len(urls) > 0 and self.downloader_available
        self.download_btn.setEnabled(has_urls and not self.download_state.is_downloading)
        self.audio_btn.setEnabled(has_urls and not self.download_state.is_downloading)

        if has_urls:
            if len(urls) == 1:
                platform = self._detect_platform(urls[0])
                self.status_card.update_status(
                    "Ready to Download",
                    0,
                    f"Platform: {platform}"
                )
            else:
                platforms = set(self._detect_platform(url) for url in urls)
                platform_str = ", ".join(list(platforms)[:3])
                if len(platforms) > 3:
                    platform_str += f" +{len(platforms)-3} more"
                self.status_card.update_status(
                    "Batch Download Ready",
                    0,
                    f"{len(urls)} URLs • {platform_str}"
                )
        else:
            self.status_card.update_status(
                "Ready to Download",
                0,
                "Paste URLs and click Download"
            )

    def _extract_urls(self, text: str) -> List[str]:
        """从文本中提取有效URL"""
        if not text:
            return []

        urls = []
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if line and (line.startswith('http://') or line.startswith('https://')):
                # 基本URL验证
                if any(domain in line.lower() for domain in [
                    'youtube.com', 'youtu.be', 'tiktok.com', 'twitter.com', 'x.com',
                    'instagram.com', 'pornhub.com', 'bilibili.com', 'twitch.tv'
                ]) or '.' in line:
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
        elif "bilibili.com" in url_lower:
            return "Bilibili"
        elif "twitch.tv" in url_lower:
            return "Twitch"
        else:
            return "Web"

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
        self._start_download_process(audio_only=False)

    def download_audio(self):
        """开始音频下载"""
        self._start_download_process(audio_only=True)

    def _start_download_process(self, audio_only: bool):
        """开始下载流程"""
        if not self.downloader_available:
            QMessageBox.warning(self, "Error", "Downloader not available. Please check installation.")
            return

        text = self.url_input.toPlainText().strip()
        urls = self._extract_urls(text)

        if not urls:
            QMessageBox.warning(self, "Error", "Please enter at least one valid URL")
            return

        if self.download_state.is_downloading:
            QMessageBox.information(self, "Info", "Download already in progress")
            return

        # 更新下载状态
        self.download_state.is_downloading = True
        self.download_state.is_paused = False
        self.download_state.current_urls = urls

        # 更新UI状态
        self._update_ui_for_download_start()

        # 开始下载
        download_type = "Audio" if audio_only else "Video"
        if len(urls) == 1:
            self.status_card.update_status(
                f"Starting {download_type} Download...",
                0,
                "Initializing..."
            )
        else:
            self.status_card.update_status(
                f"Starting Batch {download_type} Download...",
                0,
                f"Processing {len(urls)} URLs..."
            )

        # 在后台线程中执行下载
        threading.Thread(
            target=self._download_worker,
            args=(urls, audio_only),
            daemon=True
        ).start()

    def pause_download(self):
        """暂停下载"""
        if self.download_state.is_downloading and not self.download_state.is_paused:
            self.download_state.is_paused = True

            # 更新UI
            self.pause_btn.setEnabled(False)
            self.resume_btn.setEnabled(True)

            self.status_card.update_status(
                "Download Paused",
                self.download_state.total_progress,
                "Click Resume to continue"
            )

    def resume_download(self):
        """恢复下载"""
        if self.download_state.is_downloading and self.download_state.is_paused:
            self.download_state.is_paused = False

            # 更新UI
            self.pause_btn.setEnabled(True)
            self.resume_btn.setEnabled(False)

            self.status_card.update_status(
                "Resuming Download...",
                self.download_state.total_progress,
                "Download resumed"
            )

    def stop_download(self):
        """停止下载"""
        if self.download_state.is_downloading:
            self.download_state.is_downloading = False
            self.download_state.is_paused = False
            self.download_state.current_task_id = None
            self.download_state.current_urls = None

            # 重置UI
            self._update_ui_for_download_end()

            self.status_card.update_status(
                "Download Stopped",
                0,
                "Ready for new download"
            )

    def _update_ui_for_download_start(self):
        """更新UI为下载开始状态"""
        self.download_btn.setEnabled(False)
        self.audio_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.resume_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def _update_ui_for_download_end(self):
        """更新UI为下载结束状态"""
        text = self.url_input.toPlainText().strip()
        urls = self._extract_urls(text)
        has_urls = len(urls) > 0 and self.downloader_available

        self.download_btn.setEnabled(has_urls)
        self.audio_btn.setEnabled(has_urls)
        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)

    def _download_worker(self, urls: List[str], audio_only: bool):
        """下载工作线程"""
        try:
            # 确保在正确的目录
            os.chdir(Path(__file__).parent)

            # 创建下载目录
            downloads_dir = Path("./downloads")
            downloads_dir.mkdir(exist_ok=True)
            downloads_dir = downloads_dir.resolve()

            total_urls = len(urls)
            completed = 0
            failed = 0

            for i, url in enumerate(urls):
                # 检查是否被停止
                if not self.download_state.is_downloading:
                    break

                # 等待暂停恢复
                while self.download_state.is_paused and self.download_state.is_downloading:
                    time.sleep(0.5)

                # 再次检查是否被停止
                if not self.download_state.is_downloading:
                    break

                try:
                    # 更新进度
                    overall_progress = (i / total_urls) * 100
                    self.download_state.total_progress = overall_progress

                    platform = self._detect_platform(url)
                    self.progress_updated.emit(
                        f"Downloading {i+1}/{total_urls}",
                        overall_progress,
                        f"Processing {platform} URL..."
                    )

                    # 添加下载任务
                    task_id = self.downloader.add_task(
                        url,
                        str(downloads_dir),
                        audio_only=audio_only
                    )
                    self.download_state.current_task_id = task_id

                    # 开始下载
                    future = self.downloader.start_download(task_id)
                    success = future.result(timeout=600)  # 10分钟超时

                    if success:
                        completed += 1
                    else:
                        failed += 1

                except Exception as e:
                    print(f"Download error for URL {i+1}: {e}")
                    failed += 1

                # 更新完成进度
                completed_progress = ((i + 1) / total_urls) * 100
                self.download_state.total_progress = completed_progress

            # 下载完成
            if self.download_state.is_downloading:  # 没有被手动停止
                success_rate = completed / total_urls if total_urls > 0 else 0

                if total_urls == 1:
                    if completed == 1:
                        message = "Download completed successfully!"
                        self.download_completed.emit(True, message)
                    else:
                        message = "Download failed. Please check the URL and try again."
                        self.download_completed.emit(False, message)
                else:
                    message = f"Batch download completed!\n\nSuccessful: {completed}\nFailed: {failed}"
                    self.download_completed.emit(success_rate > 0, message)

        except Exception as e:
            print(f"Download worker error: {e}")
            import traceback
            traceback.print_exc()
            self.download_completed.emit(False, f"Download error: {str(e)}")

        finally:
            # 重置下载状态
            self.download_state.is_downloading = False
            self.download_state.is_paused = False
            self.download_state.current_task_id = None
            self.download_state.current_urls = None

    def _on_download_progress(self, task_id: str, progress: float, speed: float):
        """下载进度回调（线程安全）"""
        try:
            # 使用QTimer.singleShot确保在主线程中更新UI
            def update_progress():
                try:
                    if (self.download_state.is_downloading and
                        not self.download_state.is_paused):

                        # 更新速度
                        self.download_state.current_speed = speed

                        # 格式化速度显示
                        if speed > 0:
                            speed_mb = speed / 1024 / 1024
                            if speed_mb >= 1:
                                speed_text = f"{speed_mb:.1f} MB/s"
                            else:
                                speed_kb = speed / 1024
                                speed_text = f"{speed_kb:.1f} KB/s"
                        else:
                            speed_text = "Calculating..."

                        # 获取任务信息
                        title = "Downloading..."
                        if hasattr(self, 'downloader') and self.downloader:
                            task = self.downloader.get_task_status(task_id)
                            if task and hasattr(task, 'title') and task.title:
                                title = task.title[:40] + "..." if len(task.title) > 40 else task.title

                        # 更新状态卡片
                        self.status_card.update_status(
                            title,
                            progress,
                            f"Speed: {speed_text}"
                        )

                except Exception as e:
                    print(f"Progress update error: {e}")

            # 在主线程中执行更新
            QTimer.singleShot(0, update_progress)

        except Exception as e:
            print(f"Progress callback error: {e}")

    def on_progress_updated(self, title: str, progress: float, detail: str):
        """处理进度更新信号（主线程）"""
        self.status_card.update_status(title, progress, detail)

    def on_download_completed(self, success: bool, message: str):
        """处理下载完成信号（主线程）"""
        # 重置UI状态
        self._update_ui_for_download_end()

        # 更新状态卡片
        if success:
            self.status_card.update_status(
                "Download Complete!",
                100,
                "Files saved to downloads folder"
            )
            QMessageBox.information(self, "Success", message)
        else:
            self.status_card.update_status(
                "Download Failed",
                0,
                "Check error details"
            )
            QMessageBox.warning(self, "Error", message)

    def open_downloads_folder(self):
        """打开下载文件夹"""
        try:
            from portable.path_manager import PathManager
            path_manager = PathManager(silent=True)
            downloads_path = path_manager.resolve_relative_path("./downloads")
        except ImportError:
            downloads_path = Path("./downloads")

        downloads_path.mkdir(exist_ok=True)

        # 打开文件夹
        import subprocess
        try:
            if sys.platform == "win32":
                subprocess.run(["explorer", str(downloads_path)], shell=True)
            elif sys.platform == "darwin":
                subprocess.run(["open", str(downloads_path)])
            else:
                subprocess.run(["xdg-open", str(downloads_path)])
        except Exception as e:
            QMessageBox.information(
                self,
                "Downloads Folder",
                f"Downloads are saved to:\n{downloads_path}\n\nCould not open folder automatically: {e}"
            )

    def closeEvent(self, event):
        """窗口关闭事件"""
        if self.download_state.is_downloading:
            reply = QMessageBox.question(
                self,
                "Confirm Exit",
                "Download is in progress. Are you sure you want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.stop_download()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    """主函数"""
    print("🚀 Starting PySide6 Apple GUI...")

    if not PYSIDE6_AVAILABLE:
        print("❌ PySide6 not available. Please install:")
        print("   uv pip install PySide6")
        input("Press Enter to exit...")
        return 1

    try:
        # 创建应用程序
        app = QApplication(sys.argv)
        app.setApplicationName("Universal Video Downloader")
        app.setApplicationVersion("3.0")
        app.setApplicationDisplayName("Video Downloader")

        print("✅ QApplication created")

        # 设置应用样式
        app.setStyle("Fusion")

        # 创建主窗口
        print("🔧 Creating main window...")
        window = AppleVideoDownloader()

        print("📱 Showing window...")
        window.show()

        print("🎉 GUI started successfully!")
        return app.exec()

    except Exception as e:
        print(f"❌ GUI Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        return 1


if __name__ == "__main__":
    sys.exit(main())
