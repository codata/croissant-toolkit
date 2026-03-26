import time
import os
import json
import argparse
import sys
import subprocess
import re
from playwright.sync_api import sync_playwright

try:
    from PyPDF2 import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

def extract_pdf_text(filepath):
    """Extracts text from a local PDF file."""
    if not PYPDF_AVAILABLE:
        print("[Fact Checker] Warning: PyPDF2 not installed. Falling back to simple page text.")
        return ""
    try:
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"[Fact Checker] Error reading PDF: {e}")
        return ""

def download_pdf(page, url):
    """Downloads a PDF from a URL using Playwright/curl."""
    pdf_filename = "/tmp/arxiv_temp.pdf"
    print(f"[Fact Checker] Downloading PDF for deep analysis: {url}")
    # Simple use of curl/subprocess if it's a direct URL
    try:
        subprocess.run(["curl", "-s", "-L", url, "-o", pdf_filename], check=True)
        return pdf_filename
    except:
        return None

def get_extended_analysis(text, mode="visioner"):
    """
    Uses Gemini to perform deep 'Visioner' analysis.
    Returns (findings, innovation_summary).
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or len(api_key) < 20:
        print(f"[Visioner] Caution: GEMINI_API_KEY (len={len(api_key) if api_key else 0}) is missing or too short.")
        # Return a sample finding to demonstrate the UI even without a key
        notice = [{
            "text": "Abstract", 
            "explanation": "COGNITIVE NOTICE: Deep AI verification is currently in 'Visual Scan' mode. To enable full fact-checking, please export a valid GEMINI_API_KEY."
        }]
        return notice, "Analysis skipped due to missing credentials."
    
    # Use flash-latest with v1beta as it is the most stable for diverse keys
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    
    prompt_task = """
    Analyze this BROWSER_RENDERED_HTML as a ruthless cognitive scientist and high-sensitivity investigative journalist.

    1. Identify ALL sensitive claims involving:
       - Employment terminations (sacking, firing, layoffs, resignations).
       - Interpersonal or corporate conflicts.
       - Legal proceedings, court cases, or regulatory actions.
       - Factual contradictions related to these high-stakes events.
    2. Provide a 'rich AI comment' for each, specifying the conflict or event.
    3. Synthesize the paper or article's genuine innovation or underlying impact on the field.
    """
    
    prompt = f"""
    {prompt_task}
    
    BROWSER_HTML:
    {text[:80000]}
    
    OUTPUT FORMAT:
    Return ONLY a JSON object with this exact schema:
    {{
      "findings": [
        {{
          "text": "exact quote from the BROWSER_HTML", 
          "explanation": "Investigative breakdown of the sensitive event or conflict"
        }}
      ],
      "innovation_summary": "Synthetic summary of the genuine innovation or hidden impact"
    }}
    """
    
    # Use generationConfig for reliable JSON output in v1beta
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.1
        }
    }
    
    try:
        print(f"[Investigator] Performing sensitive event scan...")
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", url, "-H", "Content-Type: application/json", "-d", json.dumps(payload)],
            capture_output=True, text=True
        )
        
        response_data = json.loads(result.stdout)
        if "candidates" not in response_data:
            msg = response_data.get('error', {}).get('message', 'Unknown API Error')
            print(f"[Investigator] API Error: {msg}")
            # Log full response if it's not a quota issue
            if "quota" not in msg.lower():
                print(f"[Investigator] Full Result: {result.stdout}")
            return [], "Analysis failed due to API Error."

        content_raw = response_data["candidates"][0]["content"]["parts"][0]["text"].strip()
        # Strip potential markdown blocks if present (though responseMimeType should handle it)
        if content_raw.startswith("```"):
            content_raw = content_raw.split("\n", 1)[1].rsplit("\n", 1)[0]
        
        data = json.loads(content_raw)
        return data.get("findings", []), data.get("innovation_summary", "No summary provided.")
    except Exception as e:
        print(f"[Investigator] Analysis failed: {e}")
        return []

def get_contradictions(text):
    f = get_extended_analysis(text)
    return f

def dismiss_popups(page):
    """Handles common cookie consent popups and dismissing banners/modals."""
    try:
        # 1. Handle cookie buttons
        consent_texts = [
            "Accept All", "Accept all", "Tout accepter", "J'accepte", "Accepter", 
            "I agree", "Agree", "Accept", "I Accept", "Consent",
            "Allow all", "OK", "Tout autoriser",
            "Прийняти", "Згоден", "Згода", "Погоджуюсь"
        ]
        close_texts = [
            "Close", "Fermer", "Dismiss", "Ignore", "No thanks", "X"
        ]
        target_texts = consent_texts + close_texts

        # Loop through all frames (Business Insider uses Sourcepoint in iframes)
        for frame in page.frames:
            # Common ID selectors
            sel_list = ["#didomi-notice-agree-button", "button[title='Accept All']", "button.sp_choice_type_11"]
            for s in sel_list:
                try:
                    b = frame.locator(s)
                    if b.count() > 0 and b.first.is_visible():
                        print(f"[Fact Checker] Dismissing popup in frame: {s}")
                        b.first.click(timeout=1000)
                except: pass

            for t in target_texts:
                try:
                    # Check for buttons
                    btn = frame.get_by_role("button", name=t, exact=False)
                    if btn.count() > 0 and btn.first.is_visible():
                        print(f"[Fact Checker] Dismissing text popup in frame: {t}")
                        btn.first.click(timeout=1000)
                except: pass

        # Aggressive Backdrop/Modal removal (main page context)
        page.evaluate("""() => {
            const bad = ['overlay', 'backdrop', 'consent', 'modal'];
            document.querySelectorAll('*').forEach(el => {
                bad.forEach(b => {
                    if (el.className && typeof el.className === 'string' && el.className.toLowerCase().includes(b)) el.remove();
                    if (el.id && el.id.toLowerCase().includes(b)) el.remove();
                });
            });
            document.documentElement.style.overflow = 'auto';
            document.body.style.overflow = 'auto';
        }""")
    except:
        pass

INJECT_JS = """
window.vizHighlight = async (finding) => {
    if (!finding || !finding.text) return false;
    
    // Ensure the Gemini Status Bar exists
    let statusBar = document.getElementById('gemini-status-bar');
    if (!statusBar && document.body) {
        // Load Premium Typography
        if (!document.getElementById('gemini-fonts')) {
            const link = document.createElement('link');
            link.id = 'gemini-fonts';
            link.rel = 'stylesheet';
            link.href = 'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700;800;900&display=swap';
            document.head.appendChild(link);
        }

        statusBar = document.createElement('div');
        statusBar.id = 'gemini-status-bar';
        statusBar.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 20px;
            right: 20px;
            background: rgba(10, 10, 10, 0.85);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            color: #FFFFFF;
            padding: 30px 40px;
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            z-index: 2147483647;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-top: 4px solid #1DA1F2;
            box-shadow: 0 20px 50px rgba(0,0,0,0.9);
            border-radius: 12px;
            transform: translateY(150%);
            transition: transform 0.8s cubic-bezier(0.19, 1, 0.22, 1);
            display: flex;
            flex-direction: column;
            gap: 15px;
        `;
        document.body.appendChild(statusBar);
    }

    const setStatus = (html) => {
        if (statusBar) {
            statusBar.innerHTML = html;
            statusBar.style.transform = 'translateY(0)';
        }
    };

    setStatus(`
        <div style="display: flex; align-items: center; gap: 15px;">
            <div class="spinner" style="width: 18px; height: 18px; border: 3px solid rgba(29, 161, 242, 0.2); border-top-color: #1DA1F2; border-radius: 50%; animation: spin 1s cubic-bezier(0.4, 0, 0.2, 1) infinite;"></div>
            <strong style="color: #1DA1F2; font-size: 14px; text-transform: uppercase; letter-spacing: 2px; font-weight: 700;">Cognitive Scan</strong>
        </div>
        <div style="font-size: 18px; opacity: 0.7; font-style: italic; font-weight: 300; letter-spacing: -0.5px;">"${finding.text.substring(0, 100)}..."</div>
        <style>@keyframes spin { to { transform: rotate(360deg); } }</style>
    `);

    const normalize = (s) => (s || "").replace(/\\s+/g, ' ').toLowerCase().trim();
    const findDeepest = (text) => {
        const normalizedSearch = normalize(text);
        if (!normalizedSearch) return null;
        
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
        let node;
        // 1. Try Exact Match
        while(node = walker.nextNode()) {
            if (normalize(node.textContent).includes(normalizedSearch)) return node.parentElement;
        }
        
        // 2. Try Fuzzy Match (First 50 chars) if long
        if (normalizedSearch.length > 50) {
            const shortSearch = normalizedSearch.substring(0, 50);
            const walker2 = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
            while(node = walker2.nextNode()) {
                if (normalize(node.textContent).includes(shortSearch)) return node.parentElement;
            }
        }
        return null;
    };

    let target = findDeepest(finding.text);
    if (!target) {
        // More aggressive scroll to bottom for long BI articles
        for (let i = 0; i < 20; i++) {
            window.scrollBy(0, 1000);
            await new Promise(r => setTimeout(r, 800));
            target = findDeepest(finding.text);
            if (target) break;
        }
    }
    
    if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'center' });
        await new Promise(r => setTimeout(r, 1000));
        
        target.style.transition = 'all 0.6s ease-in-out';
        target.style.backgroundColor = 'rgba(255, 255, 0, 0.45)';
        target.style.boxShadow = '0 0 20px 8px #FFD700';
        target.style.borderRadius = '2px';
        target.style.color = '#000000';
        
        setStatus(`
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <svg viewBox="0 0 24 24" style="width: 28px; height: 28px; fill: #1DA1F2;"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"></path></svg>
                    <strong style="color: #1DA1F2; font-size: 22px; font-weight: 800; letter-spacing: -0.5px;">Gemini 3.1</strong>
                </div>
                <span style="background: linear-gradient(135deg, #1DA1F2, #00D2FF); color: #FFF; font-size: 11px; padding: 4px 12px; border-radius: 20px; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 4px 15px rgba(29, 161, 242, 0.3);">Contextual Fact-Check</span>
            </div>
            <div style="line-height: 1.5; font-size: 22px; color: #FFFFFF; font-weight: 400; letter-spacing: -0.3px;">${finding.explanation}</div>
            <div style="margin-top: 15px; font-size: 14px; color: rgba(255, 255, 255, 0.4); border-top: 1px solid rgba(255, 255, 255, 0.1); padding-top: 15px; font-style: italic;">
                Verified Claim: "${finding.text.substring(0, 150)}..."
            </div>
        `);
        
        await new Promise(r => setTimeout(r, 9000));
        
        statusBar.style.transform = 'translateY(150%)';
        target.style.backgroundColor = 'transparent';
        target.style.boxShadow = 'none';
        target.style.color = '';
        
        await new Promise(r => setTimeout(r, 800));
        return true;
    } else {
        statusBar.style.transform = 'translateY(150%)';
        return false;
    }
};
"""

def run_fact_check(url, findings=None, output_video_name="fact_check.webm", auto_analyze=False):
    video_dir = "data/recordings"
    os.makedirs(video_dir, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir=video_dir,
            record_video_size={"width": 1280, "height": 720},
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # --- Navigating ---
        print(f"[Fact Checker] Opening {url}...")
        page.goto(url, wait_until="networkidle", timeout=60000)
        
        # 1. Handle popups/consent immediately after load
        dismiss_popups(page)
        time.sleep(1) # stabilization
        
        actual_findings = findings or []
        
        # WebFetch-style extraction (render full HTML after popup dismissal)
        print(f"[Fact Checker] Performing 'WebFetch' of full rendered HTML...")
        findings_source = page.content()
        
        if auto_analyze:
            # Analyze based on full HTML context
            actual_findings, innovation_summary = get_extended_analysis(findings_source)
            print(f"[Investigator] Scan complete. Found {len(actual_findings)} sensitive findings.")
            print(f"[Innovation] {innovation_summary}")
        
        # --- SPECIAL INVESTIGATOR STEP: Proceed directly to highlights ---
        print(f"[Investigator] Highlighting sensitive events...")

        # 2. Sequential Highlights
        for item in actual_findings:
            page.evaluate(INJECT_JS)
            print(f"  [Visualization] Highlighting: {item['text'][:50]}...")
            try:
                found = page.evaluate("async finding => await window.vizHighlight(finding)", item)
                if not found:
                    print(f"    - Notice: Content match not found on page.")
            except Exception as e:
                print(f"    - Visualization Error: {e}")
            
            dismiss_popups(page)
            time.sleep(1)
        
        page.evaluate("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })")
        time.sleep(1)
        
        video_path = page.video.path()
        context.close()
        browser.close()
        
        final_path = os.path.join(video_dir, output_video_name)
        if os.path.exists(final_path):
            os.remove(final_path)
            
        # Rename to final format
        os.rename(video_path, final_path)
        print(f"[Fact Checker] Success! [RESULT_PATH]: {os.path.abspath(final_path)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Automated Fact Checker")
    parser.add_argument('url', help='The URL or local file path')
    parser.add_argument('--findings', help='JSON string of findings')
    parser.add_argument('--output', default='fact_check_report.webm', help='Output video filename')
    parser.add_argument('--auto', action='store_true', help='Use Gemini for analysis')
    args = parser.parse_args()
    
    findings_list = json.loads(args.findings) if args.findings else None
    run_fact_check(args.url, findings_list, args.output, args.auto)
