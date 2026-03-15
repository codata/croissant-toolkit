import sys
import urllib.parse
import urllib.request
import urllib.error
import re
import subprocess
import webbrowser
import json
import html as html_lib

def get_youtube_videos_playwright(query):
    """Uses Playwright to perform search and handle consent dialogue."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[Youtuber] Playwright not found, falling back to basic scraping.")
        return get_youtube_videos_urllib(query)

    print(f"\n--- [Playwright] Searching YouTube for: '{query}' ---")
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            locale="fr-FR"
        )
        page = context.new_page()
        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Handle Consent Dialogue (Multi-language support)
            try:
                # Force a small wait so the overlay can appear
                page.wait_for_timeout(2000)
                
                # Strategy 1: Explicit French button text
                target_texts = ["Tout accepter", "J'accepte", "Accepter", "Accept all", "I agree", "Agree", "Accept"]
                
                for text in target_texts:
                    # Get by text is often more reliable for translations
                    btn = page.get_by_role("button", name=text, exact=False)
                    if btn.count() > 0:
                        first_btn = btn.first
                        if first_btn.is_visible():
                            print(f"[Youtuber] Found consent button with text: '{text}'. Clicking...")
                            first_btn.click()
                            page.wait_for_load_state("networkidle", timeout=5000)
                            break
                
                # Strategy 2: Fallback to CSS selectors if needed
                selectors = [
                    'button[aria-label*="Accept"]',
                    'button[aria-label*="Accepter"]',
                    'form[action*="consent"] button'
                ]
                for sel in selectors:
                    btn = page.query_selector(sel)
                    if btn and btn.is_visible():
                        print(f"[Youtuber] Found consent button via selector: {sel}. Clicking...")
                        btn.click()
                        page.wait_for_load_state("networkidle", timeout=5000)
            except Exception as e:
                print(f"[Youtuber] Consent handling note: {e}")
            
            # Extract ytInitialData from the page
            content = page.content()
            m = re.search(r'var ytInitialData = (\{.*?\});', content)
            if not m:
                # Try to wait a bit longer for it to appear
                page.wait_for_timeout(2000)
                content = page.content()
                m = re.search(r'var ytInitialData = (\{.*?\});', content)

            if m:
                data = json.loads(m.group(1))
                videos = parse_youtube_json(data)
                save_and_print_results(videos)
                browser.close()
                return videos
            else:
                print("[Youtuber] Failed to extract ytInitialData via Playwright.")
                browser.close()
                return get_youtube_videos_urllib(query)

        except Exception as e:
            print(f"[Youtuber] Playwright error: {e}")
            browser.close()
            return get_youtube_videos_urllib(query)

def get_youtube_videos_urllib(query):
    """Fallback scraping method using basic urllib."""
    print(f"\n--- [urllib] Searching YouTube for: '{query}' ---")
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
            
        m = re.search(r'var ytInitialData = (\{.*?\});', html_content)
        if not m:
            print("[Youtuber] Could not find YouTube data in the basic page.")
            return []
            
        data = json.loads(m.group(1))
        videos = parse_youtube_json(data)
        save_and_print_results(videos)
        return videos
    except Exception as e:
        print(f"[Youtuber] urllib error: {e}")
        return []

def parse_youtube_json(data):
    """Helper to navigate the complex YouTube JSON structure."""
    videos = []
    try:
        # Standard path for search results
        sections = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']
        
        for section in sections:
            if 'itemSectionRenderer' not in section:
                continue
            
            items = section['itemSectionRenderer']['contents']
            for item in items:
                if 'videoRenderer' in item:
                    vr = item['videoRenderer']
                    video_id = vr['videoId']
                    
                    title = ""
                    if 'title' in vr and 'runs' in vr['title']:
                        title = "".join([r['text'] for r in vr['title']['runs']])
                    
                    description = ""
                    if 'detailedMetadataSnippets' in vr:
                        runs = vr['detailedMetadataSnippets'][0].get('snippetText', {}).get('runs', [])
                        description = "".join([r['text'] for r in runs])
                    elif 'descriptionSnippet' in vr and 'runs' in vr['descriptionSnippet']:
                        description = "".join([r['text'] for r in vr['descriptionSnippet']['runs']])
                        
                    view_count = ""
                    if 'viewCountText' in vr and 'simpleText' in vr['viewCountText']:
                        view_count = vr['viewCountText']['simpleText']
                    elif 'shortViewCountText' in vr and 'simpleText' in vr['shortViewCountText']:
                        view_count = vr['shortViewCountText']['simpleText']

                    publish_date = ""
                    if 'publishedTimeText' in vr and 'simpleText' in vr['publishedTimeText']:
                        publish_date = vr['publishedTimeText']['simpleText']
                        
                    videos.append({
                        "title": title,
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                        "description": description,
                        "id": video_id,
                        "views": view_count,
                        "publish_date": publish_date
                    })
    except (KeyError, IndexError):
        pass
    return videos

def save_and_print_results(videos):
    """Helper to output and persist results."""
    if videos:
        print(f"Found {len(videos)} videos:\n")
        # Use simple counter to avoid slice lint issues
        count = 0
        for vid in videos:
            if count >= 15:
                break
            count += 1
            print(f"{count}. {vid['title']}")
            print(f"   URL: {vid['url']}")
            if vid['views'] or vid['publish_date']:
                stats = [vid['views']] if vid['views'] else []
                if vid['publish_date']: stats.append(vid['publish_date'])
                print(f"   Stats: {' • '.join(stats)}")
            if vid['description']:
                desc = str(vid['description'])
                # Safe slice for linter
                desc_text = desc[0:150] if len(desc) > 150 else desc
                print(f"   Description: {desc_text}...")
            print()
    else:
        print("No videos found.")
        
    try:
        with open('youtube_search_results.json', 'w', encoding='utf-8') as f:
            json.dump(videos, f, indent=4, ensure_ascii=False)
        print("> Results saved to youtube_search_results.json")
    except Exception as e:
        print(f"Could not save JSON: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 youtube_search.py <QUERY>")
        sys.exit(1)
        
    query = " ".join(sys.argv[1:])
    
    # Try Playwright first, then fallback
    get_youtube_videos_playwright(query)

if __name__ == "__main__":
    main()
