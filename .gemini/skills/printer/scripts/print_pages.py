import time
import os
import argparse
import sys
import subprocess
from playwright.sync_api import sync_playwright
try:
    from PyPDF2 import PdfWriter, PdfReader
except ImportError:
    print("[Printer] Error: PyPDF2 not found. Please run 'pip install PyPDF2'")
    sys.exit(1)

def dismiss_popups(page):
    """Handles common cookie consent popups and dismissing banners/modals."""
    try:
        consent_texts = [
            "Tout accepter", "J'accepte", "Accepter", 
            "Accept all", "I agree", "Agree", "Accept", "I Accept", "Consent",
            "Allow all", "OK", "Tout autoriser", "Accept All",
            "Прийняти", "Згоден", "Згода", "Погоджуюсь"
        ]
        close_texts = [
            "Close", "Fermer", "Dismiss", "Ignore", "No thanks", "Maybe later", "X",
            "Read more", "Expand", "Afficher plus", "See more"
        ]
        target_texts = consent_texts + close_texts
        
        page.evaluate("""() => {
            const backdrops = document.querySelectorAll('.modal-backdrop, .overlay, .sp-message-backdrop');
            backdrops.forEach(el => el.remove());
            document.body.style.overflow = 'auto';
            document.body.style.position = 'static';
        }""")

        # 3. Direct selector check for common modals
        selectors = ["button.fc-cta-consent", "button.fc-primary-button", ".fc-consent-root button"]
        for sel in selectors:
            btn = page.locator(sel)
            if btn.count() > 0:
                first_btn = btn.first
                if first_btn.is_visible():
                    print(f"[Printer] Dismissing modal via selector: '{sel}'")
                    first_btn.click()
                    page.wait_for_timeout(1000)
                    break

        for text in target_texts:
            btn = page.get_by_role("button", name=text, exact=False)
            if btn.count() == 0:
                btn = page.get_by_text(text, exact=True)
            if btn.count() > 0:
                first_btn = btn.first
                if first_btn.is_visible():
                    first_btn.click()
                    page.wait_for_timeout(500)
    except:
        pass

def clean_and_print(page, output_tmp_pdf):
    """Processes the page for a clean print and saves to a temp PDF."""
    # 1. Scroll to hydrate lazy content
    print(f"    - Loading lazy content...")
    page.evaluate("""async () => {
        const distance = 1000;
        const delay = 400;
        while (document.scrollingElement.scrollTop + window.innerHeight < document.scrollingElement.scrollHeight) {
            window.scrollBy(0, distance);
            await new Promise(resolve => setTimeout(resolve, delay));
        }
        window.scrollTo(0, 0);
    }""")
    time.sleep(1)

    # 2. Hide noise
    print(f"    - Cleaning layout...")
    page.evaluate("""() => {
        const hideSelectors = [
            'header', 'footer', 'nav', '.nav', '#header', '#footer',
            'aside', '.sidebar', '.ads', '.ad-container', '.sticky', 
            '.fixed', '.floating', '.social-share', '.comments-section',
            'button', 'iframe', '.banner', '.overlay', '.popup'
        ];
        document.querySelectorAll(hideSelectors.join(',')).forEach(el => {
            el.style.setProperty('display', 'none', 'important');
            el.style.setProperty('visibility', 'hidden', 'important');
        });
        const style = document.createElement('style');
        style.innerHTML = `
            @media print {
                * { -webkit-print-color-adjust: exact !important; printer-colors: exact !important; }
                body { margin: 0 !important; padding: 0 !important; }
            }
        `;
        document.head.appendChild(style);
    }""")

    # 3. Print
    page.emulate_media(media="print")
    page.pdf(
        path=output_tmp_pdf,
        format="A4",
        print_background=True,
        margin={"top": "1cm", "bottom": "1cm", "left": "1cm", "right": "1cm"}
    )
    print(f"    - Temporarily saved to {output_tmp_pdf}")

def run_printer(urls, final_output):
    temp_pdfs = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 1024})
        page = context.new_page()

        for idx, url in enumerate(urls):
            print(f"[Printer] Processing URL {idx+1}/{len(urls)}: {url}")
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                dismiss_popups(page)
                time.sleep(1)
                
                tmp_path = f"tmp_print_{idx}.pdf"
                clean_and_print(page, tmp_path)
                temp_pdfs.append(tmp_path)
            except Exception as e:
                print(f"[Printer] Error processing {url}: {e}")

        browser.close()

    # Merge PDFs if needed
    if len(temp_pdfs) == 0:
        print("[Printer] No PDFs were generated. Exiting.")
        return

    if len(temp_pdfs) == 1:
        if os.path.exists(final_output):
            os.remove(final_output)
        os.rename(temp_pdfs[0], final_output)
        print(f"[Printer] Success! Single page saved to: {final_output}")
    else:
        print(f"[Printer] Merging {len(temp_pdfs)} pages into {final_output}...")
        writer = PdfWriter()
        for pdf in temp_pdfs:
            reader = PdfReader(pdf)
            for p_idx in range(len(reader.pages)):
                writer.add_page(reader.pages[p_idx])
            os.remove(pdf) # Cleanup temp
        
        with open(final_output, "wb") as f:
            writer.write(f)
        print(f"[Printer] Success! Combined PDF saved to: {final_output}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Printer Skill: Web to Clean PDF")
    parser.add_argument('urls', nargs='+', help='One or more URLs to print')
    parser.add_argument('--output', default='output_print.pdf', help='Final PDF filename')
    args = parser.parse_args()
    
    # Ensure output has .pdf extension
    out = args.output
    if not out.lower().endswith(".pdf"):
        out += ".pdf"
        
    run_printer(args.urls, out)
