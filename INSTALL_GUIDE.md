# 🌸 Arina AV Downloader 小白安装指南

> Thanks to Arina for 10 years of companionship 💕

## 📋 系统要求

- Windows 10/11 (64位)
- 至少 2GB 可用磁盘空间
- 稳定的网络连接

## 🐍 第一步：安装Python

### 检查是否已安装Python
1. 按 `Win + R` 键，输入 `cmd`，按回车
2. 在黑色窗口中输入：`python --version`
3. 如果显示 `Python 3.8.x` 或更高版本，跳到第二步
4. 如果提示"不是内部或外部命令"，继续下面的安装步骤

### 下载并安装Python
1. 访问：https://www.python.org/downloads/
2. 点击黄色的 "Download Python 3.x.x" 按钮
3. 下载完成后，双击安装包
4. **重要**：勾选 "Add Python to PATH" 选项
5. 点击 "Install Now"
6. 安装完成后重启电脑

## 📥 第二步：下载Arina

1. 访问：https://github.com/qhgy/Arina-AV-Downloader/releases
2. 点击最新版本的 "Source code (zip)" 下载
3. 下载完成后，右键解压到桌面或其他文件夹
4. 进入解压后的文件夹

## 🔧 第三步：安装依赖

### 方法一：UV虚拟环境（推荐，更快更稳定）
1. 双击运行 `install_uv.bat` 文件
2. 脚本会自动安装UV并创建虚拟环境
3. 等待安装完成后选择是否启动程序

### 方法二：传统pip安装
1. 在文件夹中按住 `Shift` 键，右键点击空白处
2. 选择 "在此处打开PowerShell窗口" 或 "在此处打开命令窗口"
3. 在弹出的窗口中输入以下命令：

```bash
pip install -r requirements.txt
```

4. 等待安装完成（可能需要几分钟）

### 如果安装失败，尝试：
```bash
# 升级pip
python -m pip install --upgrade pip

# 重新安装依赖
pip install -r requirements.txt

# 或者使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

## 🚀 第四步：启动程序

### 如果使用UV安装：
```bash
# GUI版本
uv run python arina_gui.py

# CLI版本
uv run python arina_cli.py --help

# 或者先激活虚拟环境
.venv\Scripts\activate
python arina_gui.py
```

### 如果使用pip安装：
```bash
# GUI版本（推荐新手）
python arina_gui.py

# CLI版本
python arina_cli.py --help
```

## 🎮 使用方法

### GUI界面使用
1. 程序启动后会显示图形界面
2. 在URL输入框中粘贴视频链接
3. 选择下载路径（默认：downloads文件夹）
4. 选择视频质量（推荐：最佳质量）
5. 点击"开始下载"按钮
6. 等待下载完成

### CLI命令行使用
```bash
# 基本用法
python arina_cli.py "https://example.com/video"

# 指定下载目录
python arina_cli.py "https://example.com/video" --output ./my_videos

# 查看所有选项
python arina_cli.py --help
```

## 🛠️ 常见问题解决

### 问题1：提示"python不是内部或外部命令"
**解决方案**：
- Python没有正确安装或没有添加到PATH
- 重新安装Python，确保勾选"Add Python to PATH"

### 问题2：pip安装依赖失败
**解决方案**：
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 问题3：GUI界面无法启动
**解决方案**：
```bash
# 单独安装PySide6
pip install PySide6

# 或者尝试其他GUI版本
python simple_apple_gui.py
```

### 问题4：下载失败
**解决方案**：
- 检查网络连接
- 确认视频URL有效
- 某些网站可能需要Cookie，参考COOKIE_GUIDE.md

## 📁 文件夹结构说明

```
Arina-AV-Downloader/
├── arina_gui.py          # GUI启动文件
├── arina_cli.py          # CLI启动文件
├── downloads/            # 默认下载目录
├── cookies/              # Cookie存储目录
├── requirements.txt      # 依赖列表
├── USER_GUIDE.md        # 详细使用指南
└── INSTALL_GUIDE.md     # 本安装指南
```

## 🆘 获取帮助

如果遇到问题：
1. 查看 USER_GUIDE.md 详细使用指南
2. 访问 GitHub Issues：https://github.com/qhgy/Arina-AV-Downloader/issues
3. 提交新的Issue描述你的问题

## 🎉 安装完成

恭喜！现在你可以使用Arina AV Downloader了！

建议先用GUI版本熟悉功能，然后可以尝试CLI版本获得更多控制选项。

---

💖 感谢使用 Arina AV Downloader！
