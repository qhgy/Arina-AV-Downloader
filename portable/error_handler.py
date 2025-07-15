"""
错误处理器
Apple式设计：用户友好的错误处理，智能建议，一键修复
"""

import sys
import traceback
from typing import List, Dict, Optional, Callable
from .models import ErrorInfo
from .utils import get_friendly_error_message


class ErrorHandler:
    """错误处理器 - Apple式设计：优雅处理，智能修复"""
    
    def __init__(self):
        self.error_handlers: Dict[str, Callable] = {}
        self.auto_fix_handlers: Dict[str, Callable] = {}
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """注册默认错误处理器"""
        # Python版本错误
        self.register_error_handler("python_version", self._handle_python_version_error)
        
        # 包管理器错误
        self.register_error_handler("uv_missing", self._handle_uv_missing)
        self.register_error_handler("pip_missing", self._handle_pip_missing)
        
        # 依赖错误
        self.register_error_handler("dependency_missing", self._handle_dependency_missing)
        self.register_auto_fix("dependency_missing", self._auto_fix_dependencies)
        
        # 配置错误
        self.register_error_handler("config_missing", self._handle_config_missing)
        self.register_auto_fix("config_missing", self._auto_fix_config)
        
        # 目录错误
        self.register_error_handler("dir_missing", self._handle_dir_missing)
        self.register_auto_fix("dir_missing", self._auto_fix_directories)
        
        # 权限错误
        self.register_error_handler("permission_denied", self._handle_permission_error)
        
        # 网络错误
        self.register_error_handler("network_error", self._handle_network_error)
    
    def register_error_handler(self, error_code: str, handler: Callable):
        """注册错误处理器"""
        self.error_handlers[error_code] = handler
    
    def register_auto_fix(self, error_code: str, fix_handler: Callable):
        """注册自动修复处理器"""
        self.auto_fix_handlers[error_code] = fix_handler
    
    def handle_error(self, error: ErrorInfo) -> bool:
        """处理单个错误"""
        print(f"\n{self._get_error_icon(error.severity)} {error.message}")
        
        # 显示解决方案
        if error.solution:
            print(f"💡 解决方案: {error.solution}")
        
        # 如果有自定义处理器，调用它
        if error.code in self.error_handlers:
            try:
                return self.error_handlers[error.code](error)
            except Exception as e:
                print(f"⚠️  错误处理器执行失败: {str(e)}")
        
        return False
    
    def handle_errors(self, errors: List[ErrorInfo]) -> Dict[str, bool]:
        """处理多个错误"""
        results = {}
        
        if not errors:
            return results
        
        print(f"\n🔧 发现 {len(errors)} 个问题，正在处理...")
        print("=" * 50)
        
        for error in errors:
            print(f"\n处理问题: {error.code}")
            success = self.handle_error(error)
            results[error.code] = success
            
            if success:
                print("✅ 问题已解决")
            else:
                print("❌ 问题未能自动解决")
        
        return results
    
    def auto_fix_errors(self, errors: List[ErrorInfo]) -> Dict[str, bool]:
        """自动修复错误"""
        results = {}
        fixable_errors = [e for e in errors if e.auto_fixable]
        
        if not fixable_errors:
            print("ℹ️  没有可自动修复的问题")
            return results
        
        print(f"\n🔧 自动修复 {len(fixable_errors)} 个问题...")
        print("=" * 50)
        
        for error in fixable_errors:
            print(f"\n修复问题: {error.code}")
            
            if error.code in self.auto_fix_handlers:
                try:
                    success = self.auto_fix_handlers[error.code](error)
                    results[error.code] = success
                    
                    if success:
                        print("✅ 自动修复成功")
                    else:
                        print("❌ 自动修复失败")
                except Exception as e:
                    print(f"❌ 自动修复过程中出错: {str(e)}")
                    results[error.code] = False
            else:
                print("⚠️  没有可用的自动修复方案")
                results[error.code] = False
        
        return results
    
    def show_error_summary(self, errors: List[ErrorInfo]):
        """显示错误摘要"""
        if not errors:
            print("\n✅ 没有发现问题")
            return
        
        print(f"\n📋 问题摘要 ({len(errors)} 个问题)")
        print("=" * 50)
        
        # 按严重程度分组
        critical_errors = [e for e in errors if e.severity == "error"]
        warnings = [e for e in errors if e.severity == "warning"]
        infos = [e for e in errors if e.severity == "info"]
        
        if critical_errors:
            print(f"\n❌ 严重错误 ({len(critical_errors)} 个):")
            for error in critical_errors:
                print(f"   • {error.message}")
        
        if warnings:
            print(f"\n⚠️  警告 ({len(warnings)} 个):")
            for error in warnings:
                print(f"   • {error.message}")
        
        if infos:
            print(f"\nℹ️  信息 ({len(infos)} 个):")
            for error in infos:
                print(f"   • {error.message}")
        
        # 显示可自动修复的问题
        auto_fixable = [e for e in errors if e.auto_fixable]
        if auto_fixable:
            print(f"\n🔧 可自动修复 ({len(auto_fixable)} 个):")
            for error in auto_fixable:
                print(f"   • {error.message}")
    
    def _get_error_icon(self, severity: str) -> str:
        """获取错误图标"""
        icons = {
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️"
        }
        return icons.get(severity, "❓")
    
    # 默认错误处理器实现
    def _handle_python_version_error(self, error: ErrorInfo) -> bool:
        """处理Python版本错误"""
        print("\n🐍 Python版本检查:")
        print(f"   当前版本: {sys.version}")
        print("   需要版本: 3.8 或更高")
        print("\n📥 安装建议:")
        print("   • Windows: 从 https://python.org 下载安装")
        print("   • macOS: brew install python3")
        print("   • Ubuntu: sudo apt install python3.8")
        return False
    
    def _handle_uv_missing(self, error: ErrorInfo) -> bool:
        """处理uv缺失"""
        print("\n📦 UV包管理器未安装")
        print("💡 安装UV可以获得更快的依赖管理体验:")
        print("   pip install uv")
        print("\n⚠️  将使用pip作为备选方案")
        return True  # 这不是严重错误
    
    def _handle_pip_missing(self, error: ErrorInfo) -> bool:
        """处理pip缺失"""
        print("\n📦 Pip包管理器不可用")
        print("💡 修复建议:")
        print("   • 重新安装Python")
        print("   • 或手动安装pip: python -m ensurepip")
        return False
    
    def _handle_dependency_missing(self, error: ErrorInfo) -> bool:
        """处理依赖缺失"""
        print(f"\n📦 缺少依赖包")
        print("💡 将尝试自动安装...")
        return True  # 可以自动修复
    
    def _handle_config_missing(self, error: ErrorInfo) -> bool:
        """处理配置缺失"""
        print("\n⚙️  配置文件缺失")
        print("💡 将创建默认配置...")
        return True  # 可以自动修复
    
    def _handle_dir_missing(self, error: ErrorInfo) -> bool:
        """处理目录缺失"""
        print("\n📁 目录结构不完整")
        print("💡 将自动创建必要目录...")
        return True  # 可以自动修复
    
    def _handle_permission_error(self, error: ErrorInfo) -> bool:
        """处理权限错误"""
        print("\n🔒 权限不足")
        print("💡 解决建议:")
        print("   • Windows: 以管理员身份运行")
        print("   • Linux/Mac: 使用sudo或检查文件权限")
        return False
    
    def _handle_network_error(self, error: ErrorInfo) -> bool:
        """处理网络错误"""
        print("\n🌐 网络连接问题")
        print("💡 解决建议:")
        print("   • 检查网络连接")
        print("   • 检查防火墙设置")
        print("   • 尝试使用代理")
        return False
    
    # 自动修复处理器实现
    def _auto_fix_dependencies(self, error: ErrorInfo) -> bool:
        """自动修复依赖问题"""
        try:
            from .dep_manager import DependencyManager
            dep_manager = DependencyManager(silent=False)
            return dep_manager.install_dependencies()
        except Exception:
            return False
    
    def _auto_fix_config(self, error: ErrorInfo) -> bool:
        """自动修复配置问题"""
        try:
            from .config_manager import ConfigManager
            config_manager = ConfigManager(silent=False)
            config_manager.create_default_config()
            return True
        except Exception:
            return False
    
    def _auto_fix_directories(self, error: ErrorInfo) -> bool:
        """自动修复目录问题"""
        try:
            from .path_manager import PathManager
            path_manager = PathManager(silent=False)
            results = path_manager.create_project_directories()
            return all(results.values())
        except Exception:
            return False


# 全局错误处理器实例
global_error_handler = ErrorHandler()


def handle_exception(exc_type, exc_value, exc_traceback):
    """全局异常处理器"""
    if issubclass(exc_type, KeyboardInterrupt):
        # 用户中断，优雅退出
        print("\n\n👋 操作已取消")
        sys.exit(0)
    
    print("\n" + "="*60)
    print("💥 程序遇到了意外错误")
    print("="*60)
    
    # 显示用户友好的错误信息
    error_msg = str(exc_value)
    if error_msg:
        print(f"\n错误信息: {error_msg}")
    
    # 显示错误类型
    print(f"错误类型: {exc_type.__name__}")
    
    # 显示简化的堆栈跟踪
    print("\n📍 错误位置:")
    tb_lines = traceback.format_tb(exc_traceback)
    if tb_lines:
        # 只显示最后几行相关的堆栈
        relevant_lines = [line for line in tb_lines[-3:] if 'portable' in line or 'universal' in line or 'gui' in line]
        if relevant_lines:
            for line in relevant_lines:
                print(f"   {line.strip()}")
        else:
            print(f"   {tb_lines[-1].strip()}")
    
    print("\n💡 建议:")
    print("   • 检查输入的URL是否正确")
    print("   • 确保网络连接正常")
    print("   • 尝试重新启动程序")
    print("   • 如果问题持续，请查看日志文件")
    
    print("\n" + "="*60)


def install_global_exception_handler():
    """安装全局异常处理器"""
    sys.excepthook = handle_exception