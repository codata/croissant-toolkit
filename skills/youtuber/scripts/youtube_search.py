import sys
import urllib.parse
import urllib.request
import urllib.error
import re
import subprocess
import webbrowser
import json
import html as html_lib

def get_youtube_videos(query):
    print(f"\n--- Searching YouTube for: '{query}' ---")
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
            
        # YouTube embeds results in a JSON object called ytInitialData
        m = re.search(r'var ytInitialData = (\{.*?\});', html_content)
        if not m:
            print("Could not find YouTube data in the page.")
            return []
            
        data = json.loads(m.group(1))
        
        # Navigate the complex YouTube JSON structure to find video renderers
        # contents -> twoColumnSearchResultsRenderer -> primaryContents -> sectionListRenderer -> contents
        # -> itemSectionRenderer -> contents -> videoRenderer
        
        videos = []
        try:
            # This path can vary slightly, so we iterate through sections
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
                            # snippet is usually here in modern layout
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
        except (KeyError, IndexError) as e:
            print(f"Error navigating YouTube JSON: {e}")

        # Print all found videos
        if videos:
            all_vids = list(videos)
            print(f"Found {len(all_vids)} videos:\n")
            for idx, vid in enumerate(all_vids, start=1):
                if idx > 15:
                    break
                print(f"{idx}. {vid['title']}")
                print(f"   URL: {vid['url']}")
                if vid['views'] or vid['publish_date']:
                    stats = []
                    if vid['views']: stats.append(str(vid['views']))
                    if vid['publish_date']: stats.append(str(vid['publish_date']))
                    print(f"   Stats: {' • '.join(stats)}")
                if vid['description']:
                    desc = str(vid['description'])
                    if len(desc) > 150:
                        desc_chunk = ""
                        for i in range(150):
                            desc_chunk += desc[i]
                        print(f"   Description: {desc_chunk}...")
                    else:
                        print(f"   Description: {desc}")
                print()
        else:
            print("No videos found.")
            
        # Save to a JSON file
        try:
            with open('youtube_search_results.json', 'w', encoding='utf-8') as f:
                json.dump(videos, f, indent=4, ensure_ascii=False)
            print("> Results saved to youtube_search_results.json")
        except Exception as e:
            print(f"Could not save JSON: {e}")
            
        return videos

    except urllib.error.URLError as e:
        print(f"Failed to fetch YouTube page: {e}")
        return []
    except Exception as e:
        print(f"Error while parsing YouTube results: {e}")
        return []


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 youtube_search.py <QUERY>")
        sys.exit(1)
        
    query = ""
    for i in range(1, len(sys.argv)):
        if query:
            query += " "
        query += sys.argv[i]
    
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"
    
    print(f"Opening Google Chrome to YouTube search for: '{query}'")
    
    try:
        # target macOS Google Chrome using the 'open' command
        result = subprocess.run(["open", "-a", "Google Chrome", url], check=False, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Successfully requested browser to open.")
        else:
            print("Trying default browser fallback...")
            webbrowser.open(url)
            
    except Exception as e:
        print(f"Error opening browser: {e}")
        webbrowser.open(url)

    # Scrape the results
    get_youtube_videos(query)


if __name__ == "__main__":
    main()
