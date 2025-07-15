#!/usr/bin/env python3

print("=== Environment Check ===")

# Check Python version
import sys
print(f"Python version: {sys.version}")

# Check if yt-dlp is installed
print("\nChecking yt-dlp...")
try:
    import yt_dlp
    print(f"✓ yt-dlp is installed: {yt_dlp.__version__}")
    
    # Quick test with a simple YouTube video
    print("\nTesting with simple YouTube video...")
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(test_url, download=False)
        print(f"✓ YouTube test passed: {info.get('title', 'Unknown')}")
        
        # Now test the PornHub URL
        print("\nTesting PornHub URL...")
        pornhub_url = "https://cn.pornhub.com/view_video.php?viewkey=68543d832ddd2"
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(pornhub_url, download=False)
            print(f"✓ PornHub test passed: {info.get('title', 'Unknown')}")
            
        except Exception as e:
            print(f"✗ PornHub test failed: {str(e)}")
            
            # Try with more permissive settings
            print("  Trying with permissive settings...")
            try:
                permissive_opts = {
                    'quiet': True,
                    'geo_bypass': True,
                    'age_limit': 99,
                    'nocheckcertificate': True,
                }
                with yt_dlp.YoutubeDL(permissive_opts) as ydl:
                    info = ydl.extract_info(pornhub_url, download=False)
                print(f"✓ PornHub test with bypass passed: {info.get('title', 'Unknown')}")
            except Exception as e2:
                print(f"✗ PornHub test with bypass also failed: {str(e2)}")
        
    except Exception as e:
        print(f"✗ YouTube test failed: {str(e)}")
        print("This suggests a deeper yt-dlp issue")
        
except ImportError:
    print("✗ yt-dlp is not installed")
    print("Installing yt-dlp...")
    
    import subprocess
    result = subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ yt-dlp installed successfully")
        print("Please restart the test")
    else:
        print(f"✗ Installation failed: {result.stderr}")

print("\n=== Check Complete ===")