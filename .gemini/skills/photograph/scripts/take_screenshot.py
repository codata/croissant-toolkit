import os
import sys
import argparse
import time

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("[Screenshot Taker] Error: 'playwright' library not found.")
    print("Please install it using: pip install playwright && playwright install chromium")
    sys.exit(1)

def take_screenshot(url, output_path, full_page=False, headless=True, wait_ms=2000, locale="en-US", dual_state=False, delay_ms=12000, trigger_text="Run Test"):
    """
    Opens a URL and takes a screenshot using Playwright.
    If dual_state is True:
      1. Capture 'begin' shot at 0s.
      2. Find and click button with trigger_text.
      3. Wait for delay_ms.
      4. Capture 'end' shot.
    """
    print(f"[Screenshot Taker] Navigating to: {url} (Locale: {locale})")
    
    # Ensure the directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                locale=locale
            )
            page = context.new_page()
            
            # Go to the URL and wait for the network to remain idle
            page.goto(url, wait_until="networkidle", timeout=60000)

            if dual_state:
                # 1. Capture "Begin" state immediately after load
                begin_path = output_path.replace(".png", "_begin.png")
                print(f"[Screenshot Taker] Capturing 'BEGIN' state: {begin_path}")
                page.screenshot(path=begin_path, full_page=full_page)

            # --- YouTube Ad Handling ---
            if "youtube.com/watch" in url or "youtu.be/" in url:
                print("[Screenshot Taker] YouTube video detected. Checking for ads...")
                try:
                    # Give the player a moment to start and show ads
                    page.wait_for_timeout(3000)
                    
                    # Maximum wait for ads: 60 seconds
                    for i in range(30):
                        # Detect ad components
                        ad_overlay = page.query_selector(".ytp-ad-player-overlay, .ytp-ad-module")
                        if ad_overlay and ad_overlay.is_visible():
                            # Try skip button
                            skip_selectors = [
                                ".ytp-ad-skip-button",
                                ".ytp-ad-skip-button-modern",
                                "button.ytp-ad-skip-button",
                                "div.ytp-ad-skip-button-slot"
                            ]
                            skipped = False
                            for sel in skip_selectors:
                                btn = page.query_selector(sel)
                                if btn and btn.is_visible():
                                    print("[Screenshot Taker] Skip button found. Skipping ad...")
                                    btn.click()
                                    page.wait_for_timeout(1000)
                                    skipped = True
                                    break
                            
                            if not skipped:
                                if i % 5 == 0:
                                    print(f"[Screenshot Taker] Ad playing... waiting ({i*2}s elapsed)...")
                                page.wait_for_timeout(2000)
                        else:
                            # No ad or ad finished
                            break
                    print("[Screenshot Taker] YouTube ad check finalized.")
                except Exception as ad_err:
                    print(f"[Screenshot Taker] YouTube ad handler error: {ad_err}")

            # --- Consent Handling Logic ---
            try:
                # Give a moment for overlays to appear
                page.wait_for_timeout(2000)
                
                # Broad range of target texts for consent buttons
                target_texts = [
                    "Tout accepter", "J'accepte", "Accepter", 
                    "Accept all", "I agree", "Agree", "Accept", 
                    "Allow all", "OK", "Tout autoriser"
                ]
                
                for text in target_texts:
                    # Try to find the button by text
                    btn = page.get_by_role("button", name=text, exact=False)
                    if btn.count() > 0:
                        first_btn = btn.first
                        if first_btn.is_visible():
                            print(f"[Screenshot Taker] Found consent button with text: '{text}'. Clicking...")
                            first_btn.click()
                            # Wait for the page to react and clear the overlay
                            page.wait_for_load_state("networkidle", timeout=5000)
                            page.wait_for_timeout(1000)
                            break
            except Exception as ce:
                print(f"[Screenshot Taker] Consent handling note: {ce}")
            
            # --- Trigger Action (New!) ---
            if dual_state and trigger_text:
                print(f"[Screenshot Taker] Searching for trigger button: '{trigger_text}'...")
                try:
                    # Look for button by text (case-insensitive)
                    btn = page.get_by_role("button", name=trigger_text, exact=False)
                    if btn.count() == 0:
                        # Fallback to link or general clickable if button role doesn't match
                        btn = page.get_by_text(trigger_text, exact=False)
                    
                    if btn.count() > 0:
                        first_btn = btn.first
                        if first_btn.is_visible():
                            print(f"[Screenshot Taker] Trigger found. Clicking '{trigger_text}'...")
                            first_btn.click()
                            # Wait for some movement after click
                            page.wait_for_timeout(1000)
                        else:
                            print(f"[Screenshot Taker] Trigger button '{trigger_text}' found but not visible.")
                    else:
                        print(f"[Screenshot Taker] Trigger button '{trigger_text}' not found.")
                except Exception as te:
                    print(f"[Screenshot Taker] Trigger click error: {te}")

            # Additional wait to ensure dynamic content / animations settle
            current_wait = delay_ms if dual_state else wait_ms
            if current_wait > 0:
                print(f"[Screenshot Taker] Waiting {current_wait}ms for {'END state' if dual_state else 'animations'}...")
                page.wait_for_timeout(current_wait)
            
            final_path = output_path.replace(".png", "_end.png") if dual_state else output_path
            print(f"[Screenshot Taker] Capturing {'END' if dual_state else 'final'} screenshot to: {final_path}")
            page.screenshot(path=final_path, full_page=full_page)
            
            browser.close()
            return True, final_path
        except Exception as e:
            print(f"[Screenshot Taker] Failed to take screenshot: {e}")
            return False, None

def main():
    parser = argparse.ArgumentParser(description="Take a screenshot of a web page using a real browser engine.")
    parser.add_argument('url', help='The URL of the page to capture')
    parser.add_argument('--output', '-o', default='data/screenshots/screenshot.png', help='Path to save the screenshot')
    parser.add_argument('--full_page', action='store_true', help='Capture the entire scrollable page')
    parser.add_argument('--headful', action='store_false', dest='headless', help='Run with visible browser window')
    parser.add_argument('--wait', type=int, default=2000, help='Milliseconds to wait after load before snapping')
    parser.add_argument('--locale', default='fr-FR', help='Browser locale (e.g. fr-FR, en-US)')
    parser.add_argument('--dual-state', action='store_true', help='Capture both BEGIN (0s) and END (Ns) states')
    parser.add_argument('--delay', type=int, default=12, help='Delay in seconds for the END state (default: 12)')
    parser.add_argument('--trigger', default='Run Test', help='Text of the button to click for the END state trigger')
    
    # Set default headless to True
    parser.set_defaults(headless=True)
    
    args = parser.parse_args()
    
    # Auto-generate filename based on domain/timestamp if default is used
    target_output = str(args.output)
    if target_output == 'data/screenshots/screenshot.png':
        timestamp = int(time.time())
        from urllib.parse import urlparse
        parsed_url = urlparse(args.url)
        domain = parsed_url.netloc.replace('.', '_')
        if not domain:
            domain = "local_file"
        target_output = f"data/screenshots/{domain}_{timestamp}.png"

    success, final_path = take_screenshot(
        url=str(args.url),
        output_path=target_output,
        full_page=bool(args.full_page),
        headless=bool(args.headless),
        wait_ms=int(args.wait),
        locale=str(args.locale),
        dual_state=bool(args.dual_state),
        delay_ms=int(args.delay) * 1000,
        trigger_text=str(args.trigger)
    )
    
    if success:
        print(f"[Screenshot Taker] Process Complete!")
        # Output the path clearly for other tools/agent to use
        print(f"[RESULT_PATH]: {os.path.abspath(final_path)}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
