#!/usr/bin/env python3
"""
High-Speed Download Optimizer
Implements best practices for video download acceleration
"""

import os
import sys
from pathlib import Path
from universal_downloader import DownloadManager


class SpeedOptimizer:
    """Download speed optimization utilities"""
    
    SPEED_PROFILES = {
        'conservative': {
            'concurrent_downloads': 2,
            'fragment_retries': 3,
            'socket_timeout': 30,
            'http_chunk_size': 1024*1024,  # 1MB
            'description': 'Safe and stable, good for slow connections'
        },
        'balanced': {
            'concurrent_downloads': 4,
            'fragment_retries': 5,
            'socket_timeout': 20,
            'http_chunk_size': 4*1024*1024,  # 4MB
            'description': 'Balanced speed and stability (recommended)'
        },
        'aggressive': {
            'concurrent_downloads': 8,
            'fragment_retries': 10,
            'socket_timeout': 15,
            'http_chunk_size': 8*1024*1024,  # 8MB
            'description': 'Maximum speed, may be unstable on slow connections'
        },
        'ultra': {
            'concurrent_downloads': 16,
            'fragment_retries': 15,
            'socket_timeout': 10,
            'http_chunk_size': 16*1024*1024,  # 16MB
            'description': 'Extreme speed for high-bandwidth connections'
        }
    }
    
    @classmethod
    def get_optimal_settings(cls, connection_speed: str = 'balanced') -> dict:
        """Get optimal yt-dlp settings for speed"""
        profile = cls.SPEED_PROFILES.get(connection_speed, cls.SPEED_PROFILES['balanced'])
        
        return {
            # Multi-threading and concurrency
            'concurrent_fragment_downloads': profile['concurrent_downloads'],
            'fragment_retries': profile['fragment_retries'],
            
            # Network optimization
            'socket_timeout': profile['socket_timeout'],
            'http_chunk_size': profile['http_chunk_size'],
            
            # Download optimization
            'retries': 10,
            'file_access_retries': 5,
            'extractor_retries': 3,
            
            # Buffer settings
            'buffersize': 64*1024,  # 64KB buffer
            
            # Connection settings
            'keepalive': True,
            
            # Format optimization
            'prefer_free_formats': False,  # Prefer quality over format
            'merge_output_format': 'mp4',
            
            # Additional speed optimizations
            'no_check_certificates': True,  # Skip SSL verification for speed
            'geo_bypass': True,  # Bypass geo-restrictions
            
            # Playlist optimization
            'lazy_playlist': True,  # Don't load entire playlist at once
        }
    
    @classmethod
    def detect_optimal_profile(cls) -> str:
        """Auto-detect optimal speed profile based on system"""
        try:
            import psutil
            
            # Check available memory
            memory_gb = psutil.virtual_memory().total / (1024**3)
            
            # Check CPU cores
            cpu_cores = psutil.cpu_count(logical=True)
            
            # Simple heuristic for profile selection
            if memory_gb >= 8 and cpu_cores >= 8:
                return 'aggressive'
            elif memory_gb >= 4 and cpu_cores >= 4:
                return 'balanced'
            else:
                return 'conservative'
                
        except ImportError:
            return 'balanced'  # Safe default


class HighSpeedDownloader(DownloadManager):
    """Enhanced downloader with speed optimization"""
    
    def __init__(self, speed_profile: str = 'auto', **kwargs):
        super().__init__(**kwargs)
        
        if speed_profile == 'auto':
            speed_profile = SpeedOptimizer.detect_optimal_profile()
        
        self.speed_profile = speed_profile
        self.speed_settings = SpeedOptimizer.get_optimal_settings(speed_profile)
        
        # Update extractor with speed settings
        self._apply_speed_optimizations()
        
        print(f"Speed optimization enabled: {speed_profile}")
        print(f"Profile: {SpeedOptimizer.SPEED_PROFILES[speed_profile]['description']}")
    
    def _apply_speed_optimizations(self):
        """Apply speed optimizations to extractor"""
        # Store original download method
        original_download = self.extractor.download
        
        def optimized_download(task, progress_callback=None):
            """Download with speed optimizations"""
            
            # Enhanced progress callback with speed tracking
            def enhanced_progress_hook(d):
                if progress_callback and d['status'] == 'downloading':
                    if 'total_bytes' in d:
                        progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                        speed = d.get('speed', 0)
                        
                        # Always call progress callback, even if speed is 0
                        progress_callback(task.task_id, progress, speed)
                        
                        # Enhanced speed display
                        if speed > 0:
                            speed_mb = speed / 1024 / 1024
                            eta = d.get('eta', 0)
                            eta_str = f"ETA: {eta}s" if eta else ""
                            
                            # Print detailed speed info
                            if hasattr(self, '_last_speed_update'):
                                import time
                                if time.time() - self._last_speed_update > 2:  # Update every 2 seconds
                                    print(f"\r  Speed: {speed_mb:.1f} MB/s | {eta_str} | Threads: {self.speed_settings['concurrent_fragment_downloads']}", end='')
                                    self._last_speed_update = time.time()
                            else:
                                import time
                                self._last_speed_update = time.time()
                        else:
                            # Still show progress even without speed
                            print(f"\r  Progress: {progress:.1f}%", end='')
                    elif '_percent_str' in d and progress_callback:
                        # Fallback for percentage-only progress
                        try:
                            percent_str = d['_percent_str'].strip()
                            if '%' in percent_str:
                                progress = float(percent_str.replace('%', ''))
                                speed = d.get('speed', 0)
                                progress_callback(task.task_id, progress, speed)
                                print(f"\r  Progress: {progress:.1f}%", end='')
                        except:
                            pass
            
            # Set output template with speed-optimized naming
            output_template = str(Path(task.output_dir) / '%(title)s.%(ext)s')
            
            # Build optimized yt-dlp options
            ydl_opts = {
                'outtmpl': output_template,
                'format': self._get_speed_optimized_format(task),
                'noplaylist': True,
                'progress_hooks': [enhanced_progress_hook],
                **self.speed_settings  # Apply all speed optimizations
            }
            
            # Platform-specific optimizations
            from universal_downloader import PlatformDetector
            platform = PlatformDetector.detect_platform(task.url)
            
            if platform == 'pornhub':
                ydl_opts.update({
                    'age_limit': 18,
                    # PornHub-specific speed opts
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                })
                
                # Use cookies if available
                if platform in self.extractor.cookies_files:
                    ydl_opts['cookiefile'] = self.extractor.cookies_files[platform]
                    print(f"Using cookies for {platform}: {self.extractor.cookies_files[platform]}")
            
            # Execute optimized download
            with self.extractor.yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    print(f"\nStarting optimized download with {self.speed_settings['concurrent_fragment_downloads']} threads...")
                    ydl.download([task.url])
                    return True
                except Exception as e:
                    task.error_message = str(e)
                    return False
        
        # Replace extractor download method
        self.extractor.download = optimized_download
    
    def _get_speed_optimized_format(self, task):
        """Get format string optimized for speed"""
        if task.audio_only:
            # For audio, prefer formats that download faster
            return 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio'
        else:
            if task.quality == 'best':
                # Prefer MP4 for faster download/processing
                return 'best[ext=mp4]/best[height<=1080]/best'
            elif task.quality == 'worst':
                return 'worst[ext=mp4]/worst'
            else:
                # Quality-specific with MP4 preference
                return f'best[height<={task.quality}][ext=mp4]/best[height<={task.quality}]/best'
    
    def benchmark_speed(self, test_url: str = None) -> dict:
        """Benchmark download speed"""
        if not test_url:
            # Use a known fast test video
            test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll (small file)
        
        print("Running speed benchmark...")
        
        import time
        start_time = time.time()
        
        try:
            task_id = self.add_task(test_url, "./benchmark", quality="worst")  # Fastest download
            future = self.start_download(task_id)
            success = future.result()
            
            end_time = time.time()
            duration = end_time - start_time
            
            if success:
                return {
                    'success': True,
                    'duration': duration,
                    'profile': self.speed_profile,
                    'settings': self.speed_settings
                }
            else:
                return {'success': False, 'error': 'Download failed'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}


def create_speed_optimized_downloader(profile: str = 'auto') -> HighSpeedDownloader:
    """Create speed-optimized downloader"""
    return HighSpeedDownloader(speed_profile=profile, max_workers=8)


if __name__ == '__main__':
    # Demo speed optimization
    print("High-Speed Download Optimizer")
    print("=" * 50)
    
    print("\nAvailable speed profiles:")
    for name, config in SpeedOptimizer.SPEED_PROFILES.items():
        print(f"  {name:>12}: {config['description']}")
    
    print(f"\nAuto-detected optimal profile: {SpeedOptimizer.detect_optimal_profile()}")
    
    # Test speed settings
    settings = SpeedOptimizer.get_optimal_settings('aggressive')
    print(f"\nSample aggressive settings:")
    for key, value in settings.items():
        print(f"  {key}: {value}")