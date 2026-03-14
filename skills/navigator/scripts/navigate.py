import sys
import urllib.parse
import subprocess
import webbrowser

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 navigate.py <QUERY>")
        sys.exit(1)
        
    # Combine arguments into a single search query
    query = " ".join(sys.argv[1:])
    
    # URL encode the query string
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    
    print(f"Opening Google Chrome to search for: '{query}'")
    
    try:
        # specifically target macOS Google Chrome using the 'open' command
        result = subprocess.run(["open", "-a", "Google Chrome", url], check=False, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Successfully requested browser to open.")
        else:
            print(f"Failed to open Google Chrome via 'open' command. Error: {result.stderr}")
            print("Trying default browser fallback via python webbrowser module...")
            webbrowser.open(url)
            
    except Exception as e:
        print(f"Error executing command: {e}")
        print("Trying default browser fallback...")
        webbrowser.open(url)

if __name__ == "__main__":
    main()
