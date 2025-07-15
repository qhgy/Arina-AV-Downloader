"""
核心数据模型
定义可移植性模块使用的数据结构
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum


class PackageManager(Enum):
    """包管理器类型"""
    UV = "uv"
    PIP = "pip"
    NONE = "none"


class SystemPlatform(Enum):
    """系统平台类型"""
    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"
    UNKNOWN = "unknown"


@dataclass
class EnvironmentInfo:
    """环境信息模型"""
    python_version: str
    platform: SystemPlatform
    project_root: Path
    package_manager: PackageManager
    dependencies_status: Dict[str, bool]
    config_status: bool
    directories_status: Dict[str, bool]
    
    @property
    def is_ready(self) -> bool:
        """检查环境是否就绪"""
        return (
            self.config_status and
            all(self.dependencies_status.values()) and
            all(self.directories_status.values())
        )


@dataclass
class PortableConfig:
    """可移植配置模型"""
    project_root: Path
    output_dir: Path
    logs_dir: Path
    cookies_dir: Path
    config_file: Path
    dependencies: List[str]
    package_manager: PackageManager
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            'project_root': str(self.project_root),
            'output_dir': str(self.output_dir.relative_to(self.project_root)),
            'logs_dir': str(self.logs_dir.relative_to(self.project_root)),
            'cookies_dir': str(self.cookies_dir.relative_to(self.project_root)),
            'config_file': str(self.config_file.relative_to(self.project_root)),
            'dependencies': self.dependencies,
            'package_manager': self.package_manager.value
        }


@dataclass
class ErrorInfo:
    """错误信息模型"""
    code: str
    message: str
    solution: str
    auto_fixable: bool = False
    severity: str = "error"  # error, warning, info
    
    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.message}"


class ProjectStructure:
    """项目结构定义"""
    
    REQUIRED_DIRS = [
        "downloads",
        "logs", 
        "cookies"
    ]
    
    CONFIG_FILES = [
        "downloader_config.json",
        "pyproject.toml"
    ]
    
    MAIN_SCRIPTS = [
        "universal_downloader.py",
        "gui_downloader.py"
    ]
    
    @classmethod
    def get_project_root(cls) -> Path:
        """获取项目根目录"""
        current = Path(__file__).parent.parent
        
        # 检查是否包含主要脚本文件
        for script in cls.MAIN_SCRIPTS:
            if (current / script).exists():
                return current.resolve()
        
        # 如果当前目录不是项目根目录，向上查找
        for parent in current.parents:
            if all((parent / script).exists() for script in cls.MAIN_SCRIPTS[:1]):
                return parent.resolve()
        
        # 默认返回当前目录的父目录
        return current.resolve()