# Cookie Files Directory

This directory is for storing browser cookies to access login-required video sites.

## ⚠️ IMPORTANT SECURITY NOTICE

**Cookie files contain sensitive authentication information and should NEVER be uploaded to version control or shared publicly.**

## How to Use Cookies

### 1. Export Cookies from Browser
Use a browser extension like:
- **Chrome/Edge**: "Get cookies.txt LOCALLY" extension
- **Firefox**: "cookies.txt" extension

### 2. Save Cookie Files
Save exported cookies as:
```
cookies/
├── youtube_cookies.txt
├── pornhub_cookies.txt
├── twitter_cookies.txt
└── ... (other platform cookies)
```

### 3. File Format
Cookie files should be in Netscape format (.txt) or JSON format (.json):
```
# Netscape HTTP Cookie File
.youtube.com	TRUE	/	FALSE	1234567890	session_token	abc123...
```

## Supported Platforms
- YouTube (youtube_cookies.txt)
- PornHub (pornhub_cookies.txt)
- Twitter (twitter_cookies.txt)
- Generic sites (sitename_cookies.txt)

## Privacy Protection
- All `.txt` and `.json` files in this directory are automatically ignored by Git
- Cookie files are never uploaded to GitHub
- Keep your cookie files secure and don't share them

## Troubleshooting
- Make sure cookie files are in the correct format
- Check that cookies haven't expired
- Verify the file naming convention matches the platform
- Ensure cookies are from the correct domain

---
**Remember: Your cookies = Your login credentials. Keep them safe!** 🔒
