@echo off
echo ===== GUI Download Debug Launcher =====
echo.
echo This will show detailed debug output to help fix download issues
echo.

cd /d D:\000cc

echo Checking yt-dlp installation...
python -c "import yt_dlp; print('yt-dlp version:', yt_dlp.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo Installing yt-dlp...
    pip install yt-dlp
)

echo.
echo Launching GUI with debug output...
echo Watch the console for debug messages when you start a download.
echo.

python gui_downloader.py

echo.
echo GUI closed. Check above for any error messages.
pause