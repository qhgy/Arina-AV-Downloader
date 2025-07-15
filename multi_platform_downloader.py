#!/usr/bin/env python3
"""
通用多平台视频下载器 - 增强版
基于yt-dlp，支持多个视频平台的统一下载管理
参考Hitomi-Downloader的架构设计
"""

import os
import sys
import json
import threading
import queue
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from enum import Enum


@dataclass
class DownloadTask:
    """下载任务数据类"""
    url: str
    output_dir: str
    quality: str = 'best'
    format_type: str = 'mp4'
    audio_only: bool = False
    task_id: str = None
    platform: str = None
    title: str = ""
    status: str = "pending"  # pending, downloading, completed, failed
    progress: float = 0.0
    file_path: str = ""
    error_message: str = ""
    
    def __post_init__(self):
        if not self.task_id:
            self.task_id = f"{int(time.time())}_{hash(self.url) % 10000}"


class DownloadStatus(Enum):
    """下载状态枚举"""
    PENDING = "pending"
    DOWNLOADING = "downloading" 
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class PlatformDetector:
    """平台检测器"""
    
    PLATFORM_PATTERNS = {
        'youtube': ['youtube.com', 'youtu.be', 'm.youtube.com'],
        'pornhub': ['pornhub.com', 'rt.pornhub.com', 'www.pornhub.com'],
        'twitter': ['twitter.com', 'x.com', 't.co'],
        'instagram': ['instagram.com', 'www.instagram.com'],
        'tiktok': ['tiktok.com', 'www.tiktok.com'],
        'bilibili': ['bilibili.com', 'www.bilibili.com', 'b23.tv'],
        'twitch': ['twitch.tv', 'www.twitch.tv'],
        'generic': []  # 通用处理
    }
    
    @classmethod
    def detect_platform(cls, url: str) -> str:
        """检测URL所属平台"""
        url_lower = url.lower()
        
        for platform, patterns in cls.PLATFORM_PATTERNS.items():
            if platform == 'generic':
                continue
            for pattern in patterns:
                if pattern in url_lower:
                    return platform
        
        return 'generic'


class BaseExtractor:
    """基础提取器类"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        
    def extract_info(self, url: str) -> Dict[str, Any]:
        """提取视频信息"""
        raise NotImplementedError
        
    def download(self, task: DownloadTask, progress_callback=None) -> bool:
        """下载视频"""
        raise NotImplementedError


class YtDlpExtractor(BaseExtractor):
    """基于yt-dlp的通用提取器"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self._check_dependencies()
        
    def _check_dependencies(self):
        """检查yt-dlp依赖"""
        try:
            import yt_dlp
            self.yt_dlp = yt_dlp
        except ImportError:
            print("正在安装 yt-dlp...")
            import subprocess
            subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)
            import yt_dlp
            self.yt_dlp = yt_dlp
    
    def extract_info(self, url: str) -> Dict[str, Any]:
        """提取视频信息"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with self.yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'formats': info.get('formats', []),
                    'thumbnail': info.get('thumbnail', ''),
                    'description': info.get('description', ''),
                    'upload_date': info.get('upload_date', ''),
                    'platform': PlatformDetector.detect_platform(url)
                }
            except Exception as e:
                raise Exception(f"信息提取失败: {str(e)}")
    
    def download(self, task: DownloadTask, progress_callback=None) -> bool:
        """下载视频"""
        def progress_hook(d):
            if progress_callback and d['status'] == 'downloading':
                if 'total_bytes' in d:
                    progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                    progress_callback(task.task_id, progress, d.get('speed', 0))
        
        # 设置输出模板
        output_template = str(Path(task.output_dir) / '%(title)s.%(ext)s')
        
        # 根据平台和需求调整格式选择器
        if task.audio_only:
            format_selector = 'bestaudio/best'
            postprocessors = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            if task.quality == 'best':
                format_selector = f'best[ext={task.format_type}]/best'
            elif task.quality == 'worst':
                format_selector = f'worst[ext={task.format_type}]/worst'
            else:
                format_selector = f'best[height<={task.quality}][ext={task.format_type}]/best[height<={task.quality}]/best'
            postprocessors = []
        
        ydl_opts = {
            'outtmpl': output_template,
            'format': format_selector,
            'noplaylist': True,
            'progress_hooks': [progress_hook],
            'postprocessors': postprocessors,
        }
        
        # 平台特定配置
        platform = PlatformDetector.detect_platform(task.url)
        if platform == 'pornhub':
            # PornHub特定配置
            ydl_opts.update({
                'age_limit': 18,
                'cookiesfrombrowser': ('chrome', ),  # 使用浏览器cookie
            })
        
        with self.yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([task.url])
                return True
            except Exception as e:
                task.error_message = str(e)
                return False


class DownloadManager:
    """下载管理器"""
    
    def __init__(self, max_workers: int = 4, config_file: str = None):
        self.max_workers = max_workers
        self.config_file = config_file or "downloader_config.json"
        self.tasks: Dict[str, DownloadTask] = {}
        self.download_queue = queue.Queue()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.running = False
        self.progress_callbacks = []
        
        # 加载配置
        self.config = self._load_config()
        
        # 初始化提取器
        self.extractor = YtDlpExtractor(self.config)
        
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # 默认配置
        default_config = {
            'max_workers': self.max_workers,
            'default_output_dir': './downloads',
            'default_quality': 'best',
            'default_format': 'mp4',
            'platforms': {
                'youtube': {
                    'enabled': True,
                    'quality_preference': ['1080', '720', 'best'],
                },
                'pornhub': {
                    'enabled': True,
                    'quality_preference': ['720', 'best'],
                    'age_verification': True,
                },
                'generic': {
                    'enabled': True,
                }
            }
        }
        
        self._save_config(default_config)
        return default_config
    
    def _save_config(self, config: Dict[str, Any]):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"配置保存失败: {e}")
    
    def add_progress_callback(self, callback):
        """添加进度回调函数"""
        self.progress_callbacks.append(callback)
    
    def _notify_progress(self, task_id: str, progress: float, speed: float = 0):
        """通知进度更新"""
        if task_id in self.tasks:
            self.tasks[task_id].progress = progress
            
        for callback in self.progress_callbacks:
            try:
                callback(task_id, progress, speed)
            except Exception:
                pass
    
    def add_task(self, url: str, output_dir: str = None, **kwargs) -> str:
        """添加下载任务"""
        output_dir = output_dir or self.config.get('default_output_dir', './downloads')
        
        task = DownloadTask(
            url=url,
            output_dir=output_dir,
            quality=kwargs.get('quality', self.config.get('default_quality', 'best')),
            format_type=kwargs.get('format_type', self.config.get('default_format', 'mp4')),
            audio_only=kwargs.get('audio_only', False)
        )
        
        # 检测平台
        task.platform = PlatformDetector.detect_platform(url)
        
        # 检查平台是否启用
        platform_config = self.config.get('platforms', {}).get(task.platform, {})
        if not platform_config.get('enabled', True):
            raise Exception(f"平台 {task.platform} 已禁用")
        
        # 提取基本信息
        try:
            info = self.extractor.extract_info(url)
            task.title = info.get('title', 'Unknown')
        except Exception as e:
            print(f"信息提取失败: {e}")
        
        self.tasks[task.task_id] = task
        return task.task_id
    
    def start_download(self, task_id: str):
        """开始下载任务"""
        if task_id not in self.tasks:
            raise ValueError(f"任务 {task_id} 不存在")
        
        task = self.tasks[task_id]
        task.status = DownloadStatus.DOWNLOADING.value
        
        # 创建输出目录
        os.makedirs(task.output_dir, exist_ok=True)
        
        # 提交到线程池
        future = self.executor.submit(self._download_task, task)
        return future
    
    def _download_task(self, task: DownloadTask):
        """执行下载任务"""
        try:
            success = self.extractor.download(task, self._notify_progress)
            if success:
                task.status = DownloadStatus.COMPLETED.value
                task.progress = 100.0
            else:
                task.status = DownloadStatus.FAILED.value
            return success
        except Exception as e:
            task.status = DownloadStatus.FAILED.value
            task.error_message = str(e)
            return False
    
    def get_task_status(self, task_id: str) -> Optional[DownloadTask]:
        """获取任务状态"""
        return self.tasks.get(task_id)
    
    def list_tasks(self) -> List[DownloadTask]:
        """列出所有任务"""
        return list(self.tasks.values())
    
    def remove_task(self, task_id: str):
        """移除任务"""
        if task_id in self.tasks:
            del self.tasks[task_id]
    
    def get_supported_platforms(self) -> List[str]:
        """获取支持的平台列表"""
        return list(PlatformDetector.PLATFORM_PATTERNS.keys())
    
    def shutdown(self):
        """关闭下载管理器"""
        self.executor.shutdown(wait=True)


# 便捷函数
def create_download_manager(max_workers: int = 4) -> DownloadManager:
    """创建下载管理器实例"""
    return DownloadManager(max_workers=max_workers)


def quick_download(url: str, output_dir: str = './downloads', **kwargs) -> bool:
    """快速下载函数"""
    manager = create_download_manager()
    
    try:
        task_id = manager.add_task(url, output_dir, **kwargs)
        future = manager.start_download(task_id)
        return future.result()  # 等待完成
    except Exception as e:
        print(f"下载失败: {e}")
        return False
    finally:
        manager.shutdown()


if __name__ == '__main__':
    # 测试代码
    print("🌸 多平台视频下载器 - 核心模块")
    print("支持的平台:", PlatformDetector.PLATFORM_PATTERNS.keys())
    
    # 测试平台检测
    test_urls = [
        "https://www.youtube.com/watch?v=test",
        "https://www.pornhub.com/view_video.php?viewkey=test",
        "https://twitter.com/user/status/123"
    ]
    
    for url in test_urls:
        platform = PlatformDetector.detect_platform(url)
        print(f"URL: {url} -> 平台: {platform}")