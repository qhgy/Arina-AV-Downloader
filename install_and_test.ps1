# YouTube下载器 - Windows安装和测试脚本

Write-Host "🌸 YouTube下载器安装测试脚本" -ForegroundColor Magenta
Write-Host "================================" -ForegroundColor Cyan

# 检查Python
Write-Host "`n📋 检查Python环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python版本: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 未找到Python，请先安装Python 3.7+" -ForegroundColor Red
    exit 1
}

# 检查是否有uv
Write-Host "`n📦 检查包管理器..." -ForegroundColor Yellow
$hasUv = $false
try {
    $uvVersion = uv --version 2>&1
    Write-Host "✅ 检测到uv: $uvVersion" -ForegroundColor Green
    $hasUv = $true
} catch {
    Write-Host "⚠️  未检测到uv，将使用pip安装依赖" -ForegroundColor Yellow
}

# 安装依赖
Write-Host "`n🔧 安装依赖..." -ForegroundColor Yellow
if ($hasUv) {
    Write-Host "使用uv安装yt-dlp..." -ForegroundColor Cyan
    uv add yt-dlp
} else {
    Write-Host "使用pip安装yt-dlp..." -ForegroundColor Cyan
    python -m pip install yt-dlp
}

# 测试脚本
Write-Host "`n🧪 测试YouTube下载器..." -ForegroundColor Yellow
Write-Host "显示帮助信息:" -ForegroundColor Cyan
python youtube_downloader.py --help

Write-Host "`n✅ 测试完成！" -ForegroundColor Green
Write-Host "`n使用示例:" -ForegroundColor Yellow
Write-Host "  下载视频: python youtube_downloader.py 'https://youtube.com/watch?v=...'" -ForegroundColor White
Write-Host "  下载音频: python youtube_downloader.py -a 'URL'" -ForegroundColor White
Write-Host "  查看信息: python youtube_downloader.py -i 'URL'" -ForegroundColor White

Read-Host "`n按任意键继续..."