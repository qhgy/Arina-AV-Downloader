@echo off
echo 🔍 Windows环境诊断工具
echo ========================

echo.
echo 📋 检查Python环境:
python --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python未安装或不在PATH中
) else (
    echo ✅ Python已安装
)

echo.
echo 📋 检查环境变量:
echo TERM = %TERM%
echo SHELL = %SHELL%
echo MSYSTEM = %MSYSTEM%
echo CYGWIN = %CYGWIN%

echo.
echo 📋 检查是否存在Cygwin相关路径:
echo PATH 中的可疑路径:
echo %PATH% | findstr /i "cygwin"
echo %PATH% | findstr /i "msys"
echo %PATH% | findstr /i "git"

echo.
echo 📋 检查当前工作目录:
echo %CD%

echo.
echo 📋 尝试直接运行Python脚本:
if exist youtube_downloader.py (
    echo ✅ 脚本文件存在
    echo 尝试运行帮助命令...
    python youtube_downloader.py --help
) else (
    echo ❌ 脚本文件不存在
)

echo.
echo 诊断完成！
pause