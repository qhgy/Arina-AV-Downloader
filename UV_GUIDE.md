# 🌸 Arina AV Downloader UV虚拟环境指南

> Thanks to Arina for 10 years of companionship 💕

## 🚀 什么是UV？

UV是一个超快的Python包管理器和项目管理工具，比传统的pip + venv组合快10-100倍！

### 🌟 UV的优势：
- ⚡ **超快速度**：安装依赖比pip快10-100倍
- 🔒 **依赖锁定**：自动生成lock文件确保环境一致性
- 🛡️ **隔离环境**：自动创建虚拟环境，避免依赖冲突
- 📦 **现代化**：支持最新的Python包管理标准

## 📥 安装UV

### Windows (推荐)
```powershell
# 使用PowerShell安装
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 其他方式
```bash
# 使用pip安装
pip install uv

# 使用conda安装
conda install -c conda-forge uv
```

## 🔧 使用UV安装Arina

### 方法一：一键安装脚本（最简单）
1. 下载项目并解压
2. 双击运行 `install_uv.bat`
3. 脚本会自动：
   - 检查并安装UV
   - 创建虚拟环境
   - 安装所有依赖
   - 询问是否启动程序

### 方法二：手动安装
```bash
# 1. 进入项目目录
cd Arina-AV-Downloader

# 2. 创建虚拟环境
uv venv

# 3. 安装项目依赖
uv pip install -e .

# 4. 启动程序
uv run python arina_gui.py
```

## 🎮 使用方法

### 启动程序
```bash
# GUI版本
uv run python arina_gui.py

# CLI版本
uv run python arina_cli.py --help

# 或者先激活环境再运行
.venv\Scripts\activate    # Windows
source .venv/bin/activate # Linux/Mac
python arina_gui.py
```

### 管理依赖
```bash
# 添加新依赖
uv add package_name

# 移除依赖
uv remove package_name

# 更新依赖
uv lock --upgrade

# 同步依赖（确保环境与lock文件一致）
uv sync
```

## 📁 UV项目结构

```
Arina-AV-Downloader/
├── .venv/                # 虚拟环境目录
├── uv.lock              # 依赖锁定文件
├── pyproject.toml       # 项目配置文件
├── arina_gui.py         # GUI启动文件
├── arina_cli.py         # CLI启动文件
└── install_uv.bat       # UV一键安装脚本
```

## 🔄 常用命令

### 环境管理
```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境
.venv\Scripts\activate    # Windows
source .venv/bin/activate # Linux/Mac

# 退出虚拟环境
deactivate
```

### 包管理
```bash
# 安装项目依赖
uv pip install -e .

# 安装特定包
uv pip install package_name

# 安装开发依赖
uv pip install -e ".[dev]"

# 安装GUI依赖
uv pip install -e ".[gui]"
```

### 运行程序
```bash
# 直接运行（推荐）
uv run python arina_gui.py
uv run python arina_cli.py

# 或者激活环境后运行
.venv\Scripts\activate
python arina_gui.py
```

## 🛠️ 故障排除

### 问题1：UV命令不存在
**解决方案**：
```bash
# 重新安装UV
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或者重启命令提示符
```

### 问题2：虚拟环境创建失败
**解决方案**：
```bash
# 删除现有环境重新创建
rmdir /s .venv
uv venv
```

### 问题3：依赖安装失败
**解决方案**：
```bash
# 清理缓存重新安装
uv cache clean
uv pip install -e .

# 或者使用国内镜像
uv pip install -e . --index-url https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 问题4：程序无法启动
**解决方案**：
```bash
# 检查虚拟环境是否激活
.venv\Scripts\activate

# 检查依赖是否完整
uv pip list

# 重新安装依赖
uv sync
```

## 🆚 UV vs 传统方式对比

| 特性 | UV | 传统pip+venv |
|------|----|----|
| 安装速度 | ⚡ 超快 | 🐌 较慢 |
| 依赖解析 | 🧠 智能 | 🤔 基础 |
| 锁定文件 | ✅ 自动 | ❌ 手动 |
| 环境隔离 | 🛡️ 自动 | 🔧 手动 |
| 项目管理 | 📦 集成 | 🔨 分散 |

## 🎯 最佳实践

1. **使用UV运行**：优先使用 `uv run` 而不是激活环境
2. **定期更新**：使用 `uv lock --upgrade` 更新依赖
3. **提交lock文件**：将 `uv.lock` 文件提交到版本控制
4. **环境同步**：在新环境使用 `uv sync` 确保一致性

## 🔗 相关链接

- [UV官方文档](https://docs.astral.sh/uv/)
- [UV GitHub仓库](https://github.com/astral-sh/uv)
- [Python包管理最佳实践](https://packaging.python.org/)

---

💖 使用UV让Arina AV Downloader的安装和管理变得更加简单快捷！
