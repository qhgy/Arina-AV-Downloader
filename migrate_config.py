#!/usr/bin/env python3
"""
配置迁移脚本
将现有配置迁移为可移植格式
"""

import sys
from pathlib import Path

# 添加portable模块到路径
sys.path.insert(0, str(Path(__file__).parent))

from portable.config_manager import ConfigManager
from portable.path_manager import PathManager


def main():
    """主迁移函数"""
    print("🔄 Universal Video Downloader - 配置迁移工具")
    print("=" * 50)
    print()
    
    config_manager = ConfigManager(silent=False)
    path_manager = PathManager(silent=False)
    
    # 检查是否有现有配置需要迁移
    config_file = Path("downloader_config.json")
    
    if not config_file.exists():
        print("✅ 没有找到需要迁移的配置文件")
        print("将创建新的默认配置...")
        config_manager.create_default_config()
        print("✅ 默认配置已创建")
        return 0
    
    print("📁 发现现有配置文件，开始迁移...")
    
    # 备份原配置
    backup_path = path_manager.backup_config(config_file)
    if backup_path:
        print(f"✅ 原配置已备份到: {backup_path}")
    
    # 执行迁移
    success = config_manager.migrate_config()
    
    if success:
        print("✅ 配置迁移完成!")
        
        # 显示迁移摘要
        config = config_manager.load_config()
        print("\n📋 迁移后的配置摘要:")
        print(f"   • 下载目录: {config.get('default_output_dir', './downloads')}")
        print(f"   • 默认质量: {config.get('default_quality', 'best')}")
        print(f"   • 最大并发: {config.get('max_workers', 4)}")
        print(f"   • 支持平台: {len(config.get('platforms', {}))}")
        
        # 检查错误和警告
        errors = config_manager.get_errors()
        if errors:
            print("\n⚠️  迁移过程中的注意事项:")
            for error in errors:
                print(f"   • {error.message}")
        
        print("\n🎉 迁移成功完成!")
        print("现在您的配置已经完全可移植了。")
        
    else:
        print("❌ 配置迁移失败")
        print("请检查错误信息并手动处理")
        
        errors = config_manager.get_errors()
        if errors:
            print("\n错误详情:")
            for error in errors:
                print(f"   • {error.message}")
                print(f"     解决方案: {error.solution}")
        
        return 1
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 迁移已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 迁移过程中发生错误: {str(e)}")
        sys.exit(1)