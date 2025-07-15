@echo off
:: Universal Video Downloader - Apple Style GUI Launcher
:: Clean, Beautiful, Foolproof Operation

title Universal Video Downloader - Apple GUI

echo.
echo ========================================
echo    Video Downloader - Apple Style GUI
echo    Simple and Beautiful Interface
echo ========================================
echo.

:: Switch to script directory
cd /d "%~dp0"

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found
    echo.
    echo [SOLUTION] Please install Python 3.8 or higher
    echo Download from: https://python.org
    echo.
    pause
    exit /b 1
)

echo [OK] Python available

:: Check PySide6
python -c "import PySide6" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] PySide6 not installed
    echo.
    echo [INFO] Auto-installing PySide6...
    
    :: Try using uv first
    uv pip install PySide6 >nul 2>&1
    if %errorlevel% neq 0 (
        echo [INFO] uv not available, using pip...
        python -m pip install PySide6
        if %errorlevel% neq 0 (
            echo [ERROR] PySide6 installation failed
            echo.
            echo [SOLUTION] Please install manually: python -m pip install PySide6
            echo.
            pause
            exit /b 1
        )
    )
    echo [OK] PySide6 installed successfully
) else (
    echo [OK] PySide6 available
)

echo.
echo [INFO] Starting Apple Style GUI...
echo.

:: Launch GUI
python perfect_apple_gui.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Perfect GUI launch failed
    echo [INFO] Trying fixed version...
    echo.
    python fixed_apple_gui.py

    if %errorlevel% neq 0 (
        echo.
        echo [INFO] Trying simple version...
        echo.
        python simple_apple_gui.py

        if %errorlevel% neq 0 (
            echo.
            echo [INFO] Trying test version...
            echo.
            python test_pyside6_gui.py
        )
    )
)

echo.
echo Thank you for using Universal Video Downloader
pause
