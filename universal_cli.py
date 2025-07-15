#!/usr/bin/env python3
"""
Universal Multi-Platform Video Downloader - Command Line Interface
Enhanced version supporting YouTube, PornHub and other platforms
"""

import os
import sys
import argparse
import json
import time
import threading
from pathlib import Path
from universal_downloader import DownloadManager, DownloadTask, PlatformDetector


class DownloadCLI:
    """Command line interface class"""
    
    def __init__(self):
        self.manager = DownloadManager(max_workers=4)
        self.manager.add_progress_callback(self._progress_callback)
        self.active_downloads = {}
        
    def _progress_callback(self, task_id: str, progress: float, speed: float):
        """Progress callback function"""
        if task_id in self.active_downloads:
            task = self.manager.get_task_status(task_id)
            if task:
                # Simple progress display
                bar_length = 30
                filled_length = int(bar_length * progress / 100)
                bar = '█' * filled_length + '░' * (bar_length - filled_length)
                
                speed_str = f"{speed/1024/1024:.1f} MB/s" if speed > 0 else "calculating..."
                
                print(f"\r[{task_id[:8]}] {task.title[:40]:<40} [{bar}] {progress:.1f}% {speed_str}", 
                      end='', flush=True)
                
                if progress >= 100:
                    print()  # New line
                    if task_id in self.active_downloads:
                        del self.active_downloads[task_id]
    
    def download_single(self, url: str, output_dir: str = None, **kwargs):
        """Download single video"""
        try:
            # Detect platform
            platform = PlatformDetector.detect_platform(url)
            print(f"Detected platform: {platform}")
            
            # Add task
            task_id = self.manager.add_task(url, output_dir, **kwargs)
            task = self.manager.get_task_status(task_id)
            
            print(f"Preparing download: {task.title}")
            print(f"Output directory: {task.output_dir}")
            print(f"Quality setting: {task.quality}")
            
            if kwargs.get('info_only', False):
                self._show_video_info(task)
                return True
            
            # Start download
            self.active_downloads[task_id] = True
            future = self.manager.start_download(task_id)
            
            # Wait for completion
            success = future.result()
            
            if success:
                print(f"Download completed: {task.title}")
                return True
            else:
                print(f"Download failed: {task.error_message}")
                return False
                
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
    
    def download_batch(self, urls: list, output_dir: str = None, **kwargs):
        """Batch download"""
        print(f"Batch downloading {len(urls)} links")
        
        futures = []
        task_ids = []
        
        for i, url in enumerate(urls, 1):
            try:
                platform = PlatformDetector.detect_platform(url)
                print(f"[{i}/{len(urls)}] Platform: {platform} - {url[:50]}...")
                
                task_id = self.manager.add_task(url, output_dir, **kwargs)
                task_ids.append(task_id)
                self.active_downloads[task_id] = True
                
                future = self.manager.start_download(task_id)
                futures.append((task_id, future))
                
                # Small delay to avoid rapid starts
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Task {i} failed to add: {e}")
        
        # Wait for all tasks to complete
        completed = 0
        failed = 0
        
        for task_id, future in futures:
            try:
                success = future.result()
                if success:
                    completed += 1
                else:
                    failed += 1
            except Exception:
                failed += 1
        
        print(f"\nBatch download results: {completed} succeeded, {failed} failed")
    
    def _show_video_info(self, task: DownloadTask):
        """Show video information"""
        try:
            info = self.manager.extractor.extract_info(task.url)
            
            print(f"\nVideo Information:")
            print(f"  Title: {info.get('title', 'Unknown')}")
            print(f"  Uploader: {info.get('uploader', 'Unknown')}")
            print(f"  Duration: {info.get('duration', 0)} seconds")
            print(f"  View count: {info.get('view_count', 0):,}")
            print(f"  Platform: {info.get('platform', 'Unknown')}")
            print(f"  Upload date: {info.get('upload_date', 'Unknown')}")
            
            # Show available formats
            formats = info.get('formats', [])
            if formats:
                print(f"\nAvailable formats (showing last 10):")
                for fmt in formats[-10:]:
                    ext = fmt.get('ext', 'unknown')
                    height = fmt.get('height', 'audio')
                    filesize = fmt.get('filesize', 0)
                    size_mb = f"{filesize/1024/1024:.1f}MB" if filesize else "unknown"
                    
                    print(f"  ID: {fmt.get('format_id', 'N/A'):>8} | "
                          f"Format: {ext:>4} | "
                          f"Resolution: {str(height):>6} | "
                          f"Size: {size_mb:>10}")
                          
        except Exception as e:
            print(f"Failed to get video info: {e}")
    
    def list_supported_platforms(self):
        """List supported platforms"""
        platforms = self.manager.get_supported_platforms()
        
        print("Supported platforms:")
        for platform in platforms:
            if platform == 'generic':
                print(f"  {platform:>12}: Generic platform (all other websites)")
            else:
                patterns = PlatformDetector.PLATFORM_PATTERNS.get(platform, [])
                domains = ', '.join(patterns[:3])  # Show first 3 domains
                if len(patterns) > 3:
                    domains += f" (+{len(patterns)-3} more)"
                print(f"  {platform:>12}: {domains}")
    
    def show_config(self):
        """Show current configuration"""
        config = self.manager.config
        
        print("Current configuration:")
        print(f"  Max workers: {config.get('max_workers', 4)}")
        print(f"  Default output: {config.get('default_output_dir', './downloads')}")
        print(f"  Default quality: {config.get('default_quality', 'best')}")
        print(f"  Default format: {config.get('default_format', 'mp4')}")
        
        print("\nPlatform settings:")
        platforms = config.get('platforms', {})
        for platform, settings in platforms.items():
            status = "Enabled" if settings.get('enabled', True) else "Disabled"
            print(f"  {platform:>12}: {status}")
    
    def shutdown(self):
        """Shutdown resources"""
        self.manager.shutdown()


def main():
    parser = argparse.ArgumentParser(
        description='Universal Multi-Platform Video Downloader - Supports YouTube, PornHub and other platforms',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  %(prog)s "https://youtube.com/watch?v=..." 
  %(prog)s -a "https://pornhub.com/view_video.php?viewkey=..."
  %(prog)s -q 720 -o "D:/Videos" "URL"
  %(prog)s -b urls.txt
  %(prog)s --platforms
        """
    )
    
    # Basic arguments
    parser.add_argument('url', nargs='?', help='Video URL')
    parser.add_argument('-o', '--output', default='./downloads', 
                       help='Output directory (default: ./downloads)')
    parser.add_argument('-q', '--quality', default='best',
                       help='Video quality: best, worst, 720, 1080, etc (default: best)')
    parser.add_argument('-f', '--format', default='mp4', 
                       help='Video format (default: mp4)')
    
    # Feature options
    parser.add_argument('-a', '--audio', action='store_true',
                       help='Download audio only')
    parser.add_argument('-i', '--info', action='store_true', 
                       help='Show video information only, do not download')
    parser.add_argument('-b', '--batch', 
                       help='Batch download, specify file containing URLs')
    
    # System options
    parser.add_argument('--platforms', action='store_true',
                       help='Show supported platforms list')
    parser.add_argument('--config', action='store_true',
                       help='Show current configuration')
    parser.add_argument('--max-workers', type=int, default=4,
                       help='Maximum concurrent downloads (default: 4)')
    
    args = parser.parse_args()
    
    # Initialize CLI
    cli = DownloadCLI()
    cli.manager.max_workers = args.max_workers
    
    try:
        print("Universal Multi-Platform Video Downloader v2.0")
        print("Supports technology-neutral video content downloading")
        print("=" * 50)
        
        if args.platforms:
            cli.list_supported_platforms()
            return
            
        if args.config:
            cli.show_config()
            return
            
        if args.batch:
            # Batch download
            if not os.path.exists(args.batch):
                print(f"File not found: {args.batch}")
                return
                
            with open(args.batch, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            if not urls:
                print("No valid URLs found")
                return
                
            cli.download_batch(urls, args.output, 
                             quality=args.quality,
                             format_type=args.format,
                             audio_only=args.audio)
        
        elif args.url:
            # Single download
            success = cli.download_single(args.url, args.output,
                                        quality=args.quality,
                                        format_type=args.format,
                                        audio_only=args.audio,
                                        info_only=args.info)
            sys.exit(0 if success else 1)
        
        else:
            # Show help
            parser.print_help()
            
    except KeyboardInterrupt:
        print("\nDownload cancelled")
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
    finally:
        cli.shutdown()


if __name__ == '__main__':
    main()