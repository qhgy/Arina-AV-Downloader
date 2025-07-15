#!/usr/bin/env python3
"""
Arina AV Downloader - Cookie Setup Wizard
帮助用户轻松设置Cookie以获得更好的下载体验
"""

import os
import json
import sys
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("🍪 Arina AV Downloader - Cookie Setup Wizard")
    print("Thanks to Arina for 10 years of companionship 💕")
    print("=" * 60)
    print()

def print_step(step_num, title):
    print(f"📋 Step {step_num}: {title}")
    print("-" * 40)

def install_edit_this_cookie_guide():
    """引导用户安装 EditThisCookie 扩展"""
    print_step(1, "Install EditThisCookie Extension")
    print("🌐 Please install the EditThisCookie browser extension:")
    print()
    print("For Chrome:")
    print("   https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg")
    print()
    print("For Firefox:")
    print("   https://addons.mozilla.org/en-US/firefox/addon/edit-this-cookie/")
    print()
    print("For Edge:")
    print("   https://microsoftedge.microsoft.com/addons/detail/editthiscookie/neaplmfkghagebokkhpjpoebhdledlfi")
    print()
    input("✅ Press Enter after installing the extension...")
    print()

def export_cookie_guide():
    """引导用户导出Cookie"""
    print_step(2, "Export Cookies from Website")
    print("🍪 How to export cookies:")
    print()
    print("1. Open your browser and go to the website (e.g., pornhub.com)")
    print("2. Log in to your account if needed")
    print("3. Click the EditThisCookie extension icon")
    print("4. Click 'Export' button (📤)")
    print("5. Copy all the cookie data")
    print()
    print("📝 The cookie data should look like this:")
    print('   [{"domain":".pornhub.com","name":"session_token",...}]')
    print()

def get_cookie_input():
    """获取用户输入的Cookie数据"""
    print_step(3, "Paste Your Cookie Data")
    print("📋 Please paste your cookie data below:")
    print("(Tip: Right-click and paste, then press Enter twice to finish)")
    print()
    
    lines = []
    print("Cookie data:")
    while True:
        try:
            line = input()
            if line.strip() == "" and lines:
                break
            lines.append(line)
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user")
            return None
    
    cookie_text = "\n".join(lines).strip()
    
    if not cookie_text:
        print("❌ No cookie data provided")
        return None
    
    return cookie_text

def validate_cookie_format(cookie_text):
    """验证Cookie格式"""
    try:
        # 尝试解析JSON
        cookie_data = json.loads(cookie_text)
        
        # 检查是否是列表
        if not isinstance(cookie_data, list):
            return False, "Cookie data should be a JSON array"
        
        # 检查是否有有效的cookie项
        if len(cookie_data) == 0:
            return False, "Cookie data is empty"
        
        # 检查第一个cookie的基本结构
        first_cookie = cookie_data[0]
        required_fields = ['name', 'value', 'domain']
        
        for field in required_fields:
            if field not in first_cookie:
                return False, f"Missing required field: {field}"
        
        return True, cookie_data
        
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON format: {e}"

def save_cookie_file(cookie_data, domain):
    """保存Cookie文件"""
    # 创建cookies目录
    cookies_dir = Path("cookies")
    cookies_dir.mkdir(exist_ok=True)
    
    # 根据域名确定文件名
    if "pornhub" in domain.lower():
        filename = "pornhub_cookies.json"
    elif "xvideos" in domain.lower():
        filename = "xvideos_cookies.json"
    elif "xhamster" in domain.lower():
        filename = "xhamster_cookies.json"
    else:
        # 从域名生成文件名
        clean_domain = domain.replace(".", "_").replace("/", "_")
        filename = f"{clean_domain}_cookies.json"
    
    filepath = cookies_dir / filename
    
    # 保存Cookie数据
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(cookie_data, f, indent=2, ensure_ascii=False)
    
    return filepath

def detect_domain(cookie_data):
    """从Cookie数据中检测域名"""
    for cookie in cookie_data:
        if 'domain' in cookie:
            domain = cookie['domain'].lstrip('.')
            return domain
    return "unknown"

def main():
    print_banner()
    
    print("🎯 This wizard will help you set up cookies for better download experience.")
    print("   Cookies allow you to download private/premium content from your account.")
    print()
    
    # Step 1: 安装扩展引导
    install_edit_this_cookie_guide()
    
    # Step 2: 导出Cookie引导
    export_cookie_guide()
    
    # Step 3: 获取Cookie数据
    cookie_text = get_cookie_input()
    if not cookie_text:
        print("❌ Setup cancelled")
        return
    
    # Step 4: 验证Cookie格式
    print_step(4, "Validating Cookie Data")
    is_valid, result = validate_cookie_format(cookie_text)
    
    if not is_valid:
        print(f"❌ Invalid cookie format: {result}")
        print("Please check your cookie data and try again.")
        return
    
    cookie_data = result
    print(f"✅ Valid cookie data found ({len(cookie_data)} cookies)")
    
    # Step 5: 保存Cookie文件
    print_step(5, "Saving Cookie File")
    domain = detect_domain(cookie_data)
    filepath = save_cookie_file(cookie_data, domain)
    
    print(f"✅ Cookie file saved: {filepath}")
    print(f"🌐 Detected domain: {domain}")
    print()
    
    # 完成提示
    print("🎉 Cookie setup completed successfully!")
    print()
    print("📋 Next steps:")
    print("1. Close this wizard")
    print("2. Restart Arina AV Downloader")
    print("3. Try downloading from the website")
    print()
    print("💡 Tips:")
    print("- Cookies may expire, re-run this wizard if downloads fail")
    print("- Different websites need different cookie files")
    print("- Keep your login session active in the browser")
    print()
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("Press Enter to exit...")
