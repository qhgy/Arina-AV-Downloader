"""
静默优化和预测性维护
Apple式设计：后台智能优化，预测性维护
"""

import os
import time
import json
import threading
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from .path_manager import PathManager
from .config_manager import ConfigManager
from .dep_manager import DependencyManager
from .utils import print_progress


class MaintenanceManager:
    """维护管理器 - Apple式后台智能优化"""
    
    def __init__(self, silent: bool = True):
        self.silent = silent
        self.path_manager = PathManager(silent=True)
        self.config_manager = ConfigManager(silent=True)
        self.dep_manager = DependencyManager(silent=True)
        
        self.project_root = self.path_manager.get_project_root()
        self.maintenance_file = self.project_root / ".maintenance.json"
        
        self.maintenance_data = self._load_maintenance_data()
        
    def _load_maintenance_data(self) -> Dict:
        """加载维护数据"""
        if self.maintenance_file.exists():
            try:
                with open(self.maintenance_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # 默认维护数据
        return {
            "last_check": None,
            "last_cleanup": None,
            "last_update_check": None,
            "usage_stats": {
                "total_downloads": 0,
                "total_runtime": 0,
                "last_used": None,
                "favorite_platforms": {},
                "common_qualities": {}
            },
            "performance_stats": {
                "avg_download_speed": 0,
                "cache_hit_rate": 0,
                "error_rate": 0
            },
            "optimization_settings": {
                "auto_cleanup": True,
                "cache_enabled": True,
                "predictive_prefetch": True,
                "background_updates": True
            }
        }
    
    def _save_maintenance_data(self):
        """保存维护数据"""
        try:
            with open(self.maintenance_file, 'w', encoding='utf-8') as f:
                json.dump(self.maintenance_data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def run_background_maintenance(self):
        """运行后台维护任务"""
        if not self.silent:
            print_progress("启动后台维护...")
        
        # 在后台线程中运行
        maintenance_thread = threading.Thread(
            target=self._background_maintenance_worker,
            daemon=True
        )
        maintenance_thread.start()
    
    def _background_maintenance_worker(self):
        """后台维护工作线程"""
        while True:
            try:
                # 每小时检查一次
                time.sleep(3600)
                
                current_time = datetime.now().isoformat()
                
                # 检查是否需要清理
                if self._should_run_cleanup():
                    self._run_silent_cleanup()
                    self.maintenance_data["last_cleanup"] = current_time
                
                # 检查是否需要更新检查
                if self._should_check_updates():
                    self._check_for_updates()
                    self.maintenance_data["last_update_check"] = current_time
                
                # 优化缓存
                if self._should_optimize_cache():
                    self._optimize_cache()
                
                # 保存维护数据
                self._save_maintenance_data()
                
            except Exception:
                # 静默处理错误，不影响主程序
                pass
    
    def _should_run_cleanup(self) -> bool:
        """检查是否应该运行清理"""
        if not self.maintenance_data["optimization_settings"]["auto_cleanup"]:
            return False
        
        last_cleanup = self.maintenance_data.get("last_cleanup")
        if not last_cleanup:
            return True
        
        try:
            last_time = datetime.fromisoformat(last_cleanup)
            return datetime.now() - last_time > timedelta(days=7)
        except Exception:
            return True
    
    def _should_check_updates(self) -> bool:
        """检查是否应该检查更新"""
        if not self.maintenance_data["optimization_settings"]["background_updates"]:
            return False
        
        last_check = self.maintenance_data.get("last_update_check")
        if not last_check:
            return True
        
        try:
            last_time = datetime.fromisoformat(last_check)
            return datetime.now() - last_time > timedelta(days=3)
        except Exception:
            return True
    
    def _should_optimize_cache(self) -> bool:
        """检查是否应该优化缓存"""
        return self.maintenance_data["optimization_settings"]["cache_enabled"]
    
    def _run_silent_cleanup(self):
        """静默清理"""
        try:
            # 清理日志文件
            logs_dir = self.project_root / "logs"
            if logs_dir.exists():
                self._cleanup_old_logs(logs_dir)
            
            # 清理临时文件
            temp_files = [
                "*.tmp",
                "*.temp",
                "*.part",
                "*.ytdl"
            ]
            
            for pattern in temp_files:
                for file in self.project_root.glob(pattern):
                    try:
                        file.unlink()
                    except Exception:
                        pass
            
            # 清理空目录
            self._cleanup_empty_directories()
            
        except Exception:
            pass
    
    def _cleanup_old_logs(self, logs_dir: Path):
        """清理旧日志文件"""
        try:
            cutoff_date = datetime.now() - timedelta(days=30)
            
            for log_file in logs_dir.glob("*.log"):
                try:
                    if log_file.stat().st_mtime < cutoff_date.timestamp():
                        log_file.unlink()
                except Exception:
                    pass
        except Exception:
            pass
    
    def _cleanup_empty_directories(self):
        """清理空目录"""
        try:
            for root, dirs, files in os.walk(self.project_root):
                for dir_name in dirs:
                    dir_path = Path(root) / dir_name
                    try:
                        if not any(dir_path.iterdir()):
                            # 不删除重要目录
                            if dir_name not in ["downloads", "logs", "cookies", "portable", "tests"]:
                                dir_path.rmdir()
                    except Exception:
                        pass
        except Exception:
            pass
    
    def _check_for_updates(self):
        """检查依赖更新"""
        try:
            # 检查yt-dlp更新
            current_version = self.dep_manager.get_version("yt-dlp")
            if current_version:
                # 这里可以添加版本比较逻辑
                # 如果有新版本，可以记录到维护数据中
                pass
        except Exception:
            pass
    
    def _optimize_cache(self):
        """优化缓存"""
        try:
            # 清理路径管理器缓存
            self.path_manager.clear_cache()
            
            # 优化配置缓存
            # 这里可以添加更多缓存优化逻辑
            
        except Exception:
            pass
    
    def record_usage(self, platform: str, quality: str, download_time: float):
        """记录使用统计"""
        try:
            stats = self.maintenance_data["usage_stats"]
            
            # 更新统计
            stats["total_downloads"] += 1
            stats["total_runtime"] += download_time
            stats["last_used"] = datetime.now().isoformat()
            
            # 记录平台使用频率
            if platform not in stats["favorite_platforms"]:
                stats["favorite_platforms"][platform] = 0
            stats["favorite_platforms"][platform] += 1
            
            # 记录质量偏好
            if quality not in stats["common_qualities"]:
                stats["common_qualities"][quality] = 0
            stats["common_qualities"][quality] += 1
            
            # 保存数据
            self._save_maintenance_data()
            
        except Exception:
            pass
    
    def get_usage_insights(self) -> Dict:
        """获取使用洞察"""
        try:
            stats = self.maintenance_data["usage_stats"]
            
            # 分析最常用平台
            favorite_platform = None
            if stats["favorite_platforms"]:
                favorite_platform = max(
                    stats["favorite_platforms"].items(),
                    key=lambda x: x[1]
                )[0]
            
            # 分析最常用质量
            preferred_quality = None
            if stats["common_qualities"]:
                preferred_quality = max(
                    stats["common_qualities"].items(),
                    key=lambda x: x[1]
                )[0]
            
            return {
                "total_downloads": stats["total_downloads"],
                "favorite_platform": favorite_platform,
                "preferred_quality": preferred_quality,
                "last_used": stats["last_used"],
                "suggestions": self._generate_suggestions(stats)
            }
            
        except Exception:
            return {}
    
    def _generate_suggestions(self, stats: Dict) -> List[str]:
        """生成智能建议"""
        suggestions = []
        
        try:
            # 基于使用频率的建议
            if stats["total_downloads"] > 10:
                if "youtube" in stats.get("favorite_platforms", {}):
                    suggestions.append("💡 您经常下载YouTube视频，建议设置cookies以下载高质量内容")
                
                if stats.get("favorite_platforms", {}).get("pornhub", 0) > 5:
                    suggestions.append("🔒 建议为成人内容设置专门的下载目录")
            
            # 基于质量偏好的建议
            common_qualities = stats.get("common_qualities", {})
            if "best" in common_qualities and common_qualities["best"] > 5:
                suggestions.append("⚡ 您偏好最高质量，建议检查网络带宽以优化下载速度")
            
            # 基于使用时间的建议
            if stats["total_downloads"] > 50:
                suggestions.append("🎉 您是重度用户！考虑升级到批量下载模式")
            
        except Exception:
            pass
        
        return suggestions
    
    def get_maintenance_status(self) -> Dict:
        """获取维护状态"""
        return {
            "last_cleanup": self.maintenance_data.get("last_cleanup"),
            "last_update_check": self.maintenance_data.get("last_update_check"),
            "optimization_enabled": self.maintenance_data["optimization_settings"]["auto_cleanup"],
            "cache_enabled": self.maintenance_data["optimization_settings"]["cache_enabled"],
            "background_updates": self.maintenance_data["optimization_settings"]["background_updates"]
        }
    
    def update_optimization_settings(self, settings: Dict):
        """更新优化设置"""
        try:
            self.maintenance_data["optimization_settings"].update(settings)
            self._save_maintenance_data()
        except Exception:
            pass
    
    def force_maintenance(self):
        """强制执行维护"""
        if not self.silent:
            print_progress("执行系统维护...")
        
        try:
            # 执行清理
            self._run_silent_cleanup()
            
            # 检查更新
            self._check_for_updates()
            
            # 优化缓存
            self._optimize_cache()
            
            # 更新维护时间
            current_time = datetime.now().isoformat()
            self.maintenance_data["last_cleanup"] = current_time
            self.maintenance_data["last_update_check"] = current_time
            
            # 保存数据
            self._save_maintenance_data()
            
            if not self.silent:
                print_progress("系统维护完成")
            
            return True
            
        except Exception:
            return False


# 全局维护管理器实例
global_maintenance_manager = MaintenanceManager()


def start_background_maintenance():
    """启动后台维护"""
    global_maintenance_manager.run_background_maintenance()


def record_download_usage(platform: str, quality: str, download_time: float):
    """记录下载使用情况"""
    global_maintenance_manager.record_usage(platform, quality, download_time)


def get_user_insights() -> Dict:
    """获取用户使用洞察"""
    return global_maintenance_manager.get_usage_insights()