@echo off
echo ===== PornHub Download Test =====
echo.
echo Testing the provided PornHub URL to identify download issues
echo URL: https://cn.pornhub.com/view_video.php?viewkey=68543d832ddd2
echo.

cd /d D:\000cc

echo Running comprehensive test...
echo.

python test_pornhub.py

echo.
echo Test completed. Check results above.
echo.
echo If the test failed due to age restriction, you may need to:
echo 1. Export cookies from your browser after logging into PornHub
echo 2. Use the GUI cookie management feature to import them
echo.
pause