@echo off
:: Universal Video Downloader - Apple GUI Launcher
:: Clean, Beautiful, Foolproof Operation

:: Set UTF-8 encoding for Chinese characters
chcp 65001 >nul 2>&1

title Universal Video Downloader - Apple GUI

echo.
echo ========================================
echo    Video Downloader - Apple Style GUI
echo    Simple and Beautiful Interface
echo ========================================
echo.

:: 切换到脚本所在目录
cd /d "%~dp0"

:: 检查Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到Python
    echo.
    echo 💡 请安装Python 3.8或更高版本
    echo    下载地址: https://python.org
    echo.
    pause
    exit /b 1
)

echo ✓ Python 可用

:: 检查PySide6
python -c "import PySide6" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PySide6 未安装
    echo.
    echo 💡 正在自动安装PySide6...
    
    :: 尝试使用uv安装
    uv pip install PySide6 >nul 2>&1
    if %errorlevel% neq 0 (
        echo ⚠️  uv不可用，使用pip安装...
        python -m pip install PySide6
        if %errorlevel% neq 0 (
            echo ❌ PySide6 安装失败
            echo.
            echo 💡 请手动安装: python -m pip install PySide6
            echo.
            pause
            exit /b 1
        )
    )
    echo ✅ PySide6 安装成功
) else (
    echo ✓ PySide6 可用
)

echo.
echo 🚀 启动Apple风格GUI...
echo.

:: 启动GUI
python pyside6_gui.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ GUI启动失败
    echo 💡 尝试测试版本...
    echo.
    python test_pyside6_gui.py
)

echo.
echo 👋 感谢使用 Universal Video Downloader
pause
