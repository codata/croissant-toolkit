import sys
import os
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description="Capture a high-quality screenshot of a YouTube video, automatically waiting for ads to finish.")
    parser.add_argument('url', help='The URL of the YouTube video')
    parser.add_argument('--output', '-o', help='Path to save the screenshot')
    
    args = parser.parse_args()
    
    # Path to the screenshot taker script
    # Logic: Go up from 'scripts' to 'youtuber', then up to 'skills' (2 levels)
    # Then down to screenshot_taker/scripts/
    screenshot_script = os.path.join(os.path.dirname(__file__), "../../screenshot_taker/scripts/take_screenshot.py")
    screenshot_script = os.path.abspath(screenshot_script)
    
    if not os.path.exists(screenshot_script):
        print(f"[Youtuber] Error: Screenshot taker skill not found at {screenshot_script}")
        sys.exit(1)
        
    print(f"[Youtuber] Preparing to capture video: {args.url}")
    print("[Youtuber] The system will automatically detect and wait for YouTube ads.")
    
    # Use sys.executable to ensure we use the same environment
    cmd = [sys.executable, screenshot_script, args.url]
    if args.output:
        cmd.extend(["--output", args.output])
    
    # We use a longer wait for video buffering
    cmd.extend(["--wait", "5000"])
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print("[Youtuber] Failed to capture screenshot.")
        sys.exit(1)

if __name__ == "__main__":
    main()
