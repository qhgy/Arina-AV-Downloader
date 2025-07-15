@echo off
echo 🌸 多平台视频下载器 v2.0 - 测试脚本
echo ==========================================

cd /d D:\000cc

echo.
echo 📋 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python未安装或不在PATH中
    pause
    exit /b 1
)

echo.
echo 📦 检查核心模块...
if not exist multi_platform_downloader.py (
    echo ❌ 核心模块不存在
    pause
    exit /b 1
)

if not exist enhanced_downloader.py (
    echo ❌ 命令行界面不存在  
    pause
    exit /b 1
)

echo ✅ 所有文件检查通过

echo.
echo 🧪 测试核心模块...
python -c "from multi_platform_downloader import PlatformDetector; print('平台检测测试通过')"
if %errorlevel% neq 0 (
    echo ❌ 核心模块导入失败
    pause
    exit /b 1
)

echo.
echo 📺 测试平台检测功能...
python multi_platform_downloader.py

echo.
echo 🔍 显示支持的平台...
python enhanced_downloader.py --platforms

echo.
echo ⚙️ 显示配置信息...
python enhanced_downloader.py --config

echo.
echo 📖 显示帮助信息...
python enhanced_downloader.py --help

echo.
echo ✅ 所有测试完成！
echo.
echo 💡 使用示例:
echo   基本下载: python enhanced_downloader.py "VIDEO_URL"
echo   音频下载: python enhanced_downloader.py -a "VIDEO_URL"  
echo   查看信息: python enhanced_downloader.py -i "VIDEO_URL"
echo   批量下载: python enhanced_downloader.py -b urls.txt
echo.

pause