@echo off
echo ================================================================
echo      FIXED GUI - Should work now that CLI download succeeded
echo ================================================================
echo.
echo Changes made:
echo  - Fixed thread safety issues in progress callbacks
echo  - Added proper error handling and logging
echo  - Fixed working directory problems
echo  - Added timeout protection
echo  - Improved lambda closure handling
echo.
echo Your test URL: https://cn.pornhub.com/view_video.php?viewkey=68543d832ddd2
echo.

cd /d D:\000cc

echo Launching FIXED GUI...
echo Watch the console output for detailed debugging info.
echo.

python gui_downloader.py

echo.
echo GUI session ended.
echo Check the console output above for any errors.
pause