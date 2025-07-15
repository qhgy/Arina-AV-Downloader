# Universal Video Downloader - PySide6 GUI PowerShell启动脚本
# 全新Apple风格界面，简洁易用

# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# 设置窗口标题
$Host.UI.RawUI.WindowTitle = "Universal Video Downloader - PySide6 GUI"

# 清屏并显示标题
Clear-Host
Write-Host ""
Write-Host "========================================" -ForegroundColor Blue
Write-Host "   🎬 Universal Video Downloader" -ForegroundColor Blue
Write-Host "   全新PySide6 Apple风格界面" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

# 切换到脚本所在目录
Set-Location $PSScriptRoot

# 检查Python是否可用
function Test-Python {
    try {
        $pythonVersion = python --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ 找到Python: $pythonVersion" -ForegroundColor Green
            return $true
        }
    }
    catch {
        # Python命令不存在
    }
    
    Write-Host "❌ 错误: 未找到Python" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 解决方案:" -ForegroundColor Yellow
    Write-Host "   1. 请安装Python 3.8或更高版本"
    Write-Host "   2. 确保Python已添加到系统PATH"
    Write-Host "   3. 从 https://python.org 下载安装"
    Write-Host ""
    Read-Host "按Enter键退出"
    return $false
}

# 检查PySide6是否安装
function Test-PySide6 {
    Write-Host "🔍 检查PySide6..." -ForegroundColor Cyan
    
    try {
        $result = python -c "import PySide6; print('PySide6 available')" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ PySide6 已安装" -ForegroundColor Green
            return $true
        }
    }
    catch {
        # PySide6不可用
    }
    
    Write-Host "❌ PySide6 未安装" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 正在自动安装PySide6..." -ForegroundColor Yellow
    
    try {
        # 尝试使用uv安装
        $uvResult = uv pip install PySide6 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ PySide6 安装成功 (使用uv)" -ForegroundColor Green
            return $true
        }
        
        # 回退到pip
        Write-Host "⚠️  uv不可用，使用pip安装..." -ForegroundColor Yellow
        $pipResult = python -m pip install PySide6
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ PySide6 安装成功 (使用pip)" -ForegroundColor Green
            return $true
        }
        
        Write-Host "❌ PySide6 安装失败" -ForegroundColor Red
        Write-Host ""
        Write-Host "💡 请手动安装:" -ForegroundColor Yellow
        Write-Host "   uv pip install PySide6" -ForegroundColor White
        Write-Host "   或者: python -m pip install PySide6" -ForegroundColor White
        Write-Host ""
        Read-Host "按Enter键退出"
        return $false
        
    }
    catch {
        Write-Host "❌ 安装过程出错: $_" -ForegroundColor Red
        Read-Host "按Enter键退出"
        return $false
    }
}

# 启动GUI应用程序
function Start-PySide6GUI {
    Write-Host ""
    Write-Host "🚀 启动PySide6 GUI..." -ForegroundColor Blue
    Write-Host ""
    
    try {
        # 启动PySide6 GUI
        python pyside6_gui.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "👋 感谢使用 Universal Video Downloader" -ForegroundColor Green
            return $true
        } else {
            Write-Host ""
            Write-Host "❌ GUI启动失败" -ForegroundColor Red
            Write-Host "💡 请检查错误信息并重试" -ForegroundColor Yellow
            Write-Host ""
            Read-Host "按Enter键退出"
            return $false
        }
    }
    catch {
        Write-Host ""
        Write-Host "❌ GUI启动过程中出错: $_" -ForegroundColor Red
        Read-Host "按Enter键退出"
        return $false
    }
}

# 主函数
function Main {
    try {
        # 检查Python
        if (-not (Test-Python)) {
            exit 1
        }
        
        # 检查PySide6
        if (-not (Test-PySide6)) {
            exit 1
        }
        
        # 启动GUI
        if (-not (Start-PySide6GUI)) {
            exit 1
        }
        
        # 如果是双击运行，暂停以便用户看到消息
        if ($MyInvocation.InvocationName -ne "&") {
            Read-Host "按Enter键退出"
        }
        
        exit 0
    }
    catch {
        Write-Host ""
        Write-Host "❌ 启动过程被中断: $_" -ForegroundColor Red
        Read-Host "按Enter键退出"
        exit 1
    }
}

# 错误处理
trap {
    Write-Host ""
    Write-Host "❌ 发生意外错误: $_" -ForegroundColor Red
    Read-Host "按Enter键退出"
    exit 1
}

# 运行主函数
Main
