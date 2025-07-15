#!/usr/bin/env python3
"""
测试运行器
运行所有单元测试和集成测试
"""

import sys
import unittest
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def run_unit_tests():
    """运行单元测试"""
    print("🧪 运行单元测试...")
    print("=" * 50)
    
    # 发现并运行测试
    loader = unittest.TestLoader()
    start_dir = project_root / 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def run_integration_tests():
    """运行集成测试"""
    print("\n🔗 运行集成测试...")
    print("=" * 50)
    
    # 集成测试
    try:
        from portable.env_checker import EnvChecker
        from portable.dep_manager import DependencyManager
        from portable.path_manager import PathManager
        from portable.config_manager import ConfigManager
        
        print("✅ 模块导入测试通过")
        
        # 测试环境检查
        env_checker = EnvChecker(silent=True)
        env_info = env_checker.check_all()
        print(f"✅ 环境检查测试通过 (Python {env_info.python_version})")
        
        # 测试路径管理
        path_manager = PathManager(silent=True)
        project_root = path_manager.get_project_root()
        print(f"✅ 路径管理测试通过 (根目录: {project_root})")
        
        # 测试配置管理
        config_manager = ConfigManager(silent=True)
        config = config_manager.load_config()
        print("✅ 配置管理测试通过")
        
        # 测试依赖管理
        dep_manager = DependencyManager(silent=True)
        deps_status = dep_manager.check_dependencies()
        print(f"✅ 依赖管理测试通过 (检查了 {len(deps_status)} 个包)")
        
        return True
        
    except Exception as e:
        print(f"❌ 集成测试失败: {str(e)}")
        return False


def run_portable_deployment_test():
    """运行可移植性部署测试"""
    print("\n📦 运行可移植性测试...")
    print("=" * 50)
    
    try:
        # 测试项目结构
        required_files = [
            "start.bat",
            "start.sh", 
            "pyproject.toml",
            "requirements.txt",
            "portable/__init__.py"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not (project_root / file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            print(f"❌ 缺少必要文件: {', '.join(missing_files)}")
            return False
        
        print("✅ 项目结构完整")
        
        # 测试启动脚本
        start_bat = project_root / "start.bat"
        start_sh = project_root / "start.sh"
        
        if start_bat.exists():
            print("✅ Windows启动脚本存在")
        
        if start_sh.exists():
            print("✅ Linux/Mac启动脚本存在")
        
        # 测试配置文件
        pyproject = project_root / "pyproject.toml"
        if pyproject.exists():
            print("✅ pyproject.toml配置文件存在")
        
        requirements = project_root / "requirements.txt"
        if requirements.exists():
            print("✅ requirements.txt回退文件存在")
        
        return True
        
    except Exception as e:
        print(f"❌ 可移植性测试失败: {str(e)}")
        return False


def main():
    """主测试函数"""
    print("🎬 Universal Video Downloader - 测试套件")
    print("=" * 60)
    
    all_passed = True
    
    # 运行单元测试
    if not run_unit_tests():
        all_passed = False
    
    # 运行集成测试
    if not run_integration_tests():
        all_passed = False
    
    # 运行可移植性测试
    if not run_portable_deployment_test():
        all_passed = False
    
    # 显示结果
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过!")
        print("✅ 项目已准备好进行可移植部署")
    else:
        print("❌ 部分测试失败")
        print("请检查上述错误信息并修复问题")
    
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 测试已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试运行器出错: {str(e)}")
        sys.exit(1)