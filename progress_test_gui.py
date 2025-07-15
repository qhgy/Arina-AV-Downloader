#!/usr/bin/env python3
"""
Universal Video Downloader - Progress Test GUI
测试实时进度显示
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


class ProgressTestButton(QPushButton):
    """测试按钮"""
    
    def __init__(self, text: str, button_type: str = "secondary"):
        super().__init__(text)
        self.setMinimumHeight(36)
        self.setFont(QFont("Segoe UI", 11))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        if button_type == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #007AFF;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-weight: 600;
                    padding: 8px 16px;
                }
                QPushButton:hover { background-color: #0056CC; }
                QPushButton:disabled { background-color: #C7C7CC; color: #8E8E93; }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #FFFFFF;
                    border: 1px solid #D1D1D6;
                    border-radius: 10px;
                    color: #007AFF;
                    padding: 8px 16px;
                }
                QPushButton:hover { background-color: #F2F2F7; }
                QPushButton:disabled { background-color: #F2F2F7; color: #8E8E93; }
            """)


class ProgressTestDownloader(QMainWindow):
    """进度测试下载器"""
    
    # 信号定义
    progress_updated = Signal(str, float, str)
    download_completed = Signal(bool, str)
    
    def __init__(self):
        super().__init__()
        
        # 下载状态
        self.is_downloading = False
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
        """初始化下载器 - 增强版"""
        try:
            from universal_downloader import DownloadManager
            self.downloader = DownloadManager(max_workers=2)

            # 添加增强版进度回调
            self.downloader.add_progress_callback(self._on_download_progress)

            # 修补下载器的progress_hook以处理更多情况
            self._patch_downloader_progress_hook()

            self.downloader_available = True
            print("✅ Enhanced downloader initialized successfully")
        except Exception as e:
            print(f"❌ Downloader initialization failed: {e}")
            self.downloader = None
            self.downloader_available = False

    def _patch_downloader_progress_hook(self):
        """修补下载器的进度钩子以处理更多情况"""
        try:
            original_download = self.downloader.extractor.download

            def enhanced_download(task, progress_callback=None):
                """增强版下载函数"""
                def enhanced_progress_hook(d):
                    print(f"🔍 Progress hook called: status={d.get('status')}, keys={list(d.keys())}")

                    if progress_callback:
                        if d['status'] == 'downloading':
                            # 方法1: 使用total_bytes
                            if 'total_bytes' in d and d['total_bytes']:
                                progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                                speed = d.get('speed', 0)
                                print(f"📊 Method 1 - Progress: {progress:.1f}% | Speed: {speed}")
                                progress_callback(task.task_id, progress, speed)

                            # 方法2: 使用_percent_str
                            elif '_percent_str' in d:
                                try:
                                    percent_str = d['_percent_str'].strip()
                                    if '%' in percent_str:
                                        progress = float(percent_str.replace('%', ''))
                                        speed = d.get('speed', 0)
                                        print(f"📊 Method 2 - Progress: {progress:.1f}% | Speed: {speed}")
                                        progress_callback(task.task_id, progress, speed)
                                except:
                                    pass

                            # 方法3: 使用downloaded_bytes估算
                            elif 'downloaded_bytes' in d:
                                downloaded_mb = d['downloaded_bytes'] / 1024 / 1024
                                speed = d.get('speed', 0)
                                # 估算进度（基于下载量）
                                estimated_progress = min(downloaded_mb / 10 * 100, 95)  # 假设10MB = 95%
                                print(f"📊 Method 3 - Estimated: {estimated_progress:.1f}% | Downloaded: {downloaded_mb:.1f}MB")
                                progress_callback(task.task_id, estimated_progress, speed)

                            # 方法4: 至少显示活动状态
                            else:
                                speed = d.get('speed', 0)
                                print(f"📊 Method 4 - Unknown progress | Speed: {speed}")
                                # 显示一个动态进度（10-90之间循环）
                                import time
                                cycle_progress = (int(time.time()) % 80) + 10
                                progress_callback(task.task_id, cycle_progress, speed)

                        elif d['status'] == 'finished':
                            print("✅ Download finished!")
                            progress_callback(task.task_id, 100, 0)

                        elif d['status'] == 'error':
                            print("❌ Download error!")
                            progress_callback(task.task_id, 0, 0)

                # 调用原始下载函数，传递增强的进度回调
                return original_download(task, lambda task_id, progress, speed: enhanced_progress_hook({'status': 'downloading', 'downloaded_bytes': progress * 1024 * 1024, 'total_bytes': 100 * 1024 * 1024, 'speed': speed}))

            # 替换下载函数
            self.downloader.extractor.download = enhanced_download
            print("🔧 Progress hook patched successfully")

        except Exception as e:
            print(f"⚠️ Progress hook patch failed: {e}")
            # 如果修补失败，继续使用原始版本
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("Progress Test - Video Downloader")
        self.setMinimumSize(500, 400)
        self.resize(600, 450)
        
        # 设置背景
        self.setStyleSheet("QMainWindow { background-color: #F5F5F7; }")
        
        # 主窗口部件
        main_widget = QWidget()
        main_widget.setStyleSheet("background-color: #F5F5F7;")
        self.setCentralWidget(main_widget)
        
        # 主布局
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title = QLabel("🧪 Progress Test")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #1D1D1F; background-color: #F5F5F7;")
        
        # URL输入
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste a video URL to test real-time progress...")
        self.url_input.setFont(QFont("Segoe UI", 12))
        self.url_input.setMinimumHeight(40)
        self.url_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border: 2px solid #E5E5E7;
                border-radius: 10px;
                padding: 8px 12px;
                color: #1D1D1F;
            }
            QLineEdit:focus { border-color: #007AFF; }
        """)
        self.url_input.textChanged.connect(self.on_url_changed)
        
        # 状态显示
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
        self.status_title = QLabel("Ready for Progress Test")
        self.status_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Medium))
        self.status_title.setStyleSheet("color: #1D1D1F; background-color: transparent;")
        self.status_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 进度条 - 增强可见性
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(16)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #E5E5EA;
                border: 2px solid #D1D1D6;
                border-radius: 8px;
                text-align: center;
                color: #1D1D1F;
                font-size: 11px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #007AFF, stop:1 #5AC8FA);
                border-radius: 6px;
            }
        """)
        
        # 状态详情
        self.status_detail = QLabel("Enter URL and click Test Download")
        self.status_detail.setFont(QFont("Segoe UI", 11))
        self.status_detail.setStyleSheet("color: #86868B; background-color: transparent;")
        self.status_detail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        status_layout.addWidget(self.status_title)
        status_layout.addWidget(self.progress_bar)
        status_layout.addWidget(self.status_detail)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.test_btn = ProgressTestButton("🧪 Test Download", "primary")
        self.test_btn.setEnabled(False)
        self.test_btn.clicked.connect(self.test_download)

        self.force_btn = ProgressTestButton("🔄 Force Download", "primary")
        self.force_btn.setEnabled(False)
        self.force_btn.clicked.connect(self.force_download)

        self.fake_btn = ProgressTestButton("🎭 Fake Progress", "secondary")
        self.fake_btn.clicked.connect(self.fake_progress)

        self.stop_btn = ProgressTestButton("⏹️ Stop", "secondary")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_download)
        
        button_layout.addWidget(self.test_btn)
        button_layout.addWidget(self.force_btn)
        button_layout.addWidget(self.fake_btn)
        button_layout.addWidget(self.stop_btn)
        
        # 添加到布局
        layout.addWidget(title)
        layout.addWidget(self.url_input)
        layout.addWidget(status_widget)
        layout.addLayout(button_layout)
        layout.addStretch()
    
    def center_window(self):
        """居中窗口"""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def on_url_changed(self):
        """URL变化处理"""
        text = self.url_input.text().strip()
        has_url = bool(text) and self.downloader_available
        self.test_btn.setEnabled(has_url and not self.is_downloading)
        self.force_btn.setEnabled(has_url and not self.is_downloading)

        if has_url:
            self.update_status("Ready for Test", 0, "Test: normal | Force: ignore cache")
        else:
            self.update_status("Ready for Progress Test", 0, "Enter URL and click Test Download")
    
    def update_status(self, title: str, progress: float, detail: str):
        """更新状态显示"""
        self.status_title.setText(title)
        self.progress_bar.setValue(int(progress))
        self.status_detail.setText(detail)
    
    def test_download(self):
        """测试真实下载（可能使用缓存）"""
        self._start_download_test(force_redownload=False)

    def force_download(self):
        """强制重新下载（忽略缓存）"""
        self._start_download_test(force_redownload=True)

    def _start_download_test(self, force_redownload=False):
        """开始下载测试"""
        if not self.downloader_available:
            QMessageBox.warning(self, "Error", "Downloader not available")
            return

        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a URL")
            return

        self.is_downloading = True
        self.test_btn.setEnabled(False)
        self.force_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

        # 开始真实下载测试
        threading.Thread(target=self._real_download_test, args=(url, force_redownload), daemon=True).start()
    
    def fake_progress(self):
        """模拟进度测试"""
        self.is_downloading = True
        self.test_btn.setEnabled(False)
        self.fake_btn.setEnabled(False)
        self.force_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        # 开始模拟进度
        threading.Thread(target=self._fake_progress_test, daemon=True).start()
    
    def stop_download(self):
        """停止下载"""
        self.is_downloading = False
        has_url = bool(self.url_input.text().strip())
        self.test_btn.setEnabled(has_url)
        self.force_btn.setEnabled(has_url)
        self.fake_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.update_status("Stopped", 0, "Test stopped by user")
    
    def _real_download_test(self, url: str, force_redownload: bool = False):
        """增强版真实下载测试 - 支持强制重新下载"""
        try:
            downloads_dir = Path("./downloads")
            downloads_dir.mkdir(exist_ok=True)

            print(f"🚀 Starting download test | Force: {force_redownload} | URL: {url}")

            if force_redownload:
                self.progress_updated.emit("Force Download Mode", 0, "Will ignore existing files...")

                # 清理可能的缓存文件
                try:
                    potential_files = list(downloads_dir.glob("*.mp4")) + list(downloads_dir.glob("*.webm"))
                    if potential_files:
                        # 删除最新的文件
                        latest_file = max(potential_files, key=lambda f: f.stat().st_mtime)
                        print(f"🗑️ Removing for force download: {latest_file.name}")
                        latest_file.unlink()
                        self.progress_updated.emit("Preparing Force Download", 2, f"Removed: {latest_file.name}")
                except Exception as e:
                    print(f"File cleanup error: {e}")
            else:
                self.progress_updated.emit("Normal Download Mode", 0, "May use cached files...")

            # 添加下载任务
            print("📝 Adding download task...")
            task_id = self.downloader.add_task(url, str(downloads_dir))
            self.current_task_id = task_id
            print(f"✅ Task added: {task_id}")

            # 获取任务信息
            task = self.downloader.get_task_status(task_id)
            if task and task.title:
                print(f"📺 Video title: {task.title}")
                self.progress_updated.emit("Getting video info...", 2, f"Title: {task.title[:40]}...")

            # 开始下载
            print("⬇️ Starting download...")
            future = self.downloader.start_download(task_id)

            # 增强监控进度
            last_progress = 0
            stall_count = 0
            start_time = time.time()

            while not future.done() and self.is_downloading:
                task = self.downloader.get_task_status(task_id)
                if task:
                    current_progress = task.progress
                    elapsed = time.time() - start_time

                    # 检测进度是否停滞
                    if current_progress == last_progress:
                        stall_count += 1
                    else:
                        stall_count = 0
                        last_progress = current_progress

                    # 构建状态信息
                    if stall_count > 4:  # 2秒没有进度更新
                        detail = f"Progress: {current_progress:.1f}% | Stalled? | Time: {elapsed:.0f}s"
                    else:
                        detail = f"Progress: {current_progress:.1f}% | Active | Time: {elapsed:.0f}s"

                    title = f"Downloading: {task.title[:25]}..." if task.title else "Downloading..."

                    self.progress_updated.emit(title, current_progress, detail)
                    print(f"📊 Monitor: {current_progress:.1f}% | Stall: {stall_count} | Time: {elapsed:.0f}s")

                time.sleep(0.5)

            # 获取最终结果
            if self.is_downloading:
                print("⏳ Waiting for download completion...")
                success = future.result(timeout=10)
                elapsed = time.time() - start_time

                if success:
                    message = f"Real download test completed!\n\nTime taken: {elapsed:.1f} seconds"
                    print(f"✅ Download successful in {elapsed:.1f}s")
                    self.download_completed.emit(True, message)
                else:
                    message = f"Real download test failed!\n\nTime taken: {elapsed:.1f} seconds"
                    print(f"❌ Download failed after {elapsed:.1f}s")
                    self.download_completed.emit(False, message)

        except Exception as e:
            print(f"💥 Real download test error: {e}")
            self.download_completed.emit(False, f"Test error: {str(e)}")
    
    def _fake_progress_test(self):
        """模拟进度测试"""
        try:
            stages = [
                ("Connecting...", 0, "Initializing connection"),
                ("Getting info...", 5, "Fetching video information"),
                ("Starting download...", 10, "Beginning file transfer"),
            ]
            
            # 初始阶段
            for title, progress, detail in stages:
                if not self.is_downloading:
                    return
                self.progress_updated.emit(title, progress, detail)
                time.sleep(1)
            
            # 模拟下载进度
            for i in range(15, 101, 5):
                if not self.is_downloading:
                    return
                
                speed = 2.5 + (i / 100) * 3  # 模拟速度变化
                self.progress_updated.emit(
                    "Fake Video Download Test",
                    i,
                    f"Progress: {i}% | Speed: {speed:.1f} MB/s"
                )
                time.sleep(0.3)  # 快速更新
            
            if self.is_downloading:
                self.download_completed.emit(True, "Fake progress test completed!")
            
        except Exception as e:
            self.download_completed.emit(False, f"Fake test error: {str(e)}")
    
    def _on_download_progress(self, task_id: str, progress: float, speed: float):
        """增强版下载进度回调"""
        try:
            def update_ui():
                if self.is_downloading and task_id == self.current_task_id:
                    speed_mb = speed / 1024 / 1024 if speed > 0 else 0
                    speed_text = f"{speed_mb:.1f} MB/s" if speed_mb >= 0.1 else "Connecting..."

                    task = self.downloader.get_task_status(task_id)
                    title = "Real Download Progress"
                    if task and task.title:
                        title = task.title[:30] + "..." if len(task.title) > 30 else task.title

                    # 添加详细的阶段信息
                    if progress < 1:
                        detail = f"Initializing... | {speed_text}"
                    elif progress < 5:
                        detail = f"Starting download... | {speed_text}"
                    elif progress >= 99:
                        detail = f"Finalizing... | {speed_text}"
                    else:
                        detail = f"Real: {progress:.1f}% | {speed_text}"

                    self.update_status(title, progress, detail)
                    print(f"📊 Real progress: {progress:.1f}% | {speed_text} | Task: {task_id[:8]}")

            QTimer.singleShot(0, update_ui)
        except Exception as e:
            print(f"Progress callback error: {e}")
    
    def on_progress_updated(self, title: str, progress: float, detail: str):
        """处理进度更新信号"""
        self.update_status(title, progress, detail)
    
    def on_download_completed(self, success: bool, message: str):
        """处理下载完成信号"""
        self.is_downloading = False
        has_url = bool(self.url_input.text().strip())
        self.test_btn.setEnabled(has_url)
        self.force_btn.setEnabled(has_url)
        self.fake_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        if success:
            self.update_status("Test Complete!", 100, "All tests finished")
            QMessageBox.information(self, "Success", message)
        else:
            self.update_status("Test Failed", 0, "Check error details")
            QMessageBox.warning(self, "Error", message)


def main():
    """主函数"""
    print("🧪 Starting Progress Test GUI...")
    
    if not PYSIDE6_AVAILABLE:
        print("❌ PySide6 not available")
        return 1
    
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Progress Test")
        
        window = ProgressTestDownloader()
        window.show()
        
        print("✅ Progress Test GUI started!")
        return app.exec()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
