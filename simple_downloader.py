#!/usr/bin/env python3
"""
Universal Video Downloader - Apple-Style Simple Interface
Clean, elegant, and foolproof user experience
"""

import os
import sys
import time
import json
import threading
from pathlib import Path
from universal_downloader import DownloadManager, PlatformDetector
from speed_optimizer import HighSpeedDownloader, SpeedOptimizer


class SimpleDownloader:
    """Apple-style simple downloader interface"""
    
    def __init__(self):
        # Use high-speed downloader with auto-optimization
        self.manager = HighSpeedDownloader(speed_profile='auto', max_workers=4)
        self.manager.add_progress_callback(self._progress_callback)
        self.downloads_dir = Path('./downloads')
        self.downloads_dir.mkdir(exist_ok=True)
        self.current_downloads = {}
        
    def _progress_callback(self, task_id: str, progress: float, speed: float):
        """Clean progress display"""
        if task_id in self.current_downloads:
            task = self.manager.get_task_status(task_id)
            if task:
                # Clean progress bar
                bar_length = 40
                filled_length = int(bar_length * progress / 100)
                bar = '█' * filled_length + '░' * (bar_length - filled_length)
                
                speed_mb = speed / 1024 / 1024 if speed > 0 else 0
                
                print(f"\r  {bar} {progress:5.1f}%  {speed_mb:6.1f} MB/s", end='', flush=True)
                
                if progress >= 100:
                    print(f"\n  ✓ Download completed: {task.title}")
                    del self.current_downloads[task_id]
    
    def show_header(self):
        """Display clean header"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print("         Universal Video Downloader")
        print("           Simple • Fast • Clean")
        print("=" * 60)
        print()
    
    def show_main_menu(self):
        """Display main menu"""
        print("What would you like to do?")
        print()
        print("  1. Download Video")
        print("  2. Download Audio Only") 
        print("  3. Get Video Info")
        print("  4. Batch Download")
        print("  5. Settings")
        print("  6. Cookie Management")
        print("  7. Speed Optimization")
        print("  0. Exit")
        print()
        
    def get_user_choice(self, max_option: int) -> int:
        """Get user menu choice"""
        while True:
            try:
                choice = input(f"Choose option (0-{max_option}): ").strip()
                choice_num = int(choice)
                if 0 <= choice_num <= max_option:
                    return choice_num
                else:
                    print(f"Please enter a number between 0 and {max_option}")
            except ValueError:
                print("Please enter a valid number")
            except KeyboardInterrupt:
                return 0
    
    def get_url_input(self) -> str:
        """Get URL from user with smart detection"""
        print()
        print("Paste your video URL:")
        print("(Supports: YouTube, PornHub, Twitter, Instagram, TikTok, etc.)")
        print()
        
        while True:
            try:
                url = input("URL: ").strip()
                if not url:
                    print("Please enter a URL")
                    continue
                    
                if not (url.startswith('http://') or url.startswith('https://')):
                    print("Please enter a valid URL starting with http:// or https://")
                    continue
                    
                return url
            except KeyboardInterrupt:
                return ""
    
    def show_platform_info(self, url: str):
        """Show detected platform info"""
        platform = PlatformDetector.detect_platform(url)
        platform_display = {
            'youtube': 'YouTube',
            'pornhub': 'PornHub', 
            'twitter': 'Twitter/X',
            'instagram': 'Instagram',
            'tiktok': 'TikTok',
            'bilibili': 'Bilibili',
            'twitch': 'Twitch',
            'generic': 'Generic Platform'
        }
        
        print(f"\n  Platform detected: {platform_display.get(platform, platform)}")
        
    def download_video(self, url: str, audio_only: bool = False):
        """Download video with clean interface"""
        try:
            print("\n" + "─" * 60)
            self.show_platform_info(url)
            
            # Get video info first
            print("  Getting video information...")
            task_id = self.manager.add_task(url, str(self.downloads_dir), audio_only=audio_only)
            task = self.manager.get_task_status(task_id)
            
            print(f"  Title: {task.title}")
            print(f"  Output: {self.downloads_dir}")
            print(f"  Type: {'Audio Only' if audio_only else 'Video'}")
            print()
            
            # Confirm download
            confirm = input("Start download? (Y/n): ").strip().lower()
            if confirm and confirm != 'y' and confirm != 'yes':
                self.manager.remove_task(task_id)
                return False
            
            print("\n  Starting download...")
            self.current_downloads[task_id] = True
            
            future = self.manager.start_download(task_id)
            success = future.result()
            
            if success:
                print("  ✓ Download successful!")
                return True
            else:
                print(f"  ✗ Download failed: {task.error_message}")
                return False
                
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            return False
    
    def show_video_info(self, url: str):
        """Display video information"""
        try:
            print("\n" + "─" * 60)
            self.show_platform_info(url)
            print("  Getting video information...")
            
            info = self.manager.extractor.extract_info(url)
            
            print(f"\n  Title: {info.get('title', 'Unknown')}")
            print(f"  Uploader: {info.get('uploader', 'Unknown')}")
            
            duration = info.get('duration', 0)
            if duration:
                minutes, seconds = divmod(duration, 60)
                print(f"  Duration: {minutes:02d}:{seconds:02d}")
            
            view_count = info.get('view_count', 0)
            if view_count:
                print(f"  Views: {view_count:,}")
                
            upload_date = info.get('upload_date', '')
            if upload_date:
                try:
                    formatted_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
                    print(f"  Upload Date: {formatted_date}")
                except:
                    pass
            
            # Show available qualities
            formats = info.get('formats', [])
            if formats:
                print(f"\n  Available qualities:")
                qualities = set()
                for fmt in formats:
                    height = fmt.get('height')
                    if height:
                        qualities.add(f"{height}p")
                
                if qualities:
                    sorted_qualities = sorted(qualities, key=lambda x: int(x[:-1]), reverse=True)
                    print(f"    {', '.join(sorted_qualities[:5])}")  # Show top 5
                        
        except Exception as e:
            print(f"  ✗ Error getting info: {str(e)}")
    
    def batch_download(self):
        """Batch download interface"""
        print("\n" + "─" * 60)
        print("Batch Download")
        print()
        print("You can either:")
        print("  1. Enter URLs one by one (empty line to finish)")
        print("  2. Load from urls.txt file")
        print()
        
        choice = self.get_user_choice(2)
        
        if choice == 1:
            urls = []
            print("\nEnter URLs (empty line to finish):")
            while True:
                try:
                    url = input(f"URL {len(urls)+1}: ").strip()
                    if not url:
                        break
                    urls.append(url)
                except KeyboardInterrupt:
                    break
                    
        elif choice == 2:
            urls_file = Path('urls.txt')
            if not urls_file.exists():
                print("  ✗ urls.txt file not found")
                return
            
            with open(urls_file, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                
        else:
            return
        
        if not urls:
            print("  No URLs to download")
            return
            
        print(f"\n  Found {len(urls)} URLs to download")
        confirm = input("Start batch download? (Y/n): ").strip().lower()
        if confirm and confirm != 'y' and confirm != 'yes':
            return
        
        # Download all URLs
        completed = 0
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Processing: {url[:50]}...")
            if self.download_video(url):
                completed += 1
        
        print(f"\n  Batch download completed: {completed}/{len(urls)} successful")
    
    def show_settings(self):
        """Show settings menu"""
        while True:
            self.show_header()
            print("Settings")
            print()
            print("  1. Change Download Directory")
            print("  2. Set Default Quality")
            print("  3. View Supported Platforms")
            print("  4. About")
            print("  0. Back to Main Menu")
            print()
            
            choice = self.get_user_choice(4)
            
            if choice == 1:
                self._change_download_dir()
            elif choice == 2:
                self._set_default_quality()
            elif choice == 3:
                self._show_supported_platforms()
            elif choice == 4:
                self._show_about()
            elif choice == 0:
                break
    
    def _change_download_dir(self):
        """Change download directory"""
        print(f"\nCurrent directory: {self.downloads_dir}")
        new_dir = input("Enter new directory (or press Enter to keep current): ").strip()
        
        if new_dir:
            try:
                new_path = Path(new_dir)
                new_path.mkdir(parents=True, exist_ok=True)
                self.downloads_dir = new_path
                print(f"  ✓ Download directory changed to: {new_path}")
            except Exception as e:
                print(f"  ✗ Error: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def _set_default_quality(self):
        """Set default quality"""
        print("\nSelect default quality:")
        print("  1. Best Available")
        print("  2. 1080p")
        print("  3. 720p") 
        print("  4. 480p")
        print("  0. Cancel")
        
        choice = self.get_user_choice(4)
        qualities = {1: 'best', 2: '1080', 3: '720', 4: '480'}
        
        if choice in qualities:
            print(f"  ✓ Default quality set to: {qualities[choice]}")
        
        input("\nPress Enter to continue...")
    
    def _show_supported_platforms(self):
        """Show supported platforms"""
        print("\nSupported Platforms:")
        platforms = {
            'YouTube': 'youtube.com, youtu.be',
            'PornHub': 'pornhub.com',
            'Twitter/X': 'twitter.com, x.com',
            'Instagram': 'instagram.com',
            'TikTok': 'tiktok.com',
            'Bilibili': 'bilibili.com',
            'Twitch': 'twitch.tv',
            'And 1800+ more': 'via yt-dlp support'
        }
        
        for platform, domains in platforms.items():
            print(f"  • {platform:<15} ({domains})")
        
        input("\nPress Enter to continue...")
    
    def _show_about(self):
        """Show about information"""
        print("\nUniversal Video Downloader v2.0")
        print("━" * 40)
        print("Simple • Fast • Clean")
        print()
        print("Features:")
        print("  • Multi-platform support")
        print("  • High-quality downloads") 
        print("  • Audio extraction")
        print("  • Batch processing")
        print("  • Clean progress tracking")
        print()
        print("Technology:")
        print("  • Based on yt-dlp")
        print("  • Python 3.7+")
        print("  • Cross-platform")
        print()
        print("Made with ❤️ for simple video downloading")
        
        input("\nPress Enter to continue...")
    
    def manage_cookies(self):
        """Cookie management interface"""
        from cookie_manager import CookieManager
        
        while True:
            self.show_header()
            print("Cookie Management")
            print()
            print("  1. Import Cookies from JSON")
            print("  2. View Current Cookies") 
            print("  3. Delete Cookies")
            print("  4. Import Your PornHub Cookies")
            print("  0. Back to Main Menu")
            print()
            
            choice = self.get_user_choice(4)
            
            if choice == 1:
                self._import_cookies_json()
            elif choice == 2:
                self._view_cookies()
            elif choice == 3:
                self._delete_cookies()
            elif choice == 4:
                self._import_pornhub_cookies()
            elif choice == 0:
                break
    
    def _import_cookies_json(self):
        """Import cookies from JSON"""
        from cookie_manager import CookieManager
        
        print("\n" + "─" * 60)
        print("Import Cookies from JSON")
        print()
        print("Paste your JSON cookies below.")
        print("When finished, press Enter on an empty line:")
        print()
        
        lines = []
        try:
            while True:
                line = input()
                if not line:
                    break
                lines.append(line)
        except EOFError:
            pass
        
        if lines:
            cookies_text = '\n'.join(lines)
            platform = input("\nPlatform name (default: pornhub): ").strip() or "pornhub"
            
            manager = CookieManager()
            cookies_file = manager.save_json_cookies(cookies_text, platform)
            
            if cookies_file:
                print(f"\n✓ Cookies imported successfully for {platform}")
                # Refresh extractor cookies
                self.manager.extractor._setup_cookies()
            else:
                print("\n✗ Failed to import cookies")
        else:
            print("\nNo cookies provided")
        
        input("\nPress Enter to continue...")
    
    def _view_cookies(self):
        """View current cookies"""
        from cookie_manager import CookieManager
        
        print("\n" + "─" * 60)
        print("Current Cookies")
        
        manager = CookieManager()
        cookies = manager.list_cookies()
        
        if cookies:
            print("\nInstalled cookies:")
            for platform, file_path in cookies.items():
                print(f"  • {platform}: {file_path}")
                
            # Show which ones are active
            print("\nActive in downloader:")
            for platform, file_path in self.manager.extractor.cookies_files.items():
                print(f"  ✓ {platform}: {file_path}")
        else:
            print("\nNo cookies found")
            print("Import cookies to enable authentication for restricted content.")
        
        input("\nPress Enter to continue...")
    
    def _delete_cookies(self):
        """Delete cookies"""
        from cookie_manager import CookieManager
        
        manager = CookieManager()
        cookies = manager.list_cookies()
        
        if not cookies:
            print("\nNo cookies to delete")
            input("\nPress Enter to continue...")
            return
        
        print("\n" + "─" * 60)
        print("Delete Cookies")
        print("\nAvailable cookies:")
        for platform in cookies.keys():
            print(f"  • {platform}")
        
        platform = input("\nEnter platform name to delete: ").strip()
        if platform in cookies:
            confirm = input(f"Delete cookies for {platform}? (y/N): ").strip().lower()
            if confirm == 'y':
                manager.delete_cookies(platform)
                self.manager.extractor._setup_cookies()  # Refresh
                print(f"\n✓ Cookies deleted for {platform}")
            else:
                print("\nCancelled")
        else:
            print(f"\nPlatform '{platform}' not found")
        
        input("\nPress Enter to continue...")
    
    def _import_pornhub_cookies(self):
        """Quick import for PornHub cookies"""
        from cookie_manager import CookieManager
        
        print("\n" + "─" * 60)
        print("Import PornHub Cookies")
        print()
        print("This will help you download age-restricted content from PornHub.")
        print("You need to export cookies from your browser after logging in.")
        print()
        print("Steps:")
        print("  1. Login to PornHub in your browser")
        print("  2. Export cookies using a browser extension")
        print("  3. Copy the JSON data and paste it below")
        print()
        
        proceed = input("Proceed with cookie import? (y/N): ").strip().lower()
        if proceed != 'y':
            return
        
        print("\nPaste your PornHub cookies JSON:")
        print("(Press Enter on empty line when done)")
        print()
        
        lines = []
        try:
            while True:
                line = input()
                if not line:
                    break
                lines.append(line)
        except EOFError:
            pass
        
        if lines:
            cookies_text = '\n'.join(lines)
            manager = CookieManager()
            cookies_file = manager.save_json_cookies(cookies_text, "pornhub")
            
            if cookies_file:
                print(f"\n✓ PornHub cookies imported successfully!")
                print(f"File: {cookies_file}")
                self.manager.extractor._setup_cookies()
                print("\nYou can now download age-restricted PornHub content.")
            else:
                print("\n✗ Failed to import cookies")
        else:
            print("\nNo cookies provided")
        
        input("\nPress Enter to continue...")
    
    def optimize_speed(self):
        """Speed optimization interface"""
        while True:
            self.show_header()
            print("Speed Optimization")
            print()
            print(f"Current profile: {self.manager.speed_profile}")
            print(f"Threads: {self.manager.speed_settings['concurrent_fragment_downloads']}")
            print()
            print("  1. Change Speed Profile")
            print("  2. View Speed Settings")
            print("  3. Run Speed Benchmark") 
            print("  4. About Speed Optimization")
            print("  0. Back to Main Menu")
            print()
            
            choice = self.get_user_choice(4)
            
            if choice == 1:
                self._change_speed_profile()
            elif choice == 2:
                self._view_speed_settings()
            elif choice == 3:
                self._run_speed_benchmark()
            elif choice == 4:
                self._about_speed_optimization()
            elif choice == 0:
                break
    
    def _change_speed_profile(self):
        """Change speed profile"""
        print("\n" + "─" * 60)
        print("Speed Profiles")
        print()
        
        profiles = list(SpeedOptimizer.SPEED_PROFILES.keys())
        for i, (name, config) in enumerate(SpeedOptimizer.SPEED_PROFILES.items(), 1):
            current = " (CURRENT)" if name == self.manager.speed_profile else ""
            print(f"  {i}. {name.title()}{current}")
            print(f"     {config['description']}")
            print(f"     Threads: {config['concurrent_downloads']}, Chunk: {config['http_chunk_size']//1024//1024}MB")
            print()
        
        try:
            choice = int(input(f"Choose profile (1-{len(profiles)}): ").strip())
            if 1 <= choice <= len(profiles):
                new_profile = profiles[choice - 1]
                
                print(f"\nSwitching to {new_profile} profile...")
                
                # Create new optimized manager
                old_manager = self.manager
                self.manager = HighSpeedDownloader(speed_profile=new_profile, max_workers=4)
                self.manager.add_progress_callback(self._progress_callback)
                
                # Copy cookies if any
                if hasattr(old_manager.extractor, 'cookies_files'):
                    self.manager.extractor.cookies_files = old_manager.extractor.cookies_files
                
                old_manager.shutdown()
                
                print(f"✓ Speed profile changed to: {new_profile}")
            else:
                print("Invalid choice")
        except ValueError:
            print("Please enter a valid number")
        
        input("\nPress Enter to continue...")
    
    def _view_speed_settings(self):
        """View current speed settings"""
        print("\n" + "─" * 60)
        print("Current Speed Settings")
        print()
        print(f"Profile: {self.manager.speed_profile}")
        print()
        
        settings = self.manager.speed_settings
        for key, value in settings.items():
            if isinstance(value, int) and value > 1024:
                # Format large numbers
                if value >= 1024*1024:
                    value_str = f"{value//1024//1024}MB"
                else:
                    value_str = f"{value//1024}KB"
            else:
                value_str = str(value)
            
            print(f"  {key.replace('_', ' ').title()}: {value_str}")
        
        input("\nPress Enter to continue...")
    
    def _run_speed_benchmark(self):
        """Run speed benchmark"""
        print("\n" + "─" * 60)
        print("Speed Benchmark")
        print()
        print("This will download a small test video to measure speed.")
        print("The test file will be saved in ./benchmark/ directory.")
        print()
        
        proceed = input("Run benchmark? (y/N): ").strip().lower()
        if proceed != 'y':
            return
        
        print("\nRunning benchmark...")
        result = self.manager.benchmark_speed()
        
        if result['success']:
            print(f"\n✓ Benchmark completed!")
            print(f"  Duration: {result['duration']:.1f} seconds")
            print(f"  Profile: {result['profile']}")
            print(f"  Threads: {result['settings']['concurrent_fragment_downloads']}")
        else:
            print(f"\n✗ Benchmark failed: {result.get('error', 'Unknown error')}")
        
        input("\nPress Enter to continue...")
    
    def _about_speed_optimization(self):
        """About speed optimization"""
        print("\n" + "─" * 60)
        print("About Speed Optimization")
        print()
        print("Speed optimization uses multiple techniques:")
        print()
        print("🚀 Multi-threading:")
        print("  • Downloads video fragments in parallel")
        print("  • Uses 2-16 concurrent connections")
        print("  • Reduces total download time")
        print()
        print("📡 Network optimization:")
        print("  • Larger chunk sizes for faster transfers")
        print("  • Optimized socket timeouts")
        print("  • Connection keep-alive")
        print()
        print("💾 Format optimization:")
        print("  • Prefers MP4 format for speed")
        print("  • Optimized quality selection")
        print("  • Smart format fallbacks")
        print()
        print("🔧 Platform-specific tweaks:")
        print("  • Custom headers for better compatibility")
        print("  • Bypasses when safe to do so")
        print("  • Cookie integration for auth")
        print()
        print("⚡ Why not GPU?")
        print("  • Downloads are network-bound, not compute-bound")
        print("  • GPU helps with encoding/decoding, not downloading")
        print("  • Multi-threading is the proven solution")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop"""
        try:
            while True:
                self.show_header()
                self.show_main_menu()
                
                choice = self.get_user_choice(7)
                
                if choice == 0:
                    print("\nThank you for using Universal Video Downloader!")
                    break
                    
                elif choice == 1:
                    # Download Video
                    url = self.get_url_input()
                    if url:
                        self.download_video(url, audio_only=False)
                        input("\nPress Enter to continue...")
                
                elif choice == 2:
                    # Download Audio
                    url = self.get_url_input()
                    if url:
                        self.download_video(url, audio_only=True)
                        input("\nPress Enter to continue...")
                
                elif choice == 3:
                    # Get Video Info
                    url = self.get_url_input()
                    if url:
                        self.show_video_info(url)
                        input("\nPress Enter to continue...")
                
                elif choice == 4:
                    # Batch Download
                    self.batch_download()
                    input("\nPress Enter to continue...")
                
                elif choice == 5:
                    # Settings
                    self.show_settings()
                
                elif choice == 6:
                    # Cookie Management
                    self.manage_cookies()
                
                elif choice == 7:
                    # Speed Optimization
                    self.optimize_speed()
                    
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
        finally:
            self.manager.shutdown()


def main():
    """Main entry point"""
    downloader = SimpleDownloader()
    downloader.run()


if __name__ == '__main__':
    main()