import argparse
import urllib.parse
import urllib.request
import urllib.error
import re
import subprocess
import webbrowser
import platform
import json

def get_google_search_results(query):
    print(f"\n--- Extracting Web Pages from Search Results for: '{query}' ---")
    
    # We use DuckDuckGo HTML version for reliable scraping without JS/Captchas
    # while still opening the user's Chrome to Google.
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
        results = []
        
        # DuckDuckGo HTML results are contained within <div class="result "> blocks
        result_blocks = html.split('<div class="result ')[1:]
        
        # also import html for unescaping at runtime
        import html as html_lib
        
        for block in result_blocks:
            # Extract Title and URL
            # Pattern: <a rel="nofollow" class="result__a" href="([^"]+)">\s*(.*?)\s*</a>
            title_url_match = re.search(r'<a rel="nofollow" class="result__a" href="([^"]+)">\s*(.*?)\s*</a>', block, re.IGNORECASE | re.DOTALL)
            
            # Extract Snippet (Description)
            # Pattern: <a class="result__snippet" ...>(.*?)</a>
            snippet_match = re.search(r'<a class="result__snippet"[^>]*>(.*?)</a>', block, re.IGNORECASE | re.DOTALL)
            
            if title_url_match:
                url_match = title_url_match.group(1)
                text_match = title_url_match.group(2)
                
                # decode url
                if '//duckduckgo.com/l/?uddg=' in url_match:
                    target = re.search(r'uddg=([^&]+)', url_match)
                    if target:
                        url_match = urllib.parse.unquote(target.group(1))
                
                clean_url = url_match.strip()
                clean_title = re.sub(r'<[^>]+>', '', text_match).strip()
                clean_title = html_lib.unescape(clean_title)
                
                snippet_text = ""
                keywords = []
                if snippet_match:
                    snippet_content = snippet_match.group(1)
                    
                    # Extract keywords (bolded terms in DDG results)
                    bold_pattern = re.compile(r'<b>(.*?)</b>', re.IGNORECASE)
                    bold_matches = bold_pattern.findall(snippet_content)
                    keywords = list(set([html_lib.unescape(b.strip()) for b in bold_matches if b.strip()]))
                    
                    # Strip tags and unescape for the full snippet text
                    snippet_text = re.sub(r'<[^>]+>', '', snippet_content).strip()
                    snippet_text = html_lib.unescape(snippet_text)
                
                if clean_url.startswith('http') and 'duckduckgo' not in clean_url:
                    result = {
                        "title": clean_title if clean_title else "Search Result", 
                        "url": clean_url,
                        "snippet": snippet_text,
                        "keywords": keywords
                    }
                    if not any(r['url'] == clean_url for r in results):
                        results.append(result)

        # Print all found URLs, snippets and keywords
        if results:
            for idx, res in enumerate(results, start=1):
                print(f"{idx}. {res['title']}")
                print(f"   URL: {res['url']}")
                if res['snippet']:
                    print(f"   Snippet: {res['snippet']}")
                if res['keywords']:
                    print(f"   Keywords: {', '.join(res['keywords'])}")
                print()
        else:
            print("No external web pages could be extracted from search results.")
            
        # Save to a JSON file so the toolkit / LLM can consume it easily
        try:
            with open('google_search_results.json', 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4, ensure_ascii=False)
            print("> Results saved to google_search_results.json")
        except Exception as e:
            print(f"Could not save JSON: {e}")
            
        return results

    except urllib.error.URLError as e:
        print(f"Failed to scrape search results: {e}")
        return []
    except Exception as e:
        print(f"Error while parsing search results: {e}")
        return []

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

    # Extract the web pages
    get_google_search_results(query)

if __name__ == "__main__":
    main()
