# 🌸 Arina AV Downloader

**开箱即用的多平台视频下载器** - 支持YouTube、PornHub、Twitter等1800+网站

💝 **感谢新有菜Arina的10年陪伴** - 这个项目以Arina命名，纪念这份珍贵的友谊与陪伴

## ✨ 3步开始使用

### 1️⃣ 下载项目
```bash
# 下载到任意位置
git clone https://github.com/qhgy/arina-av-downloader.git
cd arina-av-downloader
```

### 2️⃣ 双击启动
- **Windows GUI**: 双击 `start_gui.bat` (图形界面)
- **Windows CLI**: 双击 `start_cli.bat` (命令行)
- **Mac/Linux**: 双击 `start.sh`

### 3️⃣ 开始下载
粘贴视频链接，点击下载按钮即可！

---

## 🚀 特色功能

- **🎯 开箱即用** - 双击启动，零配置
- **🌍 多平台支持** - 支持1800+网站
- **⚡ 智能管理** - 自动安装依赖，自动修复问题
- **🎨 现代界面** - 简洁美观的图形界面
- **📱 移动友好** - 支持手机分享的链接
- **🔒 隐私保护** - 本地下载，数据不上传

## 📋 支持的平台

| 平台 | 支持内容 | 特殊说明 |
|------|----------|----------|
| **YouTube** | 视频、播放列表、直播 | 支持4K高清 |
| **PornHub** | 成人内容 | 需18+验证 |
| **Twitter/X** | 视频、GIF | 支持推文视频 |
| **Instagram** | 帖子、故事、Reels | 需要登录 |
| **TikTok** | 短视频 | 去水印下载 |
| **Bilibili** | 视频、番剧 | 支持弹幕 |
| **抖音** | 短视频 | 去水印下载 |
| **其他** | 1800+网站 | 通用支持 |

## 💡 使用技巧

### 🎵 下载音频
点击"♪ 音频模式"按钮，只下载音频文件

### 📦 批量下载
一行一个链接，支持同时下载多个视频

### 🍪 登录下载
需要登录的内容：
1. 浏览器导出cookies
2. 放入 `cookies/` 文件夹
3. 重新启动程序

### ⚙️ 自定义设置
编辑 `downloader_config.json` 文件调整设置

## 🔧 故障排除

### 常见问题一键解决

| 问题 | 解决方案 |
|------|----------|
| 启动失败 | 重新双击启动脚本 |
| 下载失败 | 检查网络连接和链接有效性 |
| 权限错误 | 右键"以管理员身份运行" |
| 依赖缺失 | 程序会自动安装 |

### 🆘 获取帮助
- 查看 `logs/` 目录的日志文件
- 运行 `python run_tests.py` 检查环境
- 重新运行首次设置向导

## 🏗️ 技术特性

### 🔄 可移植性
- **零配置部署** - 复制到任何位置都能运行
- **智能路径管理** - 自动适应新环境
- **依赖自动安装** - 首次运行自动配置
- **跨平台兼容** - Windows/Mac/Linux通用

### 📦 现代包管理
- **UV优先** - 使用最新的Python包管理器
- **Pip回退** - 自动降级到传统方案
- **智能检测** - 自动选择最佳方案

### 🛡️ 错误处理
- **静默修复** - 自动解决常见问题
- **友好提示** - 中文错误信息和解决方案
- **一键修复** - 智能建议和自动修复

## 📁 项目结构

```
universal-video-downloader/
├── start.bat              # Windows启动脚本
├── start.sh               # Linux/Mac启动脚本
├── pyproject.toml         # 现代项目配置
├── requirements.txt       # 传统依赖文件
├── portable/              # 可移植性模块
│   ├── env_checker.py     # 环境检测
│   ├── dep_manager.py     # 依赖管理
│   ├── path_manager.py    # 路径管理
│   └── config_manager.py  # 配置管理
├── downloads/             # 下载文件夹
├── logs/                  # 日志文件夹
└── cookies/               # Cookie文件夹
```

## 🔬 开发者信息

### 运行测试
```bash
python run_tests.py
```

### 配置迁移
```bash
python migrate_config.py
```

### 环境检查
```bash
python portable/env_checker.py
```

## 📄 许可证

MIT License - 详见 LICENSE 文件

## ⚠️ 免责声明

本工具仅供学习和个人使用。请遵守相关平台的服务条款和版权法律。开发者不对软件的滥用承担责任。

## 🙏 致谢

- 基于 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 构建
- 界面使用 PyQt6/PySide6
- 采用Apple式设计理念

---

**🎉 享受您的下载体验！**