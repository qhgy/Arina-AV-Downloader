@echo off
echo Testing UI Progress Updates...
echo.
echo The progress bar should now update properly during download.
echo You should see:
echo 1. "Initializing download..." at 1%
echo 2. "Downloading: [title]..." with increasing progress
echo 3. "Download Complete!" at 100%
echo 4. Final status with file name and size
echo.

cd /d D:\000cc
python gui_downloader.py

echo.
pause