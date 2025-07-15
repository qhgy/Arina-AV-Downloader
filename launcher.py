#!/usr/bin/env python3
"""
Universal Video Downloader 启动器
处理所有启动逻辑，避免命令行中文乱码问题
"""

import sys
import os
import subprocess
from pathlib import Path


def main():
    """主启动函数"""
    try:
        # 设置UTF-8编码
        if sys.platform == "win32":
            os.system("chcp 65001 >nul 2>&1")
        
        print("🎬 Universal Video Downloader")
        print("   Starting up...")
        print()
        
        # 切换到脚本所在目录
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        # 检查Python版本
        if not check_python_version():
            return 1
        
        print("⏳ Checking environment...")
        
        # 检查虚拟环境
        try:
            from portable.venv_manager import global_venv_manager
            venv_info = global_venv_manager.get_venv_info()
            
            if venv_info["in_venv"] == "True":
                print(f"✓ Running in virtual environment")
                print(f"  Python: {venv_info['python_version']}")
            else:
                print("ℹ️  Running in system Python environment")
                recommendation = global_venv_manager.get_recommendation()
                print(f"  {recommendation}")
                
                # 尝试创建虚拟环境（静默）
                global_venv_manager.create_venv_if_needed()
        except Exception:
            pass  # 虚拟环境检查失败不影响主流程
        
        # 运行环境检查
        result = subprocess.run([sys.executable, "-m", "portable.env_checker"], 
                              capture_output=False, text=True)
        
        if result.returncode != 0:
            print("\n❌ Environment check failed")
            print("💡 Please check the error messages above")
            input("\nPress Enter to exit...")
            return result.returncode
        
        print("\n✅ Environment check completed")
        print("🚀 Starting application...")
        print()
        
        # 检查是否在虚拟环境中，如果不是，尝试使用虚拟环境
        python_cmd = sys.executable
        
        try:
            from portable.venv_manager import global_venv_manager
            venv_python = global_venv_manager.get_venv_python()
            if venv_python and not global_venv_manager.is_in_venv():
                print("🔄 Using virtual environment Python...")
                python_cmd = venv_python
        except Exception:
            pass
        
        # 尝试启动Apple风格GUI版本
        try:
            result = subprocess.run([python_cmd, "apple_gui.py"], 
                                  check=False)
            if result.returncode != 0:
                print("⚠️  Apple GUI failed to start, trying fallback GUI...")
                print()
                
                # 尝试原版GUI
                result = subprocess.run([python_cmd, "gui_downloader.py"], 
                                      check=False)
                if result.returncode != 0:
                    print("⚠️  GUI failed to start, trying CLI version...")
                    print()
                    
                    # 启动命令行版本
                    result = subprocess.run([python_cmd, "universal_downloader.py"])
                    return result.returncode
        except Exception as e:
            print(f"❌ Failed to start application: {e}")
            input("\nPress Enter to exit...")
            return 1
        
        print("\n👋 Thank you for using Universal Video Downloader")
        return 0
        
    except KeyboardInterrupt:
        print("\n\n👋 Startup cancelled")
        return 0
    except Exception as e:
        print(f"\n❌ Startup error: {e}")
        input("\nPress Enter to exit...")
        return 1


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print()
        print("💡 Solution:")
        print("   1. Install Python 3.8 or higher")
        print("   2. Download from https://python.org")
        print()
        input("Press Enter to exit...")
        return False
    
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)