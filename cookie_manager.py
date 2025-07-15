#!/usr/bin/env python3
"""
Cookie Manager for Universal Video Downloader
Handles cookie import and conversion for platform authentication
"""

import json
import os
import time
from pathlib import Path
from typing import Dict, List, Any
from http.cookiejar import MozillaCookieJar


class CookieManager:
    """Manages cookies for video downloading"""
    
    def __init__(self, cookies_dir: str = "./cookies"):
        self.cookies_dir = Path(cookies_dir)
        self.cookies_dir.mkdir(exist_ok=True)
        
    def save_json_cookies(self, cookies_json: str, platform: str = "pornhub") -> str:
        """Save JSON cookies to file"""
        try:
            cookies_data = json.loads(cookies_json) if isinstance(cookies_json, str) else cookies_json
            
            # Save original JSON
            json_file = self.cookies_dir / f"{platform}_cookies.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(cookies_data, f, indent=2)
            
            # Convert to Netscape format for yt-dlp
            netscape_file = self.cookies_dir / f"{platform}_cookies.txt"
            self._convert_to_netscape(cookies_data, netscape_file)
            
            print(f"Cookies saved successfully:")
            print(f"  JSON format: {json_file}")
            print(f"  Netscape format: {netscape_file}")
            
            return str(netscape_file)
            
        except Exception as e:
            print(f"Error saving cookies: {e}")
            return ""
    
    def _convert_to_netscape(self, cookies_json: List[Dict], output_file: Path):
        """Convert JSON cookies to Netscape format"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                # Write Netscape header
                f.write("# Netscape HTTP Cookie File\n")
                f.write("# This is a generated file! Do not edit.\n\n")
                
                for cookie in cookies_json:
                    domain = cookie.get('domain', '')
                    flag = 'TRUE' if not cookie.get('hostOnly', False) else 'FALSE'
                    path = cookie.get('path', '/')
                    secure = 'TRUE' if cookie.get('secure', False) else 'FALSE'
                    
                    # Handle expiration
                    expiration = cookie.get('expirationDate', 0)
                    if isinstance(expiration, float):
                        expiration = int(expiration)
                    elif not expiration or cookie.get('session', False):
                        expiration = 0
                    
                    name = cookie.get('name', '')
                    value = cookie.get('value', '')
                    
                    # Write cookie line
                    f.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expiration}\t{name}\t{value}\n")
                    
        except Exception as e:
            print(f"Error converting cookies: {e}")
    
    def get_cookies_file(self, platform: str = "pornhub") -> str:
        """Get cookies file path for platform"""
        netscape_file = self.cookies_dir / f"{platform}_cookies.txt"
        if netscape_file.exists():
            return str(netscape_file)
        return ""
    
    def list_cookies(self) -> Dict[str, str]:
        """List available cookie files"""
        cookies = {}
        for file in self.cookies_dir.glob("*_cookies.txt"):
            platform = file.stem.replace("_cookies", "")
            cookies[platform] = str(file)
        return cookies
    
    def delete_cookies(self, platform: str):
        """Delete cookies for platform"""
        json_file = self.cookies_dir / f"{platform}_cookies.json"
        txt_file = self.cookies_dir / f"{platform}_cookies.txt"
        
        for file in [json_file, txt_file]:
            if file.exists():
                file.unlink()
                print(f"Deleted: {file}")


def import_cookies_interactive():
    """Interactive cookie import"""
    manager = CookieManager()
    
    print("Cookie Import Utility")
    print("=" * 50)
    
    print("\nAvailable methods:")
    print("1. Paste JSON cookies directly")
    print("2. Load from JSON file")
    print("3. Show current cookies")
    print("4. Delete cookies")
    print("0. Exit")
    
    while True:
        try:
            choice = input("\nChoose option (0-4): ").strip()
            
            if choice == '0':
                break
                
            elif choice == '1':
                print("\nPaste your JSON cookies (paste and press Enter twice):")
                lines = []
                while True:
                    try:
                        line = input()
                        if not line:
                            break
                        lines.append(line)
                    except EOFError:
                        break
                
                cookies_text = '\n'.join(lines)
                if cookies_text:
                    platform = input("Platform name (default: pornhub): ").strip() or "pornhub"
                    manager.save_json_cookies(cookies_text, platform)
                
            elif choice == '2':
                file_path = input("Enter JSON file path: ").strip()
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        cookies_data = json.load(f)
                    platform = input("Platform name (default: pornhub): ").strip() or "pornhub"
                    manager.save_json_cookies(cookies_data, platform)
                else:
                    print("File not found!")
                    
            elif choice == '3':
                cookies = manager.list_cookies()
                if cookies:
                    print("\nCurrent cookies:")
                    for platform, file_path in cookies.items():
                        print(f"  {platform}: {file_path}")
                else:
                    print("No cookies found")
                    
            elif choice == '4':
                platform = input("Platform to delete: ").strip()
                manager.delete_cookies(platform)
                
            else:
                print("Invalid option")
                
        except KeyboardInterrupt:
            break
    
    print("\nCookie import completed!")


if __name__ == '__main__':
    # Test with provided PornHub cookies
    pornhub_cookies = [
        {
            "domain": ".pornhub.com",
            "expirationDate": 1779374974.390083,
            "hostOnly": False,
            "httpOnly": False,
            "name": "__l",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": "0",
            "value": "682D963C-42FE722901BB2F6C0A-6CB2B8A6",
            "id": 1
        },
        {
            "domain": ".pornhub.com",
            "hostOnly": False,
            "httpOnly": False,
            "name": "__s",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": True,
            "storeId": "0",
            "value": "6872CC56-42FE722901BBB28BC-1EBAD539",
            "id": 2
        },
        {
            "domain": ".pornhub.com",
            "expirationDate": 1779354045,
            "hostOnly": False,
            "httpOnly": False,
            "name": "accessAgeDisclaimerPH",
            "path": "/",
            "sameSite": "unspecified",
            "secure": False,
            "session": False,
            "storeId": "0",
            "value": "1",
            "id": 3
        }
        # ... (truncated for demo, but would include all cookies)
    ]
    
    # Demo
    print("Cookie Manager Demo")
    manager = CookieManager()
    cookies_file = manager.save_json_cookies(pornhub_cookies, "pornhub")
    print(f"Demo cookies saved to: {cookies_file}")
    
    # Interactive mode
    import_cookies_interactive()