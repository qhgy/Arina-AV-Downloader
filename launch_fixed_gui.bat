@echo off
echo ================================================================
echo        Universal Video Downloader - FIXED VERSION
echo ================================================================
echo.
echo This version includes fixes for:
echo  • PornHub age-restricted content
echo  • Geo-restriction bypass
echo  • Improved error messages
echo  • Fallback downloader system
echo  • Windows display compatibility
echo.
echo Your test URL: https://cn.pornhub.com/view_video.php?viewkey=68543d832ddd2
echo.

cd /d D:\000cc

echo Checking yt-dlp installation...
python -c "import yt_dlp; print('yt-dlp version:', yt_dlp.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo Installing yt-dlp...
    pip install yt-dlp
    echo.
)

echo Launching Fixed GUI with PornHub optimizations...
echo.
echo INSTRUCTIONS:
echo 1. The GUI will auto-detect downloader type (Advanced or Simple)
echo 2. Paste your URL (already copied for you)
echo 3. Try "Video Info" first to test connectivity
echo 4. If it fails with age-restriction, use Cookie Management
echo 5. Import cookies from logged-in PornHub session
echo.

python gui_downloader.py

echo.
echo GUI session ended.
echo.
echo If downloads still fail:
echo 1. Age-restricted content needs cookies (use Cookie Management in GUI)
echo 2. Check your internet connection
echo 3. The video might be private or removed
echo.
pause