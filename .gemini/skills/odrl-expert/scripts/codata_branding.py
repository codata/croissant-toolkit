import os
import argparse
import json
from playwright.sync_api import sync_playwright

CODATA_LOGO_URL = "https://codata.org/wp-content/uploads/2019/12/codata_new_logo-1.png"

def create_branded_pdf(content, output_path, title="CODATA RESEARCH REPORT"):
    """
    Creates a PDF with the CODATA branding on every page.
    Uses Playwright's header/footer templates for persistent branding.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                margin: 40px;
                padding-top: 60px; /* Space for header */
                padding-bottom: 60px; /* Space for footer */
                color: #2c3e50;
                line-height: 1.6;
            }}
            .content-container {{
                max-width: 800px;
                margin: auto;
            }}
            h1 {{ color: #2980b9; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
            pre {{ background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #eee; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <div class="content-container">
            <h1>{title}</h1>
            <div id="main-content">
                {content}
            </div>
        </div>
    </body>
    </html>
    """
    
    # We'll use a specific header and footer for Playwright's PDF generator
    header_html = f"""
    <div style="font-size: 10px; width: 100%; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #ddd; padding: 10px 40px;">
        <img src="{CODATA_LOGO_URL}" style="height: 30px;" />
        <span style="color: #666; font-weight: bold;">{title}</span>
    </div>
    """
    
    footer_html = f"""
    <div style="font-size: 10px; width: 100%; text-align: center; color: #999; padding: 10px 40px; border-top: 1px solid #ddd;">
        CODATA - The Committee on Data for Science and Technology | Page <span class="pageNumber"></span> of <span class="totalPages"></span>
    </div>
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(html_content)
        
        # We must set display_header_footer and provide templates
        # Important: the CSS in templates is isolated from the main page
        page.pdf(
            path=output_path,
            display_header_footer=True,
            header_template=header_html,
            footer_template=footer_html,
            # No printBackground: true here? Actually true is usually better
            print_background=True,
            # Margins must be set for headers/footers to appear correctly
            margin={
                "top": "80px",
                "bottom": "80px",
                "right": "40px",
                "left": "40px"
            },
            # A4 or other standard
            format="A4"
        )
        browser.close()
    
    print(f"[CODATA Branding] PDF generated successfully: {output_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CODATA Report Branding Subskill")
    parser.add_argument("--content", help="HTML or Plain Text content")
    parser.add_argument("--file", help="Path to input file")
    parser.add_argument("--output", default="data/branded_report.pdf", help="Output PDF path")
    parser.add_argument("--title", default="CODATA RESEARCH REPORT", help="Report Title")
    
    args = parser.parse_args()
    
    content_raw = args.content
    if args.file and os.path.exists(args.file):
        with open(args.file, 'r') as f:
            content_raw = f.read()
    
    if not content_raw:
        content_raw = "<p>No content provided.</p>"
        
    create_branded_pdf(content_raw, args.output, args.title)
