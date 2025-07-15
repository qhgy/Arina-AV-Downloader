# Windows环境下Python脚本测试工具

param(
    [string]$VideoUrl = ""
)

Write-Host "🌸 mio酱的YouTube下载器测试工具" -ForegroundColor Magenta
Write-Host "=================================" -ForegroundColor Cyan

# 检查当前环境
Write-Host "`n🔍 环境检查..." -ForegroundColor Yellow
Write-Host "操作系统: $($env:OS)" -ForegroundColor White
Write-Host "当前目录: $(Get-Location)" -ForegroundColor White
Write-Host "PowerShell版本: $($PSVersionTable.PSVersion)" -ForegroundColor White

# 检查Python
Write-Host "`n🐍 Python检查..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ Python未正确安装" -ForegroundColor Red
        return
    }
} catch {
    Write-Host "❌ 无法执行Python命令" -ForegroundColor Red
    return
}

# 检查脚本文件
Write-Host "`n📄 脚本文件检查..." -ForegroundColor Yellow
if (Test-Path "youtube_downloader.py") {
    Write-Host "✅ youtube_downloader.py 存在" -ForegroundColor Green
} else {
    Write-Host "❌ youtube_downloader.py 不存在" -ForegroundColor Red
    return
}

# 检查依赖
Write-Host "`n📦 依赖检查..." -ForegroundColor Yellow
try {
    $ytdlpCheck = python -c "import yt_dlp; print('yt-dlp available')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ yt-dlp 已安装" -ForegroundColor Green
    } else {
        Write-Host "⚠️  yt-dlp 未安装，尝试安装..." -ForegroundColor Yellow
        python -m pip install yt-dlp
    }
} catch {
    Write-Host "❌ 无法检查yt-dlp" -ForegroundColor Red
}

# 测试脚本
Write-Host "`n🧪 测试YouTube下载器..." -ForegroundColor Yellow
try {
    Write-Host "显示帮助信息:" -ForegroundColor Cyan
    python youtube_downloader.py --help
    
    if ($VideoUrl) {
        Write-Host "`n📺 测试视频信息获取..." -ForegroundColor Yellow
        python youtube_downloader.py -i $VideoUrl
    }
    
} catch {
    Write-Host "❌ 脚本执行出错: $_" -ForegroundColor Red
}

Write-Host "`n✅ 测试完成！" -ForegroundColor Green
Write-Host "`n💡 使用提示:" -ForegroundColor Yellow
Write-Host "  基本下载: python youtube_downloader.py 'URL'" -ForegroundColor White
Write-Host "  音频下载: python youtube_downloader.py -a 'URL'" -ForegroundColor White
Write-Host "  查看信息: python youtube_downloader.py -i 'URL'" -ForegroundColor White