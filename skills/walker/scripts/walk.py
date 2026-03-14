import os
import sys
import urllib.parse
import urllib.request
import re
import argparse
import subprocess
import ssl
import json
import google.generativeai as genai

def get_html(url):
    """Fetches HTML content with SSL bypass for resilience."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"[Walker] Failed to fetch {url}: {e}")
        return ""

def extract_links(html, base_url):
    """Extracts internal links from HTML, filtering out static assets."""
    parsed_uri = urllib.parse.urlparse(base_url)
    links = re.findall(r'href=["\'](.[^"\']+)["\']', html)
    
    internal_links = set()
    ignore_ext = ('.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip', '.gz', '.css', '.js', '.woff2', '.svg', '.json', '.ico')
    
    for link in links:
        full_link = urllib.parse.urljoin(base_url, link)
        parsed_link = urllib.parse.urlparse(full_link)
        
        if parsed_link.netloc == parsed_uri.netloc:
            # Reconstruct clean link without fragments
            clean_link = f"{parsed_link.scheme}://{parsed_link.netloc}{parsed_link.path}"
            if clean_link.lower().endswith(ignore_ext):
                continue
            if clean_link != base_url:
                internal_links.add(clean_link)
    
    return sorted(list(internal_links))

def ask_gemini(content, question):
    """Uses Gemini 3 to find a specific answer within page content."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[Walker] Warning: GEMINI_API_KEY not set. Skipping AI analysis.")
        return None
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3-flash-preview')
    
    # Strip HTML tags and normalize whitespace to save context window
    clean_text = re.sub(r'<[^>]+>', ' ', content)
    clean_text = ' '.join(clean_text.split())
    
    # Cap at 15k characters for efficiency
    text_chunk = clean_text[0:15000]
    
    prompt = f"""
    Analyze the following webpage content and answer the question: "{question}"
    
    If the precise answer is NOT found in the text, simply say "NOT_FOUND".
    Otherwise, provide the concise answer.
    
    CONTENT:
    {text_chunk} 
    """
    
    try:
        response = model.generate_content(prompt)
        answer = response.text.strip()
        return answer
    except Exception as e:
        print(f"[Walker] Gemini error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Walk through internal links of a website to find specific information.")
    parser.add_argument('url', help='The base URL to walk from')
    parser.add_argument('--query', help='Optional question to answer while walking')
    parser.add_argument('--limit', type=int, default=5, help='Limit the number of internal links to explore')
    
    args = parser.parse_args()
    
    print(f"\n[Walker] Starting walk for: {args.url}")
    if args.query:
        print(f"[Walker] Target Question: {args.query}")

    # Initial page check
    html = get_html(args.url)
    if not html:
        print("[Walker] Could not load base URL. Aborting.")
        return

    if args.query:
        answer = ask_gemini(html, args.query)
        if answer and answer != "NOT_FOUND":
            print(f"\n--- [RESULT FOUND ON MAIN PAGE] ---\n{answer}\n")
            return

    # Extract and explore internal links
    links = extract_links(html, args.url)
    print(f"[Walker] Found {len(links)} internal links to explore.")
    
    all_links = list(links)
    visit_limit = int(args.limit)
    to_visit = all_links[0:visit_limit]
    
    for link in to_visit:
        target_link = str(link)
        print(f" - Exploring: {target_link}")
        link_html = get_html(target_link)
        if not link_html:
            continue
            
        if args.query:
            answer = ask_gemini(link_html, args.query)
            if answer and answer != "NOT_FOUND":
                print(f"\n--- [RESULT FOUND ON: {target_link}] ---\n{answer}\n")
                return

    if args.query:
        print("\n[Walker] Finished walk. Information could not be located on the main page or its internal links.")
        print("[TIP] This site might require JavaScript rendering (e.g. Next.js). Try using the Navigator to open it in a real browser.")

if __name__ == "__main__":
    main()
