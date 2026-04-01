import time
import os
import argparse
import sys
import json
from playwright.sync_api import sync_playwright

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    body {{
        margin: 0;
        padding: 0;
        font-family: 'Outfit', sans-serif;
        background: #F0F4F8;
        -webkit-print-color-adjust: exact !important;
    }}
    
    .page {{
        width: 800px;
        min-height: 1000px;
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        margin: 0 auto;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        position: relative;
        overflow: hidden;
    }}
    
    .header {{
        background: #1A1A2E; /* Dark Navy */
        color: white;
        padding: 14px 28px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0.03em;
    }}
    
    .sub-head {{
        padding: 24px 48px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #E2E8F0;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #4A5568;
    }}
    
    .content-area {{
        padding: 48px 72px;
    }}
    
    .category-pill {{
        display: inline-block;
        background: #EDF2F7;
        color: #4C51BF;
        padding: 8px 16px;
        border-radius: 99px;
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }}
    
    h1 {{
        color: #1A1A2E;
        font-size: 42px;
        margin-top: 0;
        margin-bottom: 48px;
        font-weight: 700;
        line-height: 1.2;
    }}
    
    .toc-container {{
        background: rgba(248, 250, 252, 0.8);
        border: 1px solid #EDF2F7;
        border-radius: 32px;
        padding: 40px;
        margin-top: 24px;
    }}
    
    .toc-item {{
        display: flex;
        align-items: center;
        margin-bottom: 28px;
        position: relative;
    }}
    
    .toc-text {{
        font-size: 22px;
        font-weight: 600;
        color: #2D3748;
        flex: 1;
        display: flex;
        align-items: center;
    }}
    
    .toc-text::after {{
        content: "";
        flex: 1;
        height: 2px;
        background: #E2E8F0;
        margin: 0 20px;
    }}
    
    .toc-bubble {{
        width: 44px;
        height: 44px;
        background: #4C51BF; /* Vibrant Purple/Indigo */
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 16px;
        box-shadow: 0 4px 10px rgba(76, 81, 191, 0.2);
        flex-shrink: 0;
    }}
    
    .toc-index {{
        margin-right: 16px;
        color: #4C51BF;
        font-weight: 700;
    }}

    .arrows {{
        position: absolute;
        top: 50%;
        width: 100%;
        display: flex;
        justify-content: space-between;
        padding: 0 10px;
        z-index: 10;
        pointer-events: none;
    }}
    
    .arrow-btn {{
        background: #1A1A2E;
        color: white;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        opacity: 0.9;
    }}

</style>
</head>
<body>
    <div class="page">
        <div class="header">
            <span>{header_left}</span>
            <span>{header_right}</span>
        </div>
        
        <div class="sub-head">
            <span>{sub_left}</span>
            <span>{sub_right}</span>
        </div>
        
        <div class="content-area">
            <div class="category-pill">{sub_left}</div>
            <h1>{main_title}</h1>
            
            <div class="toc-container">
                {items_html}
            </div>
        </div>
        
        <div class="arrows">
             <div class="arrow-btn" style="margin-left: -16px;">&lt;</div>
             <div class="arrow-btn" style="margin-right: -16px;">&gt;</div>
        </div>
    </div>
</body>
</html>
"""

def create_document(title, items, output_filename, header_left="Major insights", header_right="Preview 3 of 11 pages", sub_left="AI CODING BEST PRACTICES", sub_right="MARCH 2026"):
    items_html = ""
    for idx, item in enumerate(items):
        i = idx + 1
        items_html += f'''
        <div class="toc-item">
            <div class="toc-text">
                <span class="toc-index">{i}.</span> {item}
            </div>
            <div class="toc-bubble">{i + 2}</div>
        </div>
        '''
    
    final_html = HTML_TEMPLATE.format(
        header_left=header_left,
        header_right=header_right,
        sub_left=sub_left,
        sub_right=sub_right,
        main_title=title,
        items_html=items_html
    )
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(final_html)
        page.wait_for_load_state("networkidle")
        
        # Determine height based on content
        body_height = page.evaluate("document.body.scrollHeight")
        viewport_height = max(1000, body_height)
        
        page.set_viewport_size({"width": 800, "height": viewport_height})
        
        page.pdf(
            path=output_filename,
            width="800px",
            height=f"{viewport_height}px",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}
        )
        browser.close()
        print(f"[Editor] High-fidelity document saved to: {output_filename}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Editor: LinkedIn Document Generator")
    parser.add_argument('--title', default='Table of Contents', help='The main title of the page')
    parser.add_argument('--items', help='JSON array of items for the TOC')
    parser.add_argument('--output', default='social_post.pdf', help='Output PDF filename')
    parser.add_argument('--header-left', default='Major insights')
    parser.add_argument('--header-right', default='Preview 3 of 11 pages')
    parser.add_argument('--sub-left', default='AI CODING BEST PRACTICES')
    parser.add_argument('--sub-right', default='MARCH 2026')
    
    args = parser.parse_args()
    
    try:
        items = json.loads(args.items.replace("'", '"')) if args.items else [
            "Developers are accountable",
            "Over document your project context",
            "Keep it simple",
            "Absolutely, positively no stray code",
            "Analyze everything",
            "Mandatory unit tests",
            "Rigorous code reviews",
            "Tools for good habits"
        ]
    except:
        items = ["Error parsing items list."]
        
    create_document(
        args.title, items, args.output, 
        header_left=args.header_left, 
        header_right=args.header_right,
        sub_left=args.sub_left.upper(), 
        sub_right=args.sub_right.upper()
    )
