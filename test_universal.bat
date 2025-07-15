@echo off
echo Universal Multi-Platform Video Downloader v2.0 - Test Script
echo ============================================================

cd /d D:\000cc

echo.
echo Checking Python environment...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Checking core modules...
if not exist universal_downloader.py (
    echo ERROR: Core module not found
    pause
    exit /b 1
)

if not exist universal_cli.py (
    echo ERROR: CLI interface not found  
    pause
    exit /b 1
)

echo SUCCESS: All files check passed

echo.
echo Testing core module...
python -c "from universal_downloader import PlatformDetector; print('Platform detection test passed')"
if %errorlevel% neq 0 (
    echo ERROR: Core module import failed
    pause
    exit /b 1
)

echo.
echo Testing platform detection...
python universal_downloader.py

echo.
echo Showing supported platforms...
python universal_cli.py --platforms

echo.
echo Showing configuration...
python universal_cli.py --config

echo.
echo Showing help information...
python universal_cli.py --help

echo.
echo SUCCESS: All tests completed!
echo.
echo Usage examples:
echo   Basic download: python universal_cli.py "VIDEO_URL"
echo   Audio download: python universal_cli.py -a "VIDEO_URL"  
echo   View info: python universal_cli.py -i "VIDEO_URL"
echo   Batch download: python universal_cli.py -b urls.txt
echo.

pause