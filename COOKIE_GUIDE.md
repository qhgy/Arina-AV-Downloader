# 🍪 Cookie 设置指南

## 🎯 快速开始 - 使用 Cookie 设置向导

**最简单的方法：**

1. 双击 `1-Cookie-Setup-Wizard.bat`
2. 按照向导提示操作
3. 几分钟内完成设置

---

## 🤔 什么是 Cookie？

Cookie 是网站存储在您浏览器中的小文件，用于记住您的登录状态。使用 Cookie 可以：

- ✅ 下载需要登录的私人视频
- ✅ 获取更高质量的视频源
- ✅ 避免地区限制
- ✅ 提高下载成功率

---

## 🛠️ 详细设置步骤

### 第一步：安装浏览器扩展

安装 **EditThisCookie** 扩展：

- **Chrome**: https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg
- **Firefox**: https://addons.mozilla.org/en-US/firefox/addon/edit-this-cookie/
- **Edge**: https://microsoftedge.microsoft.com/addons/detail/editthiscookie/neaplmfkghagebokkhpjpoebhdledlfi

### 第二步：导出 Cookie

1. 打开浏览器，访问目标网站（如 pornhub.com）
2. 登录您的账户
3. 点击 EditThisCookie 扩展图标 🍪
4. 点击 "Export" 按钮 📤
5. 复制所有 Cookie 数据

### 第三步：使用设置向导

1. 运行 `1-Cookie-Setup-Wizard.bat`
2. 粘贴复制的 Cookie 数据
3. 向导会自动创建正确的 Cookie 文件

---

## 📁 Cookie 文件说明

Cookie 文件会自动保存在 `cookies/` 目录：

```
cookies/
├── pornhub_cookies.json     # PornHub 网站
├── xvideos_cookies.json     # XVideos 网站
└── xhamster_cookies.json    # XHamster 网站
```

---

## 🍪 传统方法 - 手动导入

### Method 1: Quick Import via Simple Interface

1. **Start the downloader:**
   ```cmd
   python simple_downloader.py
   ```

2. **Choose option 6: Cookie Management**

3. **Choose option 4: Import Your PornHub Cookies**

4. **Paste your cookie JSON data when prompted**

### Method 2: Direct Cookie Import

1. **Save your cookies to a file:**
   - Create `pornhub_cookies.json` with your cookie data

2. **Run the cookie manager:**
   ```cmd
   python cookie_manager.py
   ```

3. **Choose option 2: Load from JSON file**

### Method 3: Programmatic Import

```python
from cookie_manager import CookieManager

# Your cookie data (the JSON you provided)
cookies_data = [
    {
        "domain": ".pornhub.com",
        "name": "accessAgeDisclaimerPH",
        "value": "1",
        # ... rest of cookie data
    }
    # ... more cookies
]

manager = CookieManager()
cookies_file = manager.save_json_cookies(cookies_data, "pornhub")
print(f"Cookies saved to: {cookies_file}")
```

## 🎯 What Your Cookies Do

Your provided cookies include:

- **`accessAgeDisclaimerPH=1`** - Age verification bypass
- **`cookieConsent=3`** - Cookie consent accepted  
- **`il`** - Session authentication token
- **`sessid`** - Session identifier
- **Various tracking cookies** - For site functionality

These cookies will allow the downloader to:
- ✅ Access age-restricted content
- ✅ Bypass age verification prompts
- ✅ Use your account permissions
- ✅ Download premium/restricted videos

## 🔧 How It Works

1. **Cookie Storage:**
   - JSON format: `./cookies/pornhub_cookies.json`
   - Netscape format: `./cookies/pornhub_cookies.txt`

2. **Automatic Detection:**
   - When you download from PornHub, cookies are automatically used
   - No need to manually specify - it's seamless

3. **Status Display:**
   ```
   Platform detected: PornHub
   Using cookies for pornhub: ./cookies/pornhub_cookies.txt
   Getting video information...
   ```

## 🧪 Testing Your Cookies

After importing, test with a restricted video:

1. **Check cookie status:**
   - Simple interface → Cookie Management → View Current Cookies

2. **Try downloading:**
   - Use a PornHub URL that was previously restricted
   - Should now work without age verification

## 🔄 Cookie Refresh

Cookies eventually expire. When downloads start failing:

1. **Export fresh cookies** from your browser
2. **Re-import** using the same process
3. **Delete old cookies** if needed

## 💡 Pro Tips

- **Keep cookies updated** - Re-export monthly
- **Use browser extensions** like "Cookie Editor" for easy export
- **Test with info mode** first: `python universal_cli.py -i "URL"`
- **Multiple platforms** - Import cookies for other sites too

Your specific cookie set looks perfect for PornHub access! 🎉