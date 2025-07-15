# 🌸 Arina AV Downloader 用户指南

> Thanks to Arina for 10 years of companionship 💕

## 📖 快速开始

### 🖥️ GUI图形界面版本（推荐新手）

1. **启动程序**
   ```bash
   python arina_gui.py
   ```

2. **使用步骤**
   - 在URL输入框中粘贴视频链接
   - 选择下载路径（默认：./downloads）
   - 选择视频质量（推荐：最佳质量）
   - 点击"开始下载"按钮
   - 等待下载完成

### 💻 CLI命令行版本（适合高级用户）

1. **基本用法**
   ```bash
   python arina_cli.py "https://example.com/video"
   ```

2. **高级选项**
   ```bash
   # 指定下载目录
   python arina_cli.py "https://example.com/video" --output ./my_videos
   
   # 指定视频质量
   python arina_cli.py "https://example.com/video" --quality 720p
   
   # 使用Cookie文件
   python arina_cli.py "https://example.com/video" --cookies ./cookies/site.json
   
   # 详细输出模式
   python arina_cli.py "https://example.com/video" --verbose
   ```

## 🔧 安装与配置

### 环境要求
- Python 3.8+
- Windows 10/11
- 稳定的网络连接

### 依赖安装
```bash
pip install -r requirements.txt
```

### 主要依赖
- `yt-dlp`: 核心下载引擎
- `PySide6`: GUI界面框架
- `requests`: 网络请求
- `colorama`: 彩色终端输出

## 📁 目录结构

```
Arina-AV-Downloader/
├── arina_gui.py          # GUI启动文件
├── arina_cli.py          # CLI启动文件
├── downloads/            # 默认下载目录
├── cookies/              # Cookie存储目录
├── logs/                 # 日志文件目录
├── portable/             # 便携式模块
├── requirements.txt      # 依赖列表
└── README.md            # 项目说明
```

## 🍪 Cookie配置

某些网站需要登录才能下载，可以配置Cookie：

1. **获取Cookie**
   - 使用浏览器登录目标网站
   - 导出Cookie为JSON格式
   - 保存到 `cookies/` 目录

2. **使用Cookie**
   ```bash
   # CLI方式
   python arina_cli.py "https://example.com/video" --cookies ./cookies/site.json
   
   # GUI方式：在设置中选择Cookie文件
   ```

## 🎬 支持的质量选项

- `best`: 最佳质量（默认）
- `worst`: 最低质量
- `720p`: 720P高清
- `1080p`: 1080P全高清
- `4k`: 4K超高清（如果可用）

## 📊 下载进度

### GUI版本
- 实时进度条显示
- 下载速度和剩余时间
- 文件大小信息

### CLI版本
- 终端进度条
- 详细下载统计
- 彩色状态提示

## 🛠️ 故障排除

### 常见问题

1. **下载失败**
   - 检查网络连接
   - 确认视频URL有效
   - 尝试使用Cookie

2. **GUI无法启动**
   - 检查PySide6是否正确安装
   - 尝试运行 `pip install PySide6`

3. **权限错误**
   - 确保下载目录有写入权限
   - 以管理员身份运行

### 获取帮助

```bash
# 查看CLI帮助
python arina_cli.py --help

# 检查环境
python -c "import sys; print(sys.version)"
```

## 🔄 更新日志

### v1.0.2
- 项目重命名为 Arina AV Downloader
- 统一启动文件命名
- 优化用户体验
- 修复已知问题

## 💡 使用技巧

1. **批量下载**: 可以创建包含多个URL的文本文件
2. **定时下载**: 结合系统任务计划器实现定时下载
3. **网络优化**: 在网络较慢时选择较低质量以提高成功率

## 🤝 支持与反馈

如果遇到问题或有建议，欢迎：
- 提交GitHub Issue
- 参与项目讨论
- 贡献代码改进

---

💖 感谢使用 Arina AV Downloader！
