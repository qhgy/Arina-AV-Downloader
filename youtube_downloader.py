#!/usr/bin/env python3
"""
YouTube 下载器
使用 yt-dlp 下载 YouTube 视频和音频
支持单个视频、播放列表下载，音频提取等功能
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import Optional, List


def check_dependencies():
    """检查并安装必要的依赖"""
    try:
        import yt_dlp
        return True
    except ImportError:
        print("检测到缺少 yt-dlp 依赖，正在安装...")
        try:
            # 使用 uv 安装（根据用户配置）
            if subprocess.run(["uv", "--version"], capture_output=True).returncode == 0:
                subprocess.run(["uv", "add", "yt-dlp"], check=True)
            else:
                subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)
            print("✅ yt-dlp 安装成功！")
            return True
        except subprocess.CalledProcessError:
            print("❌ 依赖安装失败，请手动安装: pip install yt-dlp")
            return False


class YouTubeDownloader:
    """YouTube 下载器类"""
    
    def __init__(self, output_dir: str = "./downloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def get_video_info(self, url: str) -> dict:
        """获取视频信息"""
        import yt_dlp
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'formats': info.get('formats', [])
                }
            except Exception as e:
                raise Exception(f"获取视频信息失败: {str(e)}")
    
    def download_video(self, url: str, quality: str = 'best', format_type: str = 'mp4') -> bool:
        """下载视频"""
        import yt_dlp
        
        # 设置输出模板
        output_template = str(self.output_dir / '%(title)s.%(ext)s')
        
        # 根据质量设置格式选择器
        if quality == 'best':
            format_selector = f'best[ext={format_type}]/best'
        elif quality == 'worst':
            format_selector = f'worst[ext={format_type}]/worst'
        else:
            # 指定分辨率
            format_selector = f'best[height<={quality}][ext={format_type}]/best[height<={quality}]/best'
        
        ydl_opts = {
            'outtmpl': output_template,
            'format': format_selector,
            'noplaylist': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                print(f"🎬 开始下载视频: {url}")
                ydl.download([url])
                print("✅ 视频下载完成！")
                return True
            except Exception as e:
                print(f"❌ 下载失败: {str(e)}")
                return False
    
    def download_audio(self, url: str, audio_format: str = 'mp3') -> bool:
        """下载音频"""
        import yt_dlp
        
        output_template = str(self.output_dir / '%(title)s.%(ext)s')
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': '192',
            }],
            'noplaylist': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                print(f"🎵 开始下载音频: {url}")
                ydl.download([url])
                print("✅ 音频下载完成！")
                return True
            except Exception as e:
                print(f"❌ 音频下载失败: {str(e)}")
                return False
    
    def download_playlist(self, url: str, quality: str = 'best', format_type: str = 'mp4') -> bool:
        """下载播放列表"""
        import yt_dlp
        
        output_template = str(self.output_dir / '%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s')
        
        if quality == 'best':
            format_selector = f'best[ext={format_type}]/best'
        elif quality == 'worst':
            format_selector = f'worst[ext={format_type}]/worst'
        else:
            format_selector = f'best[height<={quality}][ext={format_type}]/best[height<={quality}]/best'
        
        ydl_opts = {
            'outtmpl': output_template,
            'format': format_selector,
            'ignoreerrors': True,  # 跳过无法下载的视频
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                print(f"📋 开始下载播放列表: {url}")
                ydl.download([url])
                print("✅ 播放列表下载完成！")
                return True
            except Exception as e:
                print(f"❌ 播放列表下载失败: {str(e)}")
                return False
    
    def list_formats(self, url: str) -> None:
        """列出可用格式"""
        try:
            info = self.get_video_info(url)
            print(f"\n📹 视频: {info['title']}")
            print(f"👤 上传者: {info['uploader']}")
            print(f"⏱️  时长: {info['duration']}秒")
            print(f"👁️  观看次数: {info['view_count']:,}")
            
            print("\n📋 可用格式:")
            formats = info['formats']
            
            # 显示主要格式
            for fmt in formats[-10:]:  # 显示最后10个格式（通常是最好的）
                ext = fmt.get('ext', 'unknown')
                height = fmt.get('height', 'audio')
                filesize = fmt.get('filesize', 0)
                size_mb = f"{filesize/1024/1024:.1f}MB" if filesize else "未知大小"
                
                print(f"  格式ID: {fmt['format_id']:>8} | "
                      f"扩展名: {ext:>4} | "
                      f"分辨率: {str(height):>6} | "
                      f"大小: {size_mb:>10}")
                      
        except Exception as e:
            print(f"❌ 获取格式信息失败: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description='YouTube 视频下载器')
    parser.add_argument('url', help='YouTube 视频或播放列表 URL')
    parser.add_argument('-o', '--output', default='./downloads', help='输出目录 (默认: ./downloads)')
    parser.add_argument('-q', '--quality', default='best', 
                       help='视频质量: best, worst, 720, 1080 等 (默认: best)')
    parser.add_argument('-f', '--format', default='mp4', help='视频格式 (默认: mp4)')
    parser.add_argument('-a', '--audio', action='store_true', help='仅下载音频 (MP3)')
    parser.add_argument('-p', '--playlist', action='store_true', help='下载整个播放列表')
    parser.add_argument('-i', '--info', action='store_true', help='显示视频信息和可用格式')
    parser.add_argument('--audio-format', default='mp3', help='音频格式 (默认: mp3)')
    
    args = parser.parse_args()
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 创建下载器
    downloader = YouTubeDownloader(args.output)
    
    print(f"📁 输出目录: {os.path.abspath(args.output)}")
    
    try:
        if args.info:
            # 显示视频信息
            downloader.list_formats(args.url)
        elif args.audio:
            # 下载音频
            success = downloader.download_audio(args.url, args.audio_format)
        elif args.playlist:
            # 下载播放列表
            success = downloader.download_playlist(args.url, args.quality, args.format)
        else:
            # 下载单个视频
            success = downloader.download_video(args.url, args.quality, args.format)
        
        if not args.info:
            sys.exit(0 if success else 1)
            
    except KeyboardInterrupt:
        print("\n⏸️  下载已取消")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()