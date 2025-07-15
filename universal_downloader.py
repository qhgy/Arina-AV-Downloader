#!/usr/bin/env python3
"""
Universal Multi-Platform Video Downloader - Enhanced Version
Based on yt-dlp, supports multiple video platforms with unified download management
Architecture inspired by Hitomi-Downloader
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
    """Download task data class"""
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
    """Download status enum"""
    PENDING = "pending"
    DOWNLOADING = "downloading" 
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class PlatformDetector:
    """Platform detection utility"""
    
    PLATFORM_PATTERNS = {
        'youtube': ['youtube.com', 'youtu.be', 'm.youtube.com'],
        'pornhub': ['pornhub.com', 'rt.pornhub.com', 'www.pornhub.com'],
        'twitter': ['twitter.com', 'x.com', 't.co'],
        'instagram': ['instagram.com', 'www.instagram.com'],
        'tiktok': ['tiktok.com', 'www.tiktok.com'],
        'bilibili': ['bilibili.com', 'www.bilibili.com', 'b23.tv'],
        'twitch': ['twitch.tv', 'www.twitch.tv'],
        'generic': []  # Generic handler
    }
    
    @classmethod
    def detect_platform(cls, url: str) -> str:
        """Detect platform from URL"""
        url_lower = url.lower()
        
        for platform, patterns in cls.PLATFORM_PATTERNS.items():
            if platform == 'generic':
                continue
            for pattern in patterns:
                if pattern in url_lower:
                    return platform
        
        return 'generic'


class BaseExtractor:
    """Base extractor class"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        
    def extract_info(self, url: str) -> Dict[str, Any]:
        """Extract video information"""
        raise NotImplementedError
        
    def download(self, task: DownloadTask, progress_callback=None) -> bool:
        """Download video"""
        raise NotImplementedError


class YtDlpExtractor(BaseExtractor):
    """yt-dlp based universal extractor"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)

        # 并发下载配置
        self.concurrent_fragments = self.config.get('concurrent_fragments', 4)
        self.fragment_retries = self.config.get('fragment_retries', 10)
        self.chunk_size = self.config.get('http_chunk_size', 10485760)  # 10MB

        self._check_dependencies()
        self._setup_cookies()
        
    def _check_dependencies(self):
        """Check yt-dlp dependencies"""
        try:
            import yt_dlp
            self.yt_dlp = yt_dlp
        except ImportError:
            print("Installing yt-dlp...")
            import subprocess
            subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)
            import yt_dlp
            self.yt_dlp = yt_dlp
    
    def _setup_cookies(self):
        """Setup cookies for authentication"""
        self.cookies_files = {}
        
        # 使用可移植路径管理器
        try:
            from portable.path_manager import PathManager
            path_manager = PathManager(silent=True)
            cookies_dir = path_manager.resolve_relative_path('./cookies')
        except ImportError:
            # 回退到原始方式
            cookies_dir = Path('./cookies')
            
        if cookies_dir.exists():
            for file in cookies_dir.glob("*_cookies.txt"):
                platform = file.stem.replace("_cookies", "")
                self.cookies_files[platform] = str(file)
    
    def extract_info(self, url: str) -> Dict[str, Any]:
        """Extract video information"""
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
                raise Exception(f"Info extraction failed: {str(e)}")
    
    def download(self, task: DownloadTask, progress_callback=None) -> bool:
        """Download video"""
        def progress_hook(d):
            if progress_callback and d['status'] == 'downloading':
                if 'total_bytes' in d:
                    progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                    progress_callback(task.task_id, progress, d.get('speed', 0))
        
        # Set output template
        output_template = str(Path(task.output_dir) / '%(title)s.%(ext)s')
        
        # Adjust format selector based on platform and requirements
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
            # 并发分片下载优化
            'concurrent_fragment_downloads': self.concurrent_fragments,
            'fragment_retries': self.fragment_retries,
            'http_chunk_size': self.chunk_size,
            # 额外的性能优化
            'socket_timeout': 30,  # 30秒超时
            'retries': 10,  # 总重试次数
        }
        
        # Platform-specific configuration
        platform = PlatformDetector.detect_platform(task.url)

        # 根据平台调整并发设置
        platform_config = self.config.get('platforms', {}).get(platform, {})
        if 'concurrent_fragments' in platform_config:
            ydl_opts['concurrent_fragment_downloads'] = platform_config['concurrent_fragments']
            print(f"🚀 Using {platform_config['concurrent_fragments']} concurrent fragments for {platform}")
        
        # Add cookies if available
        if platform in self.cookies_files:
            ydl_opts['cookiefile'] = self.cookies_files[platform]
            print(f"Using cookies for {platform}: {self.cookies_files[platform]}")
        
        if platform == 'pornhub':
            # PornHub specific config
            ydl_opts.update({
                'age_limit': 18,
            })
            # Don't use cookiesfrombrowser if we have cookies file
            if platform not in self.cookies_files:
                ydl_opts['cookiesfrombrowser'] = ('chrome', )
        
        with self.yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([task.url])
                return True
            except Exception as e:
                task.error_message = str(e)
                return False


class DownloadManager:
    """Download manager with multi-threading support"""
    
    def __init__(self, max_workers: int = 4, config_file: str = None):
        self.max_workers = max_workers
        self.config_file = config_file or "downloader_config.json"
        self.tasks: Dict[str, DownloadTask] = {}
        self.download_queue = queue.Queue()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.running = False
        self.progress_callbacks = []
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize extractor
        self.extractor = YtDlpExtractor(self.config)
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration file"""
        # 使用可移植配置管理器
        try:
            from portable.config_manager import ConfigManager
            config_manager = ConfigManager(silent=True)
            return config_manager.load_config(self.config_file)
        except ImportError:
            # 回退到原始方式
            if os.path.exists(self.config_file):
                try:
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception:
                    pass
            
            # Default configuration
            default_config = {
                'max_workers': self.max_workers,
                'default_output_dir': './downloads',
                'default_quality': 'best',
                'default_format': 'mp4',
                # 并发下载优化配置
                'concurrent_fragments': 4,  # 并发片段数量
                'fragment_retries': 10,  # 片段重试次数
                'http_chunk_size': 10485760,  # 10MB chunk size
                'platforms': {
                    'youtube': {
                        'enabled': True,
                        'quality_preference': ['1080', '720', 'best'],
                        'concurrent_fragments': 6,  # YouTube可以更高并发
                    },
                    'pornhub': {
                        'enabled': True,
                        'quality_preference': ['720', 'best'],
                        'age_verification': True,
                        'concurrent_fragments': 4,  # PornHub适中并发
                    },
                    'generic': {
                        'enabled': True,
                        'concurrent_fragments': 3,  # 通用平台保守并发
                    }
                }
            }
            
            self._save_config(default_config)
            return default_config
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Config save failed: {e}")
    
    def add_progress_callback(self, callback):
        """Add progress callback function"""
        self.progress_callbacks.append(callback)
    
    def _notify_progress(self, task_id: str, progress: float, speed: float = 0):
        """Notify progress update"""
        if task_id in self.tasks:
            self.tasks[task_id].progress = progress
            
        for callback in self.progress_callbacks:
            try:
                callback(task_id, progress, speed)
            except Exception:
                pass
    
    def add_task(self, url: str, output_dir: str = None, **kwargs) -> str:
        """Add download task"""
        output_dir = output_dir or self.config.get('default_output_dir', './downloads')
        
        task = DownloadTask(
            url=url,
            output_dir=output_dir,
            quality=kwargs.get('quality', self.config.get('default_quality', 'best')),
            format_type=kwargs.get('format_type', self.config.get('default_format', 'mp4')),
            audio_only=kwargs.get('audio_only', False)
        )
        
        # Detect platform
        task.platform = PlatformDetector.detect_platform(url)
        
        # Check if platform is enabled
        platform_config = self.config.get('platforms', {}).get(task.platform, {})
        if not platform_config.get('enabled', True):
            raise Exception(f"Platform {task.platform} is disabled")
        
        # Extract basic information
        try:
            info = self.extractor.extract_info(url)
            task.title = info.get('title', 'Unknown')
        except Exception as e:
            print(f"Info extraction failed: {e}")
        
        self.tasks[task.task_id] = task
        return task.task_id
    
    def start_download(self, task_id: str):
        """Start download task"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} does not exist")
        
        task = self.tasks[task_id]
        task.status = DownloadStatus.DOWNLOADING.value
        
        # Create output directory
        os.makedirs(task.output_dir, exist_ok=True)
        
        # Submit to thread pool
        future = self.executor.submit(self._download_task, task)
        return future
    
    def _download_task(self, task: DownloadTask):
        """Execute download task"""
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
        """Get task status"""
        return self.tasks.get(task_id)
    
    def list_tasks(self) -> List[DownloadTask]:
        """List all tasks"""
        return list(self.tasks.values())
    
    def remove_task(self, task_id: str):
        """Remove task"""
        if task_id in self.tasks:
            del self.tasks[task_id]
    
    def get_supported_platforms(self) -> List[str]:
        """Get supported platforms list"""
        return list(PlatformDetector.PLATFORM_PATTERNS.keys())
    
    def shutdown(self):
        """Shutdown download manager"""
        self.executor.shutdown(wait=True)


# Convenience functions
def create_download_manager(max_workers: int = 4) -> DownloadManager:
    """Create download manager instance"""
    return DownloadManager(max_workers=max_workers)


def quick_download(url: str, output_dir: str = './downloads', **kwargs) -> bool:
    """Quick download function"""
    manager = create_download_manager()
    
    try:
        task_id = manager.add_task(url, output_dir, **kwargs)
        future = manager.start_download(task_id)
        return future.result()  # Wait for completion
    except Exception as e:
        print(f"Download failed: {e}")
        return False
    finally:
        manager.shutdown()


if __name__ == '__main__':
    # Test code
    print("Multi-Platform Video Downloader - Core Module")
    print("Supported platforms:", list(PlatformDetector.PLATFORM_PATTERNS.keys()))
    
    # Test platform detection
    test_urls = [
        "https://www.youtube.com/watch?v=test",
        "https://www.pornhub.com/view_video.php?viewkey=test",
        "https://twitter.com/user/status/123"
    ]
    
    for url in test_urls:
        platform = PlatformDetector.detect_platform(url)
        print(f"URL: {url} -> Platform: {platform}")