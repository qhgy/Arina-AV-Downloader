"""
路径管理器
Apple式设计：智能路径处理，跨平台兼容，透明转换
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Union
from .models import ErrorInfo, ProjectStructure
from .utils import ensure_directory, get_friendly_error_message, print_progress


class PathManager:
    """路径管理器 - Apple式设计：智能处理，透明转换"""
    
    def __init__(self, silent: bool = False):
        self.silent = silent
        self.errors: List[ErrorInfo] = []
        self._project_root = None
        self._cache = {}  # 路径缓存
    
    def get_project_root(self) -> Path:
        """获取项目根目录（带缓存）"""
        if self._project_root is None:
            self._project_root = ProjectStructure.get_project_root()
            if not self.silent:
                print_progress(f"项目根目录: {self._project_root}")
        return self._project_root
    
    def resolve_relative_path(self, path: Union[str, Path]) -> Path:
        """将相对路径解析为绝对路径"""
        if isinstance(path, str):
            path = Path(path)
        
        # 如果已经是绝对路径，直接返回
        if path.is_absolute():
            return path.resolve()
        
        # 相对于项目根目录解析
        project_root = self.get_project_root()
        resolved = (project_root / path).resolve()
        
        return resolved
    
    def convert_to_relative(self, absolute_path: Union[str, Path]) -> str:
        """将绝对路径转换为相对于项目根目录的路径"""
        if isinstance(absolute_path, str):
            absolute_path = Path(absolute_path)
        
        project_root = self.get_project_root()
        
        try:
            # 尝试计算相对路径
            relative = absolute_path.relative_to(project_root)
            return str(relative).replace('\\', '/')  # 统一使用正斜杠
        except ValueError:
            # 如果路径不在项目根目录下，返回绝对路径
            return str(absolute_path).replace('\\', '/')
    
    def normalize_path(self, path: Union[str, Path]) -> str:
        """标准化路径格式（跨平台兼容）"""
        if isinstance(path, Path):
            path = str(path)
        
        # 统一使用正斜杠
        normalized = path.replace('\\', '/')
        
        # 移除多余的斜杠
        while '//' in normalized:
            normalized = normalized.replace('//', '/')
        
        # 移除末尾的斜杠（除非是根目录）
        if normalized.endswith('/') and len(normalized) > 1:
            normalized = normalized[:-1]
        
        return normalized
    
    def ensure_directory_exists(self, path: Union[str, Path]) -> bool:
        """确保目录存在"""
        if isinstance(path, str):
            path = Path(path)
        
        # 如果是相对路径，解析为绝对路径
        if not path.is_absolute():
            path = self.resolve_relative_path(path)
        
        return ensure_directory(path)
    
    def create_project_directories(self) -> Dict[str, bool]:
        """创建项目必需的目录结构"""
        if not self.silent:
            print_progress("创建项目目录结构...")
        
        project_root = self.get_project_root()
        results = {}
        
        for dir_name in ProjectStructure.REQUIRED_DIRS:
            dir_path = project_root / dir_name
            success = self.ensure_directory_exists(dir_path)
            results[dir_name] = success
            
            if not success:
                error = ErrorInfo(
                    code="dir_creation_failed",
                    message=f"无法创建目录: {dir_name}",
                    solution="请检查文件权限",
                    severity="error"
                )
                self.errors.append(error)
        
        return results
    
    def normalize_config_paths(self, config: Dict) -> Dict:
        """标准化配置文件中的路径"""
        if not self.silent:
            print_progress("标准化配置路径...")
        
        normalized_config = config.copy()
        
        # 需要处理的路径字段
        path_fields = [
            'default_output_dir',
            'output_dir',
            'logs_dir',
            'cookies_dir',
            'config_file'
        ]
        
        for field in path_fields:
            if field in normalized_config:
                original_path = normalized_config[field]
                
                # 转换为相对路径
                if os.path.isabs(original_path):
                    normalized_config[field] = self.convert_to_relative(original_path)
                else:
                    # 已经是相对路径，只需要标准化格式
                    normalized_config[field] = self.normalize_path(original_path)
        
        return normalized_config
    
    def validate_path(self, path: Union[str, Path]) -> bool:
        """验证路径的有效性"""
        try:
            if isinstance(path, str):
                path = Path(path)
            
            # 检查路径是否包含非法字符
            illegal_chars = ['<', '>', ':', '"', '|', '?', '*']
            path_str = str(path)
            
            for char in illegal_chars:
                if char in path_str:
                    return False
            
            # 检查路径长度（Windows限制）
            if len(path_str) > 260:
                return False
            
            return True
        except Exception:
            return False
    
    def get_safe_filename(self, filename: str) -> str:
        """获取安全的文件名（移除非法字符）"""
        # 非法字符替换映射
        replacements = {
            '<': '(',
            '>': ')',
            ':': '-',
            '"': "'",
            '|': '-',
            '?': '',
            '*': '',
            '/': '-',
            '\\': '-'
        }
        
        safe_name = filename
        for illegal, replacement in replacements.items():
            safe_name = safe_name.replace(illegal, replacement)
        
        # 移除多余的空格和点
        safe_name = safe_name.strip('. ')
        
        # 确保不为空
        if not safe_name:
            safe_name = "untitled"
        
        return safe_name
    
    def get_relative_paths_info(self) -> Dict[str, str]:
        """获取项目相对路径信息"""
        project_root = self.get_project_root()
        
        info = {
            'project_root': str(project_root),
            'downloads': self.convert_to_relative(project_root / 'downloads'),
            'logs': self.convert_to_relative(project_root / 'logs'),
            'cookies': self.convert_to_relative(project_root / 'cookies'),
            'config': self.convert_to_relative(project_root / 'downloader_config.json')
        }
        
        return info
    
    def migrate_absolute_paths(self, config: Dict) -> Dict:
        """迁移配置中的绝对路径为相对路径"""
        if not self.silent:
            print_progress("迁移绝对路径...")
        
        migrated_config = config.copy()
        project_root = self.get_project_root()
        
        # 检查并转换绝对路径
        for key, value in config.items():
            if isinstance(value, str) and os.path.isabs(value):
                try:
                    abs_path = Path(value)
                    if abs_path.is_relative_to(project_root):
                        # 转换为相对路径
                        relative_path = self.convert_to_relative(abs_path)
                        migrated_config[key] = relative_path
                        
                        if not self.silent:
                            print_progress(f"转换路径: {key} -> {relative_path}")
                except Exception:
                    # 如果转换失败，保持原值
                    pass
        
        return migrated_config
    
    def backup_config(self, config_path: Union[str, Path]) -> Optional[Path]:
        """备份配置文件"""
        try:
            if isinstance(config_path, str):
                config_path = Path(config_path)
            
            if not config_path.exists():
                return None
            
            # 创建备份文件名
            backup_path = config_path.with_suffix(f'{config_path.suffix}.backup')
            
            # 复制文件
            import shutil
            shutil.copy2(config_path, backup_path)
            
            if not self.silent:
                print_progress(f"配置已备份: {backup_path}")
            
            return backup_path
        except Exception as e:
            error = ErrorInfo(
                code="backup_failed",
                message=f"备份配置失败: {str(e)}",
                solution="请检查文件权限",
                severity="warning"
            )
            self.errors.append(error)
            return None
    
    def get_errors(self) -> List[ErrorInfo]:
        """获取错误列表"""
        return self.errors
    
    def has_errors(self) -> bool:
        """是否有错误"""
        return len(self.errors) > 0
    
    def clear_cache(self):
        """清除路径缓存"""
        self._cache.clear()
        self._project_root = None