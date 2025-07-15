@echo off
echo Testing downloader dependencies...
echo.

echo Checking yt-dlp...
python -c "import yt_dlp; print('yt-dlp OK')" 2>nul
if %errorlevel% neq 0 (
    echo yt-dlp not found, installing...
    pip install yt-dlp
)

echo.
echo Checking universal_downloader...
python -c "from universal_downloader import DownloadManager; print('universal_downloader OK')" 2>nul
if %errorlevel% neq 0 (
    echo universal_downloader import failed
)

echo.
echo Checking speed_optimizer...
python -c "from speed_optimizer import HighSpeedDownloader; print('speed_optimizer OK')" 2>nul
if %errorlevel% neq 0 (
    echo speed_optimizer import failed
)

echo.
echo Testing GUI imports...
python -c "from gui_downloader import ModernVideoDownloader; print('GUI imports OK')" 2>nul
if %errorlevel% neq 0 (
    echo GUI imports failed
)

echo.
echo Dependency check completed.
pause