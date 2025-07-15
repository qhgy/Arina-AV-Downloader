#!/usr/bin/env python3
"""
Arina Video Downloader - Perfect Apple Style GUI
Clean, Beautiful, Fully Functional
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


class PerfectAppleButton(QPushButton):
    """完美的Apple风格按钮"""
    
    def __init__(self, text: str, button_type: str = "secondary"):
        super().__init__(text)
        self.button_type = button_type
        self.setMinimumHeight(36)
        self.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._apply_style()
    
    def _apply_style(self):
        """应用按钮样式"""
        base_style = """
            QPushButton {
                border: none;
                border-radius: 10px;
                font-weight: 500;
                padding: 8px 16px;
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
                    font-weight: 600;
                    padding: 10px 20px;
                }
                QPushButton:hover { background-color: #0056CC; }
                QPushButton:pressed { background-color: #004499; }
            """
        elif self.button_type == "danger":
            style = base_style + """
                QPushButton {
                    background-color: #FF3B30;
                    color: white;
                }
                QPushButton:hover { background-color: #E6342A; }
            """
        elif self.button_type == "warning":
            style = base_style + """
                QPushButton {
                    background-color: #FF9500;
                    color: white;
                }
                QPushButton:hover { background-color: #E6850E; }
            """
        elif self.button_type == "success":
            style = base_style + """
                QPushButton {
                    background-color: #34C759;
                    color: white;
                }
                QPushButton:hover { background-color: #2FB344; }
            """
        else:  # secondary
            style = base_style + """
                QPushButton {
                    background-color: #FFFFFF;
                    border: 1px solid #D1D1D6;
                    color: #007AFF;
                }
                QPushButton:hover {
                    background-color: #F2F2F7;
                    border-color: #007AFF;
                }
            """
        
        self.setStyleSheet(style)


class PerfectAppleDownloader(QMainWindow):
    """完美的Apple风格视频下载器"""
    
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
        self.setWindowTitle("Arina Video Downloader")
        self.setMinimumSize(600, 500)
        self.resize(700, 600)
        
        # 设置窗口背景色
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
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
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
        header_layout.setSpacing(6)
        
        # 主标题
        title = QLabel("🎬 Video Downloader")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #1D1D1F; background-color: #F5F5F7;")
        
        # 副标题
        subtitle = QLabel("Simple • Fast • Beautiful")
        subtitle.setFont(QFont("Segoe UI", 16))
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
        input_layout.setSpacing(12)
        
        # URL输入框
        self.url_input = QTextEdit()
        self.url_input.setPlaceholderText(
            "Paste video URLs here (one per line)\n\n"
            "Supports: YouTube, TikTok, Instagram, Twitter, PornHub, and 1800+ sites"
        )
        self.url_input.setMaximumHeight(120)
        self.url_input.setMinimumHeight(100)
        self.url_input.setFont(QFont("Segoe UI", 13))
        self.url_input.setStyleSheet("""
            QTextEdit {
                background-color: #FFFFFF;
                border: 2px solid #E5E5E7;
                border-radius: 12px;
                padding: 12px;
                color: #1D1D1F;
            }
            QTextEdit:focus {
                border-color: #007AFF;
            }
        """)
        self.url_input.textChanged.connect(self.on_url_changed)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.paste_btn = PerfectAppleButton("📋 Paste", "secondary")
        self.paste_btn.clicked.connect(self.paste_url)
        
        self.clear_btn = PerfectAppleButton("🗑️ Clear", "secondary")
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
        status_widget.setFixedHeight(100)
        status_widget.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border: 1px solid #E5E5E7;
                border-radius: 12px;
            }
        """)
        
        status_layout = QVBoxLayout(status_widget)
        status_layout.setContentsMargins(20, 16, 20, 16)
        status_layout.setSpacing(8)
        
        # 状态标题
        self.status_title = QLabel("Ready to Download")
        self.status_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Medium))
        self.status_title.setStyleSheet("color: #1D1D1F; background-color: transparent;")
        self.status_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #E5E5EA;
                border: 1px solid #D1D1D6;
                border-radius: 5px;
                text-align: center;
                color: #1D1D1F;
                font-size: 10px;
            }
            QProgressBar::chunk {
                background-color: #007AFF;
                border-radius: 4px;
            }
        """)
        
        # 状态详情
        self.status_detail = QLabel("Paste URLs and click Download")
        self.status_detail.setFont(QFont("Segoe UI", 12))
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
        controls_layout.setSpacing(12)

        # 主要操作按钮
        main_controls = QHBoxLayout()
        main_controls.setSpacing(12)

        self.download_btn = PerfectAppleButton("⬇️ Download Video", "primary")
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.start_download)

        self.audio_btn = PerfectAppleButton("🎵 Audio Only", "secondary")
        self.audio_btn.setEnabled(False)
        self.audio_btn.clicked.connect(self.download_audio)

        main_controls.addWidget(self.download_btn)
        main_controls.addWidget(self.audio_btn)

        # 下载控制按钮
        control_layout = QHBoxLayout()
        control_layout.setSpacing(8)

        self.pause_btn = PerfectAppleButton("⏸️ Pause", "warning")
        self.pause_btn.setEnabled(False)
        self.pause_btn.clicked.connect(self.pause_download)

        self.resume_btn = PerfectAppleButton("▶️ Resume", "success")
        self.resume_btn.setEnabled(False)
        self.resume_btn.clicked.connect(self.resume_download)

        self.stop_btn = PerfectAppleButton("⏹️ Stop", "danger")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_download)

        self.folder_btn = PerfectAppleButton("📁 Open Folder", "secondary")
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

        if self.is_downloading:
            QMessageBox.information(self, "Info", "Download already in progress")
            return

        # 更新状态
        self.is_downloading = True
        self.is_paused = False

        # 更新UI
        self._update_ui_for_download_start()

        # 开始下载
        download_type = "Audio" if audio_only else "Video"
        if len(urls) == 1:
            self.update_status(f"Starting {download_type} Download...", 5, "Initializing...")
        else:
            self.update_status(f"Starting Batch {download_type} Download...", 5, f"Processing {len(urls)} URLs...")

        # 在后台线程中执行下载
        threading.Thread(target=self._download_worker, args=(urls, audio_only), daemon=True).start()

    def pause_download(self):
        """暂停下载"""
        if self.is_downloading and not self.is_paused:
            self.is_paused = True
            self.pause_btn.setEnabled(False)
            self.resume_btn.setEnabled(True)
            current_progress = self.progress_bar.value()
            self.update_status("Download Paused", current_progress, "Click Resume to continue")

    def resume_download(self):
        """恢复下载"""
        if self.is_downloading and self.is_paused:
            self.is_paused = False
            self.pause_btn.setEnabled(True)
            self.resume_btn.setEnabled(False)
            current_progress = self.progress_bar.value()
            self.update_status("Resuming Download...", current_progress, "Download resumed")

    def stop_download(self):
        """停止下载"""
        if self.is_downloading:
            self.is_downloading = False
            self.is_paused = False
            self.current_task_id = None

            # 重置UI
            self._update_ui_for_download_end()
            self.update_status("Download Stopped", 0, "Ready for new download")

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
        """并发下载工作线程"""
        try:
            # 确保在正确的目录
            os.chdir(Path(__file__).parent)

            # 创建下载目录
            downloads_dir = Path("./downloads")
            downloads_dir.mkdir(exist_ok=True)

            total_urls = len(urls)

            if total_urls == 1:
                # 单个下载 - 使用原有逻辑
                self._download_single(urls[0], downloads_dir, audio_only)
            else:
                # 多个下载 - 使用并发逻辑
                self._download_concurrent(urls, downloads_dir, audio_only)

        except Exception as e:
            print(f"Download worker error: {e}")
            self.download_completed.emit(False, f"Download error: {str(e)}")

        finally:
            # 重置下载状态
            self.is_downloading = False
            self.is_paused = False
            self.current_task_id = None

    def _download_single(self, url: str, downloads_dir: Path, audio_only: bool):
        """单个下载 - 实时进度显示"""
        try:
            platform = self._detect_platform(url)
            self.progress_updated.emit(
                "Initializing Download...",
                0,
                f"Connecting to {platform}..."
            )

            # 添加下载任务
            task_id = self.downloader.add_task(url, str(downloads_dir), audio_only=audio_only)
            self.current_task_id = task_id

            # 获取视频信息
            task = self.downloader.get_task_status(task_id)
            if task and task.title:
                title = task.title[:35] + "..." if len(task.title) > 35 else task.title
                self.progress_updated.emit(
                    f"Starting: {title}",
                    5,
                    "Preparing download..."
                )

            # 开始下载 - 不阻塞，让进度回调处理更新
            future = self.downloader.start_download(task_id)

            # 监控下载进度
            start_time = time.time()
            last_progress = 0

            while not future.done():
                if not self.is_downloading:
                    break

                # 等待暂停恢复
                while self.is_paused and self.is_downloading:
                    time.sleep(0.5)

                if not self.is_downloading:
                    break

                # 检查任务状态
                current_task = self.downloader.get_task_status(task_id)
                if current_task:
                    current_progress = current_task.progress

                    # 如果进度没有通过回调更新，手动更新
                    if current_progress > last_progress:
                        last_progress = current_progress
                        elapsed = time.time() - start_time

                        if current_task.title:
                            title = current_task.title[:35] + "..." if len(current_task.title) > 35 else current_task.title
                        else:
                            title = "Downloading..."

                        self.progress_updated.emit(
                            title,
                            current_progress,
                            f"Progress: {current_progress:.1f}% | Time: {elapsed:.0f}s"
                        )

                time.sleep(0.5)  # 每0.5秒检查一次

            # 获取最终结果
            success = future.result(timeout=10)  # 短超时，因为已经完成

            if success:
                self.progress_updated.emit(
                    "Download Complete!",
                    100,
                    "File saved successfully"
                )
                message = "Download completed successfully!"
                self.download_completed.emit(True, message)
            else:
                message = "Download failed. Please check the URL and try again."
                self.download_completed.emit(False, message)

        except Exception as e:
            print(f"Single download error: {e}")
            self.download_completed.emit(False, f"Download error: {str(e)}")

    def _download_concurrent(self, urls: List[str], downloads_dir: Path, audio_only: bool):
        """并发下载多个URL"""
        try:
            total_urls = len(urls)
            futures = []
            task_ids = []

            # 启动所有下载任务（并发）
            self.progress_updated.emit(
                f"Starting {total_urls} Downloads...",
                5,
                "Initializing concurrent downloads..."
            )

            for i, url in enumerate(urls):
                if not self.is_downloading:
                    break

                try:
                    platform = self._detect_platform(url)
                    print(f"Adding task {i+1}/{total_urls}: {platform}")

                    # 添加下载任务
                    task_id = self.downloader.add_task(url, str(downloads_dir), audio_only=audio_only)
                    task_ids.append(task_id)

                    # 开始下载（不等待完成）
                    future = self.downloader.start_download(task_id)
                    futures.append((task_id, future, url))

                    # 小延迟避免过快启动
                    time.sleep(0.2)

                except Exception as e:
                    print(f"Failed to add task {i+1}: {e}")

            # 监控所有下载进度
            completed = 0
            failed = 0

            self.progress_updated.emit(
                f"Downloading {len(futures)} Videos...",
                10,
                "Concurrent downloads in progress..."
            )

            # 等待所有下载完成
            for i, (task_id, future, url) in enumerate(futures):
                if not self.is_downloading:
                    break

                # 等待暂停恢复
                while self.is_paused and self.is_downloading:
                    time.sleep(0.5)

                if not self.is_downloading:
                    break

                try:
                    # 等待这个任务完成
                    success = future.result(timeout=600)

                    if success:
                        completed += 1
                        print(f"✓ Completed {i+1}/{len(futures)}: {self._detect_platform(url)}")
                    else:
                        failed += 1
                        print(f"✗ Failed {i+1}/{len(futures)}: {self._detect_platform(url)}")

                except Exception as e:
                    failed += 1
                    print(f"✗ Error {i+1}/{len(futures)}: {e}")

                # 更新进度
                progress = 10 + ((i + 1) / len(futures)) * 80
                self.progress_updated.emit(
                    f"Progress {i+1}/{len(futures)}",
                    progress,
                    f"Completed: {completed}, Failed: {failed}"
                )

            # 最终结果
            if self.is_downloading:  # 没有被手动停止
                message = f"Concurrent download completed!\n\nSuccessful: {completed}\nFailed: {failed}\n\nAll downloads ran simultaneously!"
                self.download_completed.emit(completed > 0, message)

        except Exception as e:
            print(f"Concurrent download error: {e}")
            self.download_completed.emit(False, f"Concurrent download error: {str(e)}")

    def _on_download_progress(self, task_id: str, progress: float, speed: float):
        """下载进度回调（线程安全）- 增强版"""
        try:
            def update_progress():
                if self.is_downloading and not self.is_paused:
                    # 格式化速度显示
                    if speed > 0:
                        speed_mb = speed / 1024 / 1024
                        if speed_mb >= 1:
                            speed_text = f"{speed_mb:.1f} MB/s"
                        else:
                            speed_kb = speed / 1024
                            speed_text = f"{speed_kb:.1f} KB/s"
                    else:
                        speed_text = "Connecting..."

                    # 获取任务信息
                    title = "Downloading..."
                    if hasattr(self, 'downloader') and self.downloader:
                        task = self.downloader.get_task_status(task_id)
                        if task and hasattr(task, 'title') and task.title:
                            title = task.title[:35] + "..." if len(task.title) > 35 else task.title

                    # 确保进度在合理范围内
                    progress = max(0, min(100, progress))

                    # 添加下载阶段信息
                    if progress < 1:
                        detail = f"Initializing... | {speed_text}"
                    elif progress < 5:
                        detail = f"Starting download... | {speed_text}"
                    elif progress >= 99:
                        detail = f"Finalizing... | {speed_text}"
                    else:
                        detail = f"Downloading {progress:.1f}% | {speed_text}"

                    # 更新状态
                    self.update_status(title, progress, detail)

                    # 调试输出
                    print(f"Progress: {progress:.1f}% | Speed: {speed_text} | Task: {task_id[:8]}")

            # 在主线程中执行更新
            QTimer.singleShot(0, update_progress)

        except Exception as e:
            print(f"Progress callback error: {e}")

    def on_progress_updated(self, title: str, progress: float, detail: str):
        """处理进度更新信号（主线程）"""
        self.update_status(title, progress, detail)

    def on_download_completed(self, success: bool, message: str):
        """处理下载完成信号（主线程）"""
        # 重置UI状态
        self._update_ui_for_download_end()

        # 更新状态
        if success:
            self.update_status("Download Complete!", 100, "Files saved to downloads folder")
            QMessageBox.information(self, "Success", message)
        else:
            self.update_status("Download Failed", 0, "Check error details")
            QMessageBox.warning(self, "Error", message)

    def open_downloads_folder(self):
        """打开下载文件夹"""
        downloads_path = Path("./downloads")
        downloads_path.mkdir(exist_ok=True)

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
                f"Downloads are saved to:\n{downloads_path.absolute()}\n\nCould not open folder automatically: {e}"
            )


def main():
    """主函数"""
    print("🚀 Starting Perfect Apple GUI...")

    if not PYSIDE6_AVAILABLE:
        print("❌ PySide6 not available")
        return 1

    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Arina Video Downloader")
        app.setApplicationVersion("3.0")

        # 设置应用程序样式
        app.setStyle("Fusion")

        window = PerfectAppleDownloader()
        window.show()

        print("✅ Perfect Apple GUI started successfully!")
        return app.exec()

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
