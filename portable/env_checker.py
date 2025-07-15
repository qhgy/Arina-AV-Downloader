"""
环境检测器
Apple式用户体验：静默检查，智能修复，优雅提示
"""

import sys
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from .models import EnvironmentInfo, SystemPlatform, PackageManager, ErrorInfo, ProjectStructure
from .utils import (
    detect_system_platform, 
    get_python_version, 
    is_python_version_compatible,
    find_project_root,
    ensure_directory,
    is_command_available,
    get_friendly_error_message,
    print_welcome_message,
    print_success_message,
    print_progress
)
from .error_handler import global_error_handler


class EnvChecker:
    """环境检测器 - Apple式设计：开箱即用，静默智能"""
    
    def __init__(self, silent: bool = False):
        self.silent = silent
        self.errors: List[ErrorInfo] = []
        self.warnings: List[ErrorInfo] = []
        self.project_root = find_project_root()
        
    def check_all(self) -> EnvironmentInfo:
        """执行完整的环境检查"""
        if not self.silent:
            print_welcome_message()
            
        # 检查Python版本
        python_version = get_python_version()
        python_ok = self._check_python_version()
        
        # 检查系统平台
        platform = detect_system_platform()
        
        # 检查包管理器
        package_manager = self._check_package_managers()
        
        # 检查依赖
        dependencies_status = self._check_dependencies()
        
        # 检查配置
        config_status = self._check_config()
        
        # 检查目录结构
        directories_status = self._check_directories()
        
        env_info = EnvironmentInfo(
            python_version=python_version,
            platform=platform,
            project_root=self.project_root,
            package_manager=package_manager,
            dependencies_status=dependencies_status,
            config_status=config_status,
            directories_status=directories_status
        )
        
        if not self.silent:
            self._print_summary(env_info)
            
        return env_info
    
    def _check_python_version(self) -> bool:
        """检查Python版本"""
        if not self.silent:
            print_progress("检查Python版本...")
            
        if not is_python_version_compatible("3.8"):
            error = ErrorInfo(
                code="python_version",
                message=get_friendly_error_message("python_version"),
                solution="请升级到Python 3.8或更高版本",
                severity="error"
            )
            self.errors.append(error)
            return False
        
        return True
    
    def _check_package_managers(self) -> PackageManager:
        """检查包管理器可用性"""
        if not self.silent:
            print_progress("检查包管理器...")
            
        # 优先检查uv
        if is_command_available("uv"):
            return PackageManager.UV
        
        # 回退到pip
        if is_command_available("pip"):
            warning = ErrorInfo(
                code="uv_missing",
                message=get_friendly_error_message("uv_missing"),
                solution="建议安装uv以获得更好的性能: pip install uv",
                severity="warning",
                auto_fixable=True
            )
            self.warnings.append(warning)
            return PackageManager.PIP
        
        # 都不可用
        error = ErrorInfo(
            code="pip_missing",
            message=get_friendly_error_message("pip_missing"),
            solution="请重新安装Python或修复pip",
            severity="error"
        )
        self.errors.append(error)
        return PackageManager.NONE
    
    def _check_dependencies(self) -> Dict[str, bool]:
        """检查依赖包状态"""
        if not self.silent:
            print_progress("检查依赖包...")
            
        required_packages = ["yt-dlp"]
        optional_packages = ["PyQt6", "PySide6"]
        
        status = {}
        
        # 检查必需依赖
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                status[package] = True
            except ImportError:
                status[package] = False
                
        # 检查可选依赖（GUI）
        gui_available = False
        for package in optional_packages:
            try:
                __import__(package)
                status[package] = True
                gui_available = True
                break
            except ImportError:
                status[package] = False
                
        if not gui_available:
            warning = ErrorInfo(
                code="gui_missing",
                message="GUI依赖缺失，将只能使用命令行模式",
                solution="安装PyQt6或PySide6以启用图形界面",
                severity="warning",
                auto_fixable=True
            )
            self.warnings.append(warning)
            
        return status
    
    def _check_config(self) -> bool:
        """检查配置文件"""
        if not self.silent:
            print_progress("检查配置文件...")
            
        config_file = self.project_root / "downloader_config.json"
        
        if not config_file.exists():
            warning = ErrorInfo(
                code="config_missing",
                message=get_friendly_error_message("config_missing"),
                solution="将自动创建默认配置文件",
                severity="warning",
                auto_fixable=True
            )
            self.warnings.append(warning)
            return False
            
        return True
    
    def _check_directories(self) -> Dict[str, bool]:
        """检查目录结构"""
        if not self.silent:
            print_progress("检查目录结构...")
            
        status = {}
        
        for dir_name in ProjectStructure.REQUIRED_DIRS:
            dir_path = self.project_root / dir_name
            status[dir_name] = dir_path.exists()
            
            if not status[dir_name]:
                warning = ErrorInfo(
                    code="dir_missing",
                    message=f"目录 {dir_name} 不存在",
                    solution="将自动创建必要目录",
                    severity="warning",
                    auto_fixable=True
                )
                self.warnings.append(warning)
                
        return status
    
    def auto_fix_issues(self) -> bool:
        """自动修复可修复的问题（静默自愈）"""
        if not self.silent:
            print_progress("正在自动修复问题...")
        
        # 使用全局错误处理器进行静默自愈
        all_issues = self.errors + self.warnings
        auto_fixable_issues = [issue for issue in all_issues if issue.auto_fixable]
        
        if auto_fixable_issues:
            if not self.silent:
                print_progress(f"发现 {len(auto_fixable_issues)} 个可自动修复的问题")
            
            # 静默修复
            fix_results = global_error_handler.auto_fix_errors(auto_fixable_issues)
            success_count = sum(1 for success in fix_results.values() if success)
            
            if not self.silent:
                print_progress(f"成功修复 {success_count}/{len(auto_fixable_issues)} 个问题")
            
            return success_count == len(auto_fixable_issues)
        
        return True
    
    def _print_summary(self, env_info: EnvironmentInfo):
        """打印检查摘要"""
        print("\n" + "="*50)
        print("🔍 环境检查报告")
        print("="*50)
        
        print(f"Python版本: {env_info.python_version}")
        print(f"系统平台: {env_info.platform.value}")
        print(f"项目根目录: {env_info.project_root}")
        print(f"包管理器: {env_info.package_manager.value}")
        
        # 显示错误
        if self.errors:
            print("\n❌ 发现错误:")
            for error in self.errors:
                print(f"  • {error.message}")
                print(f"    解决方案: {error.solution}")
                
        # 显示警告
        if self.warnings:
            print("\n⚠️  警告信息:")
            for warning in self.warnings:
                print(f"  • {warning.message}")
                if warning.auto_fixable:
                    print(f"    将自动修复: {warning.solution}")
                    
        # 显示状态
        if env_info.is_ready:
            print("\n✅ 环境检查通过，一切就绪！")
        else:
            print("\n🔧 需要修复一些问题...")
            
        print("="*50)
    
    def get_errors(self) -> List[ErrorInfo]:
        """获取错误列表"""
        return self.errors
    
    def get_warnings(self) -> List[ErrorInfo]:
        """获取警告列表"""
        return self.warnings
    
    def has_critical_errors(self) -> bool:
        """是否有严重错误"""
        return len(self.errors) > 0


def main():
    """主入口函数 - 用于独立运行环境检查"""
    # 检查是否为首次运行
    from .welcome_wizard import check_first_run, run_welcome_wizard_if_needed
    
    if check_first_run():
        # 首次运行，启动欢迎向导
        success = run_welcome_wizard_if_needed()
        sys.exit(0 if success else 1)
    
    # 常规环境检查
    checker = EnvChecker(silent=False)
    env_info = checker.check_all()
    
    if checker.has_critical_errors():
        print("\n❌ 发现严重错误，无法继续运行")
        print("请根据上述提示解决问题后重试")
        sys.exit(1)
    
    # 尝试自动修复警告
    if checker.warnings:
        print("\n🔧 正在自动修复问题...")
        if checker.auto_fix_issues():
            print("✅ 问题修复完成")
        else:
            print("⚠️  部分问题无法自动修复")
    
    print_success_message()
    return 0


if __name__ == "__main__":
    # 修复相对导入问题
    import sys
    from pathlib import Path
    
    # 添加项目根目录到路径
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # 避免重复导入警告，直接调用main函数
    main()