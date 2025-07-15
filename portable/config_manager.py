"""
配置管理器
Apple式设计：智能配置，自动修复，优雅降级
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from .models import ErrorInfo, ProjectStructure
from .path_manager import PathManager
from .utils import get_friendly_error_message, print_progress


class ConfigManager:
    """配置管理器 - Apple式设计：智能配置，自动修复"""
    
    def __init__(self, silent: bool = False):
        self.silent = silent
        self.errors: List[ErrorInfo] = []
        self.path_manager = PathManager(silent=silent)
        self.project_root = self.path_manager.get_project_root()
        
    def load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """加载配置文件"""
        if config_path is None:
            config_path = "downloader_config.json"
        
        config_file = self.project_root / config_path
        
        if not self.silent:
            print_progress(f"加载配置: {config_file}")
        
        try:
            if not config_file.exists():
                if not self.silent:
                    print_progress("配置文件不存在，创建默认配置")
                return self.create_default_config()
            
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 标准化路径
            config = self.normalize_paths(config)
            
            # 验证配置
            if not self.validate_config(config):
                if not self.silent:
                    print_progress("配置验证失败，使用默认配置")
                return self.create_default_config()
            
            return config
            
        except json.JSONDecodeError as e:
            error = ErrorInfo(
                code="config_parse_error",
                message=f"配置文件格式错误: {str(e)}",
                solution="将重新创建默认配置",
                severity="warning",
                auto_fixable=True
            )
            self.errors.append(error)
            return self.create_default_config()
            
        except Exception as e:
            error = ErrorInfo(
                code="config_load_error",
                message=f"加载配置失败: {str(e)}",
                solution="将使用默认配置",
                severity="error"
            )
            self.errors.append(error)
            return self.create_default_config()
    
    def save_config(self, config: Dict[str, Any], config_path: Optional[str] = None) -> bool:
        """保存配置文件"""
        if config_path is None:
            config_path = "downloader_config.json"
        
        config_file = self.project_root / config_path
        
        if not self.silent:
            print_progress(f"保存配置: {config_file}")
        
        try:
            # 备份现有配置
            if config_file.exists():
                self.path_manager.backup_config(config_file)
            
            # 标准化路径
            normalized_config = self.normalize_paths(config)
            
            # 保存配置
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(normalized_config, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            error = ErrorInfo(
                code="config_save_error",
                message=f"保存配置失败: {str(e)}",
                solution="请检查文件权限",
                severity="error"
            )
            self.errors.append(error)
            return False
    
    def normalize_paths(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """标准化配置中的路径"""
        return self.path_manager.normalize_config_paths(config)
    
    def create_default_config(self) -> Dict[str, Any]:
        """创建默认配置"""
        if not self.silent:
            print_progress("创建默认配置")
        
        default_config = {
            "max_workers": 4,
            "default_output_dir": "./downloads",
            "default_quality": "best",
            "default_format": "mp4",
            "platforms": {
                "youtube": {
                    "enabled": True,
                    "quality_preference": [
                        "1080",
                        "720",
                        "best"
                    ]
                },
                "pornhub": {
                    "enabled": True,
                    "quality_preference": [
                        "720",
                        "best"
                    ],
                    "age_verification": True
                },
                "twitter": {
                    "enabled": True,
                    "quality_preference": [
                        "720",
                        "best"
                    ]
                },
                "instagram": {
                    "enabled": True,
                    "quality_preference": [
                        "720",
                        "best"
                    ]
                },
                "tiktok": {
                    "enabled": True,
                    "quality_preference": [
                        "720",
                        "best"
                    ]
                },
                "bilibili": {
                    "enabled": True,
                    "quality_preference": [
                        "1080",
                        "720",
                        "best"
                    ]
                },
                "twitch": {
                    "enabled": True,
                    "quality_preference": [
                        "720",
                        "best"
                    ]
                },
                "generic": {
                    "enabled": True
                }
            },
            "download_settings": {
                "retry_attempts": 3,
                "timeout": 300,
                "concurrent_downloads": 2
            },
            "file_settings": {
                "filename_template": "%(title)s.%(ext)s",
                "subtitle_languages": ["zh", "en"],
                "embed_subtitles": False
            },
            "network_settings": {
                "proxy": "",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        }
        
        # 保存默认配置
        self.save_config(default_config)
        
        return default_config
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """验证配置文件的有效性"""
        try:
            # 检查必需的字段
            required_fields = [
                "max_workers",
                "default_output_dir",
                "default_quality",
                "default_format",
                "platforms"
            ]
            
            for field in required_fields:
                if field not in config:
                    error = ErrorInfo(
                        code="config_missing_field",
                        message=f"配置缺少必需字段: {field}",
                        solution="将使用默认值",
                        severity="warning",
                        auto_fixable=True
                    )
                    self.errors.append(error)
                    return False
            
            # 验证数值字段
            if not isinstance(config.get("max_workers"), int) or config["max_workers"] < 1:
                return False
            
            # 验证路径字段
            output_dir = config.get("default_output_dir")
            if output_dir and not self.path_manager.validate_path(output_dir):
                return False
            
            # 验证平台配置
            platforms = config.get("platforms", {})
            if not isinstance(platforms, dict):
                return False
            
            return True
            
        except Exception:
            return False
    
    def migrate_config(self, old_config_path: Optional[str] = None) -> bool:
        """迁移旧配置文件"""
        if old_config_path is None:
            old_config_path = "downloader_config.json"
        
        old_config_file = self.project_root / old_config_path
        
        if not old_config_file.exists():
            return True  # 没有旧配置，无需迁移
        
        if not self.silent:
            print_progress("迁移配置文件...")
        
        try:
            # 加载旧配置
            with open(old_config_file, 'r', encoding='utf-8') as f:
                old_config = json.load(f)
            
            # 迁移路径
            migrated_config = self.path_manager.migrate_absolute_paths(old_config)
            
            # 保存迁移后的配置
            return self.save_config(migrated_config)
            
        except Exception as e:
            error = ErrorInfo(
                code="config_migration_error",
                message=f"配置迁移失败: {str(e)}",
                solution="将创建新的默认配置",
                severity="warning"
            )
            self.errors.append(error)
            return False
    
    def repair_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """修复损坏的配置"""
        if not self.silent:
            print_progress("修复配置文件...")
        
        # 获取默认配置作为模板
        default_config = self.create_default_config()
        
        # 合并配置（保留有效的用户设置）
        repaired_config = default_config.copy()
        
        def merge_dict(target: Dict, source: Dict):
            """递归合并字典"""
            for key, value in source.items():
                if key in target:
                    if isinstance(target[key], dict) and isinstance(value, dict):
                        merge_dict(target[key], value)
                    else:
                        # 验证值的有效性
                        if self._is_valid_config_value(key, value):
                            target[key] = value
        
        try:
            merge_dict(repaired_config, config)
        except Exception:
            # 如果合并失败，使用默认配置
            repaired_config = default_config
        
        return repaired_config
    
    def _is_valid_config_value(self, key: str, value: Any) -> bool:
        """验证配置值的有效性"""
        try:
            if key == "max_workers":
                return isinstance(value, int) and value > 0
            elif key in ["default_output_dir"]:
                return isinstance(value, str) and self.path_manager.validate_path(value)
            elif key in ["default_quality", "default_format"]:
                return isinstance(value, str) and len(value) > 0
            elif key == "platforms":
                return isinstance(value, dict)
            else:
                return True  # 其他字段暂时不验证
        except Exception:
            return False
    
    def get_config_info(self) -> Dict[str, Any]:
        """获取配置信息摘要"""
        config = self.load_config()
        
        info = {
            "config_file": str(self.project_root / "downloader_config.json"),
            "platforms_enabled": len([p for p, settings in config.get("platforms", {}).items() 
                                    if settings.get("enabled", False)]),
            "output_directory": config.get("default_output_dir", "./downloads"),
            "max_workers": config.get("max_workers", 4),
            "default_quality": config.get("default_quality", "best")
        }
        
        return info
    
    def reset_to_defaults(self) -> bool:
        """重置为默认配置"""
        if not self.silent:
            print_progress("重置为默认配置...")
        
        try:
            # 备份当前配置
            config_file = self.project_root / "downloader_config.json"
            if config_file.exists():
                self.path_manager.backup_config(config_file)
            
            # 创建默认配置
            self.create_default_config()
            return True
            
        except Exception as e:
            error = ErrorInfo(
                code="config_reset_error",
                message=f"重置配置失败: {str(e)}",
                solution="请手动删除配置文件",
                severity="error"
            )
            self.errors.append(error)
            return False
    
    def get_errors(self) -> List[ErrorInfo]:
        """获取错误列表"""
        return self.errors + self.path_manager.get_errors()
    
    def has_errors(self) -> bool:
        """是否有错误"""
        return len(self.get_errors()) > 0