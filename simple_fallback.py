#!/usr/bin/env python3
"""
Simple Fallback Downloader for GUI
Basic yt-dlp wrapper without complex optimizations
"""

import os
import sys
from pathlib import Path

class SimpleYtDlpDownloader:
    """Simple yt-dlp wrapper"""
    
    def __init__(self):
        try:
            import yt_dlp
            self.yt_dlp = yt_dlp
            self.available = True
            print("Simple downloader initialized")
        except ImportError:
            self.available = False
            print("yt-dlp not available")
    
    def download(self, url: str, output_dir: str, audio_only: bool = False, progress_callback=None):
        """Simple download method with PornHub-specific fixes"""
        if not self.available:
            raise Exception("yt-dlp not installed")
        
        try:
            print(f"Starting download for: {url}")
            
            # Basic options with PornHub-specific settings
            ydl_opts = {
                'outtmpl': str(Path(output_dir) / '%(title)s.%(ext)s'),
                'noplaylist': True,
                
                # PornHub-specific settings
                'geo_bypass': True,
                'geo_bypass_country': 'US',
                'age_limit': 99,  # Bypass age restrictions
                'nocheckcertificate': True,
                'no_check_certificates': True,
                
                # User agent to avoid blocking
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                },
                
                # Retry settings
                'retries': 10,
                'fragment_retries': 10,
                
                # Connection settings
                'socket_timeout': 30,
            }
            
            # Format selection
            if audio_only:
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }]
            else:
                # For PornHub, prefer mp4 format with reasonable quality
                ydl_opts['format'] = 'best[ext=mp4][height<=1080]/best[height<=1080]/best'
            
            # Add progress hook if provided
            if progress_callback:
                def progress_hook(d):
                    if d['status'] == 'downloading':
                        if 'total_bytes' in d:
                            progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                            speed = d.get('speed', 0)
                            progress_callback(progress, speed)
                        elif '_percent_str' in d:
                            # Fallback progress parsing
                            try:
                                percent_str = d['_percent_str'].strip()
                                if '%' in percent_str:
                                    progress = float(percent_str.replace('%', ''))
                                    speed = d.get('speed', 0)
                                    progress_callback(progress, speed)
                            except:
                                pass
                
                ydl_opts['progress_hooks'] = [progress_hook]
            
            # Check if it's PornHub and needs special handling
            if 'pornhub.com' in url.lower():
                print("Detected PornHub URL - applying specific optimizations...")
                
                # Check for cookies
                cookie_files = ['pornhub_cookies.txt', 'cookies.txt', './cookies/pornhub.txt']
                for cookie_file in cookie_files:
                    if Path(cookie_file).exists():
                        ydl_opts['cookiefile'] = cookie_file
                        print(f"Using cookies: {cookie_file}")
                        break
                
                # PornHub-specific format preference
                if not audio_only:
                    ydl_opts['format'] = 'best[ext=mp4]/best'
            
            # Download with error handling
            with self.yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("Starting download...")
                ydl.download([url])
            
            print("Download completed successfully!")
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"Download error: {error_msg}")
            
            # Provide specific error guidance
            if "age" in error_msg.lower() or "restricted" in error_msg.lower():
                raise Exception("Age-restricted content. Please import cookies from a logged-in PornHub session.")
            elif "geo" in error_msg.lower() or "region" in error_msg.lower():
                raise Exception("Geo-restricted content. This video may not be available in your region.")
            elif "private" in error_msg.lower():
                raise Exception("Private video. This content requires special access permissions.")
            elif "not available" in error_msg.lower():
                raise Exception("Video not available. The video may have been removed or made private.")
            else:
                raise Exception(f"Download failed: {error_msg}")
    
    def get_video_info(self, url: str):
        """Get video information without downloading"""
        if not self.available:
            raise Exception("yt-dlp not installed")
        
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'geo_bypass': True,
                'age_limit': 99,
                'nocheckcertificate': True,
            }
            
            # Check for cookies for PornHub
            if 'pornhub.com' in url.lower():
                cookie_files = ['pornhub_cookies.txt', 'cookies.txt', './cookies/pornhub.txt']
                for cookie_file in cookie_files:
                    if Path(cookie_file).exists():
                        ydl_opts['cookiefile'] = cookie_file
                        break
            
            with self.yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            
            return info
            
        except Exception as e:
            error_msg = str(e)
            if "age" in error_msg.lower() or "restricted" in error_msg.lower():
                raise Exception("Age-restricted content. Please import cookies from a logged-in PornHub session.")
            else:
                raise Exception(f"Failed to get video info: {error_msg}")

if __name__ == '__main__':
    # Test the simple downloader
    downloader = SimpleYtDlpDownloader()
    if downloader.available:
        print("Simple downloader test passed")
    else:
        print("Simple downloader test failed - yt-dlp not available")