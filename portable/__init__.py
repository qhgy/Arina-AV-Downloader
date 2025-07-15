"""
Portable Deployment Module
为视频下载器提供跨平台可移植性支持

Apple式设计理念：
- 开箱即用，零配置
- 静默智能，自动处理
- 优雅错误处理
- 用户友好体验
"""

from .env_checker import EnvChecker
from .path_manager import PathManager
from .dep_manager import DependencyManager
from .config_manager import ConfigManager
from .error_handler import ErrorHandler, global_error_handler
from .welcome_wizard import WelcomeWizard
from .maintenance import MaintenanceManager, global_maintenance_manager

__version__ = "1.0.0"
__author__ = "Universal Video Downloader Team"

# 导出主要类
__all__ = [
    'EnvChecker',
    'PathManager', 
    'DependencyManager',
    'ConfigManager',
    'ErrorHandler',
    'WelcomeWizard',
    'MaintenanceManager',
    'global_error_handler',
    'global_maintenance_manager'
]