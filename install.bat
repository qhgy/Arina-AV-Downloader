@echo off
chcp 65001 >nul
echo.
echo ========================================
echo 🌸 Arina AV Downloader 一键安装脚本
echo Thanks to Arina for 10 years of companionship 💕
echo ========================================
echo.

echo 📋 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未检测到Python环境！
    echo 请先安装Python 3.8+：https://www.python.org/downloads/
    echo 安装时请勾选 "Add Python to PATH" 选项
    pause
    exit /b 1
)

echo ✅ Python环境检查通过
python --version

echo.
echo 📦 升级pip...
python -m pip install --upgrade pip

echo.
echo 📥 安装依赖包...
echo 这可能需要几分钟时间，请耐心等待...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ⚠️ 安装失败，尝试使用国内镜像源...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
)

if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败！
    echo 请检查网络连接或手动执行：pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo ✅ 安装完成！
echo.
echo 🚀 启动选项：
echo 1. GUI图形界面：python arina_gui.py
echo 2. CLI命令行：python arina_cli.py --help
echo.
echo 📖 详细使用说明请查看：USER_GUIDE.md
echo.

set /p choice="是否现在启动GUI版本？(y/n): "
if /i "%choice%"=="y" (
    echo 启动GUI版本...
    python arina_gui.py
) else (
    echo 安装完成！可以手动运行程序。
)

pause
