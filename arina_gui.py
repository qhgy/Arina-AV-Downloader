#!/usr/bin/env python3
"""
Arina AV Downloader - GUI版本
Thanks to Arina for 10 years of companionship

主启动文件 - 图形界面版本
"""

import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    """主函数 - 启动GUI界面"""
    try:
        # 尝试导入最佳的GUI版本
        try:
            from perfect_apple_gui import main as gui_main
            print("🌸 启动 Arina AV Downloader GUI (Apple风格)")
        except ImportError:
            try:
                from pyside6_gui import main as gui_main
                print("🌸 启动 Arina AV Downloader GUI (PySide6)")
            except ImportError:
                try:
                    from simple_apple_gui import main as gui_main
                    print("🌸 启动 Arina AV Downloader GUI (简化版)")
                except ImportError:
                    from gui_downloader import main as gui_main
                    print("🌸 启动 Arina AV Downloader GUI (基础版)")
        
        # 启动GUI
        gui_main()
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("请检查依赖是否正确安装")
        input("按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 50)
    print("🌸 Arina AV Downloader v1.0.3")
    print("Thanks to Arina for 10 years of companionship 💕")
    print("=" * 50)
    main()
