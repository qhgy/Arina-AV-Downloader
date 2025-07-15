"""
欢迎向导
Apple式设计：首次运行的优雅体验
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any
from .config_manager import ConfigManager
from .env_checker import EnvChecker
from .dep_manager import DependencyManager
from .utils import print_progress


class WelcomeWizard:
    """欢迎向导 - Apple式首次运行体验"""
    
    def __init__(self):
        self.config_manager = ConfigManager(silent=False)
        self.env_checker = EnvChecker(silent=False)
        self.dep_manager = DependencyManager(silent=False)
        
    def run_first_time_setup(self) -> bool:
        """运行首次设置向导"""
        self._show_welcome()
        
        # 环境检查
        if not self._check_environment():
            return False
        
        # 依赖安装
        if not self._setup_dependencies():
            return False
        
        # 配置初始化
        if not self._initialize_config():
            return False
        
        # 创建目录结构
        if not self._create_directories():
            return False
        
        self._show_completion()
        return True
    
    def _show_welcome(self):
        """显示欢迎信息"""
        print("\n" + "="*60)
        print("🎉 欢迎使用 Universal Video Downloader!")
        print("="*60)
        print()
        print("这是您第一次运行此应用程序。")
        print("我们将为您进行快速设置，让一切准备就绪。")
        print()
        print("⏱️  预计需要 1-2 分钟")
        print("🔧 将自动安装必要的依赖")
        print("📁 将创建必要的目录结构")
        print("⚙️  将生成默认配置文件")
        print()
        
        try:
            input("按 Enter 键开始设置...")
        except KeyboardInterrupt:
            print("\n\n👋 设置已取消")
            sys.exit(0)
        
        print()
    
    def _check_environment(self) -> bool:
        """检查环境"""
        print("🔍 第1步: 环境检查")
        print("-" * 30)
        
        env_info = self.env_checker.check_all()
        
        if self.env_checker.has_critical_errors():
            print("\n❌ 发现严重的环境问题:")
            for error in self.env_checker.get_errors():
                print(f"   • {error.message}")
                print(f"     解决方案: {error.solution}")
            
            print("\n请解决上述问题后重新运行设置。")
            return False
        
        # 自动修复警告
        if self.env_checker.warnings:
            print("\n🔧 正在自动修复一些小问题...")
            if self.env_checker.auto_fix_issues():
                print("✅ 问题已自动修复")
            else:
                print("⚠️  部分问题需要手动处理")
        
        print("\n✅ 环境检查通过!")
        return True
    
    def _setup_dependencies(self) -> bool:
        """设置依赖"""
        print("\n📦 第2步: 安装依赖包")
        print("-" * 30)
        
        # 检查当前依赖状态
        deps_status = self.dep_manager.check_dependencies()
        missing_deps = [pkg for pkg, installed in deps_status.items() if not installed]
        
        if not missing_deps:
            print("✅ 所有必需的依赖包已安装")
            return True
        
        print(f"需要安装 {len(missing_deps)} 个依赖包:")
        for dep in missing_deps:
            print(f"   • {dep}")
        
        print("\n⏳ 正在安装依赖包...")
        print("   这可能需要几分钟时间，请耐心等待...")
        
        if self.dep_manager.install_dependencies(missing_deps):
            print("✅ 依赖包安装完成!")
            return True
        else:
            print("\n❌ 依赖包安装失败")
            print("请检查网络连接或手动安装以下包:")
            for dep in missing_deps:
                print(f"   pip install {dep}")
            return False
    
    def _initialize_config(self) -> bool:
        """初始化配置"""
        print("\n⚙️  第3步: 初始化配置")
        print("-" * 30)
        
        # 生成pyproject.toml
        if self.dep_manager.generate_pyproject_toml():
            print("✅ 已生成 pyproject.toml")
        else:
            print("⚠️  pyproject.toml 生成失败，将使用 requirements.txt")
        
        # 创建默认配置
        config = self.config_manager.create_default_config()
        if config:
            print("✅ 已创建默认配置文件")
            
            # 显示配置摘要
            print("\n📋 配置摘要:")
            print(f"   • 下载目录: {config.get('default_output_dir', './downloads')}")
            print(f"   • 默认质量: {config.get('default_quality', 'best')}")
            print(f"   • 最大并发: {config.get('max_workers', 4)}")
            print(f"   • 支持平台: {len(config.get('platforms', {}))}")
            
            return True
        else:
            print("❌ 配置文件创建失败")
            return False
    
    def _create_directories(self) -> bool:
        """创建目录结构"""
        print("\n📁 第4步: 创建目录结构")
        print("-" * 30)
        
        from .path_manager import PathManager
        path_manager = PathManager(silent=False)
        
        results = path_manager.create_project_directories()
        
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        
        if success_count == total_count:
            print(f"✅ 已创建 {total_count} 个必要目录")
            for dir_name in results.keys():
                print(f"   • {dir_name}/")
            return True
        else:
            print(f"⚠️  创建了 {success_count}/{total_count} 个目录")
            for dir_name, success in results.items():
                status = "✅" if success else "❌"
                print(f"   {status} {dir_name}/")
            return success_count > 0
    
    def _show_completion(self):
        """显示完成信息"""
        print("\n" + "="*60)
        print("🎉 设置完成!")
        print("="*60)
        print()
        print("✅ 环境检查通过")
        print("✅ 依赖包已安装")
        print("✅ 配置文件已创建")
        print("✅ 目录结构已建立")
        print()
        print("🚀 您现在可以开始使用 Universal Video Downloader 了!")
        print()
        print("💡 智能使用提示:")
        print("   • 🎯 双击启动脚本即可运行，无需命令行")
        print("   • 🌐 支持1800+网站，包括YouTube、TikTok等热门平台")
        print("   • 📱 直接粘贴手机分享的链接即可下载")
        print("   • 🎵 支持音频模式，一键提取音频文件")
        print("   • 📦 支持批量下载，一次处理多个链接")
        print()
        print("🔧 下一步建议:")
        print("   1. 尝试下载一个YouTube视频测试功能")
        print("   2. 查看downloads/目录中的下载文件")
        print("   3. 如需登录下载，将cookies放入cookies/目录")
        print()
        print("📚 获取帮助:")
        print("   • 查看 README.md - 3步快速上手指南")
        print("   • 查看 DEVELOPER.md - 开发者详细文档")
        print("   • 运行 python run_tests.py - 环境诊断")
        print()
        
        # 智能建议下一步操作
        print("🎯 智能建议:")
        try:
            # 检测是否有GUI支持
            gui_available = False
            try:
                import PyQt6
                gui_available = True
            except ImportError:
                try:
                    import PySide6
                    gui_available = True
                except ImportError:
                    pass
            
            if gui_available:
                print("   • 推荐使用图形界面，操作更直观")
                print("   • 将自动启动GUI模式")
            else:
                print("   • 当前为命令行模式")
                print("   • 可安装PyQt6启用图形界面: pip install PyQt6")
        except Exception:
            pass
        
        print()
        try:
            input("按 Enter 键继续启动应用程序...")
        except KeyboardInterrupt:
            print("\n\n👋 再见!")
            sys.exit(0)


def check_first_run() -> bool:
    """检查是否为首次运行"""
    project_root = Path(__file__).parent.parent
    config_file = project_root / "downloader_config.json"
    
    # 如果配置文件不存在，认为是首次运行
    return not config_file.exists()


def run_welcome_wizard_if_needed() -> bool:
    """如果需要，运行欢迎向导"""
    if check_first_run():
        wizard = WelcomeWizard()
        return wizard.run_first_time_setup()
    return True


if __name__ == "__main__":
    if check_first_run():
        wizard = WelcomeWizard()
        success = wizard.run_first_time_setup()
        sys.exit(0 if success else 1)
    else:
        print("✅ 应用程序已配置完成")
        sys.exit(0)