import argparse
import urllib.parse
import subprocess
import webbrowser
import platform

def main():
    parser = argparse.ArgumentParser(description="Navigate to Google Search")
    parser.add_argument('--browser', choices=['chrome', 'firefox'], default='chrome', help='Browser to use (chrome or firefox)')
    parser.add_argument('query', nargs='+', help='The search query')
    
    args = parser.parse_args()
    query = " ".join(args.query)
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    
    print(f"Opening {args.browser.title()} to search for: '{query}'")
    
    os_name = platform.system()
    
    try:
        cmd = []
        if args.browser == 'chrome':
            if os_name == 'Darwin':
                cmd = ["open", "-a", "Google Chrome", url]
            elif os_name == 'Windows':
                cmd = ["cmd", "/c", "start", "chrome", url]
            else: # Linux
                cmd = ["google-chrome", url]
        elif args.browser == 'firefox':
            if os_name == 'Darwin':
                cmd = ["open", "-a", "Firefox", url]
            elif os_name == 'Windows':
                cmd = ["cmd", "/c", "start", "firefox", url]
            else: # Linux
                cmd = ["firefox", url]

        # On Windows, we need to pass shell=True for 'cmd /c start' to work properly
        if os_name == 'Windows':
            result = subprocess.run(cmd, check=False, shell=True, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, check=False, capture_output=True, text=True)
            
        if result.returncode == 0:
            print("Successfully requested browser to open.")
        else:
            print(f"Failed to open browser. Error: {result.stderr}")
            print("Trying default browser fallback via python webbrowser module...")
            if args.browser == 'firefox':
                try:
                    webbrowser.get('firefox').open(url)
                except:
                    webbrowser.open(url)
            else:
                try:
                    webbrowser.get('chrome').open(url)
                except:
                    webbrowser.open(url)
            
    except Exception as e:
        print(f"Error executing command: {e}")
        print("Trying default browser fallback...")
        webbrowser.open(url)

if __name__ == "__main__":
    main()
