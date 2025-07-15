# Universal Video Downloader - PowerShell启动脚本
# 处理复杂逻辑和中文显示

# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# 设置窗口标题
$Host.UI.RawUI.WindowTitle = "Universal Video Downloader - 启动中..."

# 清屏并显示标题
Clear-Host
Write-Host ""
Write-Host "========================================" -ForegroundColor Blue
Write-Host "   🎬 Universal Video Downloader" -ForegroundColor Blue
Write-Host "   开箱即用的多平台视频下载器" -ForegroundColor Blue
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

# 显示进度动画
function Show-Progress {
    param([string]$Message, [int]$Duration = 2)
    
    Write-Host "⏳ $Message" -NoNewline -ForegroundColor Cyan
    for ($i = 0; $i -lt $Duration; $i++) {
        Start-Sleep -Milliseconds 500
        Write-Host "." -NoNewline -ForegroundColor Cyan
    }
    Write-Host ""
}

# 运行环境检查
function Start-EnvironmentCheck {
    Show-Progress "正在检查环境" 3
    
    try {
        $result = python -m portable.env_checker
        if ($LASTEXITCODE -ne 0) {
            Write-Host ""
            Write-Host "❌ 环境检查失败" -ForegroundColor Red
            Write-Host "💡 请根据上述提示解决问题后重试" -ForegroundColor Yellow
            Write-Host ""
            Read-Host "按Enter键退出"
            return $false
        }
        return $true
    }
    catch {
        Write-Host ""
        Write-Host "❌ 环境检查过程中出错: $_" -ForegroundColor Red
        Read-Host "按Enter键退出"
        return $false
    }
}

# 启动应用程序
function Start-Application {
    Write-Host ""
    Write-Host "✅ 环境检查完成" -ForegroundColor Green
    Write-Host "🚀 正在启动应用程序..." -ForegroundColor Blue
    Write-Host ""
    
    # 尝试启动GUI版本
    try {
        python gui_downloader.py 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "⚠️  GUI启动失败，尝试命令行版本..." -ForegroundColor Yellow
            Write-Host ""
            
            # 启动命令行版本
            python universal_downloader.py
            if ($LASTEXITCODE -ne 0) {
                Write-Host ""
                Write-Host "❌ 应用程序启动失败" -ForegroundColor Red
                Write-Host "💡 请检查依赖是否正确安装" -ForegroundColor Yellow
                Write-Host ""
                Read-Host "按Enter键退出"
                return $false
            }
        }
        return $true
    }
    catch {
        Write-Host ""
        Write-Host "❌ 启动过程中出错: $_" -ForegroundColor Red
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
        
        # 环境检查
        if (-not (Start-EnvironmentCheck)) {
            exit 1
        }
        
        # 启动应用
        if (-not (Start-Application)) {
            exit 1
        }
        
        Write-Host ""
        Write-Host "👋 感谢使用 Universal Video Downloader" -ForegroundColor Green
        
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