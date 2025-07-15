#!/bin/bash
# Universal Video Downloader - 简化启动脚本
# 使用Python处理复杂逻辑，保持跨平台一致性

# 设置UTF-8编码
export LANG=C.UTF-8
export LC_ALL=C.UTF-8

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 切换到脚本所在目录
cd "$(dirname "$0")"

# 设置执行权限
if [ ! -x "$0" ]; then
    chmod +x "$0" 2>/dev/null
fi

# 检查Python是否可用
check_python() {
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_CMD="python3"
    elif command -v python >/dev/null 2>&1; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}Error: Python not found${NC}"
        echo
        echo -e "${YELLOW}Solution:${NC}"
        echo "   1. Install Python 3.8 or higher"
        echo "   2. Ubuntu/Debian: sudo apt install python3"
        echo "   3. macOS: brew install python3"
        echo "   4. Or use the Python launcher: python3 launcher.py"
        echo
        read -p "Press Enter to exit..."
        exit 1
    fi
}

# 主函数
main() {
    # 显示简单标题
    echo -e "${BLUE}🎬 Universal Video Downloader${NC}"
    echo "   Starting up..."
    echo
    
    # 检查Python
    check_python
    
    # 使用Python启动器处理复杂逻辑
    echo "Using Python launcher for better compatibility..."
    $PYTHON_CMD launcher.py
    
    exit_code=$?
    
    # 如果是交互式运行，等待用户确认
    if [ -t 0 ]; then
        if [ $exit_code -ne 0 ]; then
            read -p "Press Enter to exit..."
        fi
    fi
    
    exit $exit_code
}

# 错误处理
trap 'echo -e "\n${RED}Startup interrupted${NC}"; exit 1' INT TERM

# 运行主函数
main "$@"