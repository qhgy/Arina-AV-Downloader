"""
依赖管理器
Apple式设计：静默安装，智能选择，优雅降级
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from abc import ABC, abstractmethod

from .models import PackageManager, ErrorInfo
from .utils import is_command_available, get_friendly_error_message, print_progress


class PackageManagerInterface(ABC):
    """包管理器接口"""
    
    @abstractmethod
    def is_available(self) -> bool:
        """检查包管理器是否可用"""
        pass
    
    @abstractmethod
    def install(self, packages: List[str]) -> bool:
        """安装包"""
        pass
    
    @abstractmethod
    def check_installed(self, package: str) -> bool:
        """检查包是否已安装"""
        pass
    
    @abstractmethod
    def list_installed(self) -> List[str]:
        """列出已安装的包"""
        pass
    
    @abstractmethod
    def get_version(self, package: str) -> Optional[str]:
        """获取包版本"""
        pass


class UvManager(PackageManagerInterface):
    """UV包管理器实现"""
    
    def __init__(self):
        self.command = "uv"
    
    def is_available(self) -> bool:
        """检查uv是否可用"""
        return is_command_available(self.command)
    
    def install(self, packages: List[str]) -> bool:
        """使用uv安装包"""
        try:
            # 首先确保有虚拟环境
            self._ensure_venv()
            
            # 安装包
            cmd = [self.command, "add"] + packages
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True,
                timeout=300
            )
            return result.returncode == 0
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def check_installed(self, package: str) -> bool:
        """检查包是否已安装"""
        try:
            # 尝试导入包
            package_import_name = package.replace("-", "_")
            __import__(package_import_name)
            return True
        except ImportError:
            return False
    
    def list_installed(self) -> List[str]:
        """列出已安装的包"""
        try:
            result = subprocess.run(
                [self.command, "pip", "list", "--format=freeze"],
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            
            packages = []
            for line in result.stdout.strip().split('\n'):
                if '==' in line:
                    packages.append(line.split('==')[0])
            return packages
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return []
    
    def get_version(self, package: str) -> Optional[str]:
        """获取包版本"""
        try:
            result = subprocess.run(
                [self.command, "pip", "show", package],
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    return line.split(':', 1)[1].strip()
            return None
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return None
    
    def _ensure_venv(self):
        """确保虚拟环境存在"""
        try:
            # 检查是否已经在虚拟环境中
            if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
                return
            
            # 检查是否存在uv项目配置
            project_root = Path(__file__).parent.parent
            pyproject_file = project_root / "pyproject.toml"
            
            if pyproject_file.exists():
                # 创建或激活虚拟环境
                subprocess.run(
                    [self.command, "sync"],
                    capture_output=True,
                    check=True,
                    timeout=60,
                    cwd=project_root
                )
            else:
                # 初始化uv项目
                subprocess.run(
                    [self.command, "init", "--no-readme"],
                    capture_output=True,
                    check=True,
                    timeout=30,
                    cwd=project_root
                )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            pass


class PipManager(PackageManagerInterface):
    """Pip包管理器实现"""
    
    def __init__(self):
        self.command = "pip"
    
    def is_available(self) -> bool:
        """检查pip是否可用"""
        return is_command_available(self.command)
    
    def install(self, packages: List[str]) -> bool:
        """使用pip安装包"""
        try:
            cmd = [sys.executable, "-m", "pip", "install"] + packages
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=300
            )
            return result.returncode == 0
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def check_installed(self, package: str) -> bool:
        """检查包是否已安装"""
        try:
            package_import_name = package.replace("-", "_")
            __import__(package_import_name)
            return True
        except ImportError:
            return False
    
    def list_installed(self) -> List[str]:
        """列出已安装的包"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list", "--format=freeze"],
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            
            packages = []
            for line in result.stdout.strip().split('\n'):
                if '==' in line:
                    packages.append(line.split('==')[0])
            return packages
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return []
    
    def get_version(self, package: str) -> Optional[str]:
        """获取包版本"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", package],
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    return line.split(':', 1)[1].strip()
            return None
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return None


class DependencyManager:
    """依赖管理器 - Apple式设计：智能选择，静默安装"""
    
    def __init__(self, silent: bool = False):
        self.silent = silent
        self.errors: List[ErrorInfo] = []
        self.package_manager = self._detect_package_manager()
        
    def _detect_package_manager(self) -> PackageManagerInterface:
        """检测并选择最佳的包管理器"""
        # 优先选择uv
        uv_manager = UvManager()
        if uv_manager.is_available():
            if not self.silent:
                print_progress("使用uv包管理器")
            return uv_manager
        
        # 回退到pip
        pip_manager = PipManager()
        if pip_manager.is_available():
            if not self.silent:
                print_progress("使用pip包管理器")
            return pip_manager
        
        # 都不可用
        error = ErrorInfo(
            code="no_package_manager",
            message="没有可用的包管理器",
            solution="请安装pip或uv",
            severity="error"
        )
        self.errors.append(error)
        return pip_manager  # 返回pip作为默认值
    
    def get_package_manager_type(self) -> PackageManager:
        """获取当前使用的包管理器类型"""
        if isinstance(self.package_manager, UvManager):
            return PackageManager.UV
        elif isinstance(self.package_manager, PipManager):
            return PackageManager.PIP
        else:
            return PackageManager.NONE
    
    def install_dependencies(self, packages: List[str] = None) -> bool:
        """安装依赖包"""
        if packages is None:
            packages = self._get_required_packages()
        
        if not self.silent:
            print_progress(f"正在安装依赖包: {', '.join(packages)}")
        
        success = True
        for package in packages:
            if not self.check_installed(package):
                if not self.silent:
                    print_progress(f"安装 {package}...")
                
                if not self.package_manager.install([package]):
                    error = ErrorInfo(
                        code="install_failed",
                        message=f"安装 {package} 失败",
                        solution="请检查网络连接或手动安装",
                        severity="error"
                    )
                    self.errors.append(error)
                    success = False
        
        return success
    
    def check_dependencies(self) -> Dict[str, bool]:
        """检查所有依赖的状态"""
        packages = self._get_required_packages()
        status = {}
        
        for package in packages:
            status[package] = self.check_installed(package)
        
        return status
    
    def check_installed(self, package: str) -> bool:
        """检查单个包是否已安装"""
        return self.package_manager.check_installed(package)
    
    def get_version(self, package: str) -> Optional[str]:
        """获取包版本"""
        return self.package_manager.get_version(package)
    
    def _get_required_packages(self) -> List[str]:
        """获取必需的包列表"""
        return [
            "yt-dlp>=2024.11.04"
        ]
    
    def _get_optional_packages(self) -> List[str]:
        """获取可选的包列表"""
        return [
            "PyQt6>=6.0.0",
            "PySide6>=6.0.0"
        ]
    
    def generate_pyproject_toml(self) -> bool:
        """生成pyproject.toml文件"""
        try:
            project_root = Path(__file__).parent.parent
            pyproject_file = project_root / "pyproject.toml"
            
            content = self._get_pyproject_content()
            
            with open(pyproject_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if not self.silent:
                print_progress("已生成 pyproject.toml")
            
            return True
        except Exception as e:
            error = ErrorInfo(
                code="pyproject_generation_failed",
                message=f"生成pyproject.toml失败: {str(e)}",
                solution="请检查文件权限",
                severity="error"
            )
            self.errors.append(error)
            return False
    
    def _get_pyproject_content(self) -> str:
        """获取pyproject.toml内容"""
        return '''[project]
name = "universal-video-downloader"
version = "1.0.0"
description = "Universal multi-platform video downloader with portable deployment"
requires-python = ">=3.8"
dependencies = [
    "yt-dlp>=2024.11.04",
]

[project.optional-dependencies]
gui = [
    "PyQt6>=6.0.0; platform_system!='Darwin'",
    "PySide6>=6.0.0; platform_system=='Darwin'"
]
dev = [
    "pytest>=7.0.0",
    "black>=22.0.0"
]

[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "black>=22.0.0"
]

[tool.uv.sources]
# 可以在这里指定特定的包源
'''
    
    def migrate_from_requirements_txt(self) -> bool:
        """从requirements.txt迁移到pyproject.toml"""
        try:
            project_root = Path(__file__).parent.parent
            requirements_file = project_root / "requirements.txt"
            
            if not requirements_file.exists():
                return True  # 没有requirements.txt文件，无需迁移
            
            # 读取现有依赖
            with open(requirements_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 解析依赖
            dependencies = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    dependencies.append(line)
            
            # 生成pyproject.toml
            return self.generate_pyproject_toml()
            
        except Exception as e:
            error = ErrorInfo(
                code="migration_failed",
                message=f"迁移失败: {str(e)}",
                solution="请手动创建pyproject.toml",
                severity="warning"
            )
            self.errors.append(error)
            return False
    
    def get_errors(self) -> List[ErrorInfo]:
        """获取错误列表"""
        return self.errors
    
    def has_errors(self) -> bool:
        """是否有错误"""
        return len(self.errors) > 0