"""
通用工具函数
提供可移植性模块的基础工具
"""

import sys
import platform
from pathlib import Path
from typing import Optional
from .models import SystemPlatform, ProjectStructure


def detect_system_platform() -> SystemPlatform:
    """检测系统平台"""
    system = platform.system().lower()
    
    if system == "windows":
        return SystemPlatform.WINDOWS
    elif system == "linux":
        return SystemPlatform.LINUX
    elif system == "darwin":
        return SystemPlatform.MACOS
    else:
        return SystemPlatform.UNKNOWN


def get_python_version() -> str:
    """获取Python版本"""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def is_python_version_compatible(min_version: str = "3.8") -> bool:
    """检查Python版本兼容性"""
    current = sys.version_info
    min_parts = [int(x) for x in min_version.split('.')]
    
    return (current.major, current.minor) >= (min_parts[0], min_parts[1])


def find_project_root() -> Path:
    """智能查找项目根目录"""
    return ProjectStructure.get_project_root()


def ensure_directory(path: Path) -> bool:
    """确保目录存在"""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False


def is_command_available(command: str) -> bool:
    """检查命令是否可用"""
    import subprocess
    
    try:
        subprocess.run(
            [command, "--version"], 
            capture_output=True, 
            check=True,
            timeout=10
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_friendly_error_message(error_code: str) -> str:
    """获取用户友好的错误信息"""
    error_messages = {
        "python_version": "Python版本过低，需要3.8或更高版本",
        "uv_missing": "uv包管理器未安装，将使用pip作为备选",
        "pip_missing": "pip包管理器不可用，请检查Python安装",
        "config_missing": "配置文件缺失，将自动创建默认配置",
        "dir_missing": "必要目录缺失，将自动创建",
        "dependency_missing": "依赖包缺失，将自动安装",
        "permission_denied": "权限不足，请以管理员身份运行",
        "network_error": "网络连接问题，请检查网络设置"
    }
    
    return error_messages.get(error_code, "未知错误，请联系技术支持")


def print_welcome_message():
    """打印欢迎信息"""
    print("🎬 Universal Video Downloader")
    print("   开箱即用的多平台视频下载器")
    print("   正在进行环境检查...")
    print()


def print_success_message():
    """打印成功信息"""
    print("✅ 环境检查完成，一切就绪！")
    print("🚀 正在启动应用程序...")
    print()


def print_progress(message: str, progress: int = 0):
    """打印进度信息"""
    if progress > 0:
        bar = "█" * (progress // 5) + "░" * (20 - progress // 5)
        print(f"\r{message} [{bar}] {progress}%", end="", flush=True)
    else:
        print(f"⏳ {message}")