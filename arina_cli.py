#!/usr/bin/env python3
"""
Arina AV Downloader - CLI版本
Thanks to Arina for 10 years of companionship

主启动文件 - 命令行版本
"""

import sys
import os
import argparse

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    """主函数 - 启动CLI界面"""
    parser = argparse.ArgumentParser(
        description='Arina AV Downloader - 命令行版本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python arina_cli.py "https://example.com/video"
  python arina_cli.py "https://example.com/video" --output ./downloads
  python arina_cli.py "https://example.com/video" --quality best
        """
    )
    
    parser.add_argument('url', help='视频URL')
    parser.add_argument('--output', '-o', default='./downloads', help='下载目录 (默认: ./downloads)')
    parser.add_argument('--quality', '-q', default='best', help='视频质量 (默认: best)')
    parser.add_argument('--cookies', '-c', help='Cookie文件路径')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    try:
        # 尝试导入CLI下载器
        try:
            from universal_cli import download_video
        except ImportError:
            from universal_downloader import UniversalDownloader
            
            def download_video(url, output_dir, quality='best', cookies=None, verbose=False):
                downloader = UniversalDownloader()
                return downloader.download(url, output_dir, quality, cookies, verbose)
        
        print("🌸 Arina AV Downloader v1.0.3 - CLI")
        print("Thanks to Arina for 10 years of companionship 💕")
        print("-" * 50)
        
        if args.verbose:
            print(f"📥 URL: {args.url}")
            print(f"📁 输出目录: {args.output}")
            print(f"🎬 质量: {args.quality}")
            if args.cookies:
                print(f"🍪 Cookie文件: {args.cookies}")
        
        # 创建输出目录
        os.makedirs(args.output, exist_ok=True)
        
        # 开始下载
        success = download_video(
            url=args.url,
            output_dir=args.output,
            quality=args.quality,
            cookies=args.cookies,
            verbose=args.verbose
        )
        
        if success:
            print("✅ 下载完成！")
        else:
            print("❌ 下载失败！")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ 用户取消下载")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
