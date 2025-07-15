# Cookie Import and Setup Guide

## 🍪 How to Import Your PornHub Cookies

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