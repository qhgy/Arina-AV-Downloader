@echo off
echo ===== Batch Download GUI Test =====
echo.
echo New features:
echo - Multi-line URL input (paste multiple URLs, one per line)
echo - Automatic platform detection for each URL
echo - Batch download with progress tracking
echo - Support for mixed platforms (YouTube + PornHub + Twitter, etc.)
echo.
echo How to use:
echo 1. Paste multiple URLs in the text area (one per line)
echo 2. GUI will show "Found X URLs (platforms)"
echo 3. Click "Download Video(s)" for batch download
echo 4. Confirm batch download dialog
echo 5. Watch progress for each download
echo.

cd /d D:\000cc
python gui_downloader.py

echo.
pause