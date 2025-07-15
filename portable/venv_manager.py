"""
虚拟环境管理器
Apple式设计：智能虚拟环境管理，无缝切换
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional, Dict, List
from .models import ErrorInfo
from .utils import is_command_available, print_progress


class VenvManager:
    """虚拟环境管理器 - Apple式设计：智能管理，无缝体验"""
    
    def __init__(self, silent: bool = False):
        self.silent = silent
        self.errors: List[ErrorInfo] = []
        self.project_root = Path(__file__).parent.parent
        self.venv_path = self.project_root / ".venv"
        
    def is_in_venv(self) -> bool:
        """检查是否在虚拟环境中"""
        # 检查标准虚拟环境标志
        in_standard_venv = (
            hasattr(sys, 'real_prefix') or 
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
            os.environ.get('VIRTUAL_ENV') is not None
        )
        
        # 检查是否在项目的.venv目录中运行
        if not in_standard_venv and self.venv_path.exists():
            # 检查当前Python是否来自项目的.venv
            current_python = Path(sys.executable).resolve()
            venv_python_paths = [
                self.venv_path / "Scripts" / "python.exe",  # Windows
                self.venv_path / "bin" / "python",         # Unix
            ]
            
            for venv_python in venv_python_paths:
                if venv_python.exists() and current_python == venv_python.resolve():
                    return True
        
        return in_standard_venv
    
    def get_venv_info(self) -> Dict[str, str]:
        """获取虚拟环境信息"""
        info = {
            "in_venv": str(self.is_in_venv()),
            "python_path": sys.executable,
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        }
        
        if self.is_in_venv():
            venv_path = os.environ.get('VIRTUAL_ENV')
            if venv_path:
                info["venv_path"] = venv_path
                info["venv_name"] = Path(venv_path).name
        
        return info
    
    def create_venv_if_needed(self) -> bool:
        """如果需要，创建虚拟环境"""
        if self.is_in_venv():
            if not self.silent:
                print_progress("已在虚拟环境中")
            return True
        
        # 检查是否存在项目虚拟环境
        if self.venv_path.exists():
            if not self.silent:
                print_progress("发现现有虚拟环境")
            return True
        
        # 尝试使用uv创建虚拟环境
        if self._create_uv_venv():
            return True
        
        # 回退到标准venv
        if self._create_standard_venv():
            return True
        
        # 如果都失败了，记录错误但不阻止运行
        error = ErrorInfo(
            code="venv_creation_failed",
            message="无法创建虚拟环境",
            solution="将在系统Python环境中运行",
            severity="warning",
            auto_fixable=False
        )
        self.errors.append(error)
        return False
    
    def _create_uv_venv(self) -> bool:
        """使用uv创建虚拟环境"""
        if not is_command_available("uv"):
            if not self.silent:
                print_progress("uv不可用，尝试安装...")
            # 尝试安装uv
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "uv"],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if not is_command_available("uv"):
                    return False
            except:
                return False
        
        try:
            if not self.silent:
                print_progress("使用uv创建虚拟环境...")
            
            # 检查是否已经存在.venv目录
            if self.venv_path.exists():
                if not self.silent:
                    print_progress("发现现有虚拟环境，跳过创建")
                return True
            
            # 使用uv创建虚拟环境
            result = subprocess.run(
                ["uv", "venv", ".venv"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                if not self.silent:
                    print_progress(f"uv venv失败: {result.stderr}")
                return False
            
            # 使用uv安装依赖
            if not self.silent:
                print_progress("安装基础依赖...")
            
            install_result = subprocess.run(
                ["uv", "pip", "install", "yt-dlp>=2024.11.04"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if install_result.returncode != 0:
                if not self.silent:
                    print_progress(f"依赖安装失败: {install_result.stderr}")
                return False
            
            if not self.silent:
                print_progress("uv虚拟环境创建成功")
            
            return True
            
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
            if not self.silent:
                print_progress(f"uv创建失败: {str(e)}")
            return False
    
    def _create_standard_venv(self) -> bool:
        """使用标准venv创建虚拟环境"""
        try:
            if not self.silent:
                print_progress("使用标准venv创建虚拟环境...")
            
            # 创建虚拟环境
            result = subprocess.run(
                [sys.executable, "-m", "venv", str(self.venv_path)],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                return False
            
            # 获取虚拟环境中的pip路径
            if sys.platform == "win32":
                pip_path = self.venv_path / "Scripts" / "pip.exe"
                python_path = self.venv_path / "Scripts" / "python.exe"
            else:
                pip_path = self.venv_path / "bin" / "pip"
                python_path = self.venv_path / "bin" / "python"
            
            # 升级pip
            subprocess.run(
                [str(python_path), "-m", "pip", "install", "--upgrade", "pip"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # 安装基础依赖
            subprocess.run(
                [str(pip_path), "install", "yt-dlp>=2024.11.04"],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            return True
            
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def get_venv_python(self) -> Optional[str]:
        """获取虚拟环境中的Python路径"""
        if self.is_in_venv():
            return sys.executable
        
        if self.venv_path.exists():
            if sys.platform == "win32":
                python_path = self.venv_path / "Scripts" / "python.exe"
            else:
                python_path = self.venv_path / "bin" / "python"
            
            if python_path.exists():
                return str(python_path)
        
        return None
    
    def activate_venv_command(self) -> Optional[List[str]]:
        """获取激活虚拟环境的命令"""
        if self.is_in_venv():
            return None  # 已经在虚拟环境中
        
        venv_python = self.get_venv_python()
        if venv_python:
            return [venv_python]
        
        return None
    
    def install_in_venv(self, packages: List[str]) -> bool:
        """在虚拟环境中安装包"""
        try:
            # 获取正确的Python路径
            python_cmd = self.get_venv_python() or sys.executable
            
            # 安装包
            cmd = [python_cmd, "-m", "pip", "install"] + packages
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            return result.returncode == 0
            
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def run_in_venv(self, script_args: List[str]) -> subprocess.Popen:
        """在虚拟环境中运行脚本"""
        python_cmd = self.get_venv_python() or sys.executable
        cmd = [python_cmd] + script_args
        
        return subprocess.Popen(
            cmd,
            cwd=self.project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    
    def get_recommendation(self) -> str:
        """获取虚拟环境使用建议"""
        if self.is_in_venv():
            return "✅ 当前在虚拟环境中运行，环境隔离良好"
        
        if self.venv_path.exists():
            return "💡 建议激活虚拟环境以获得更好的依赖管理"
        
        if is_command_available("uv"):
            return "💡 建议使用 'uv sync' 创建虚拟环境"
        else:
            return "💡 建议创建虚拟环境: python -m venv .venv"
    
    def get_errors(self) -> List[ErrorInfo]:
        """获取错误列表"""
        return self.errors
    
    def has_errors(self) -> bool:
        """是否有错误"""
        return len(self.errors) > 0


# 全局虚拟环境管理器实例
global_venv_manager = VenvManager()


def ensure_venv() -> bool:
    """确保虚拟环境存在"""
    return global_venv_manager.create_venv_if_needed()


def get_venv_info() -> Dict[str, str]:
    """获取虚拟环境信息"""
    return global_venv_manager.get_venv_info()


def get_venv_recommendation() -> str:
    """获取虚拟环境建议"""
    return global_venv_manager.get_recommendation()