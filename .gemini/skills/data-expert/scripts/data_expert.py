import os
import sys
import json
import argparse
import requests
import subprocess
import hashlib
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

try:
    from PyPDF2 import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

def extract_pdf_contents(filepath):
    """Extracts text from a local PDF file."""
    if not PYPDF_AVAILABLE:
        print("[Data Expert] Error: PyPDF2 is required for PDF analysis. please install it.")
        return ""
    try:
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"[Data Expert] PDF Error: {e}")
        return ""

def load_url_contents(url):
    """Opens a URL and gets the rendered innerText."""
    if not PLAYWRIGHT_AVAILABLE:
        print("[Data Expert] Error: 'playwright' package is not installed. WebFetch currently unavailable.")
        return ""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=60000)
            content = page.evaluate("document.body.innerText")
            browser.close()
            return content
    except Exception as e:
        print(f"[Data Expert] WebFetch Error: {e}")
        return ""

def chunk_text(text, max_len=255):
    """Splits text into chunks of max_len characters."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_len = 0
    
    for word in words:
        if current_len + len(word) + 1 > max_len:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_len = len(word)
        else:
            current_chunk.append(word)
            current_len += len(word) + 1
            
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def perform_data_analysis(content):
    """
    Uses Gemini to extract quantitative/qualitative claims and assign probability.
    Returns: Dict containing 'claim' (narrative) and 'measurable_claims' (list).
    """
    api_key = os.getenv("GEMINI_API_KEY")
    agent_did = "did:oyd:zQmcVHWDMeXtj273A9gNAnEG2EdrGEjtQiFuw9PncyVgs9z" # Antigravity AI DID

    if not api_key:
        print("[Claims Detection] Error: GEMINI_API_KEY is not set.")
        return {"claim": "Missing API Key", "measurable_claims": []}
    
    api_key = api_key.strip()
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    prompt = f"""
    Analyze this document as an expert investigative journalist and fact-checker for the Croissant Toolkit.
    
    TASK:
    1. Identify all FACTUAL claims (Quantitative and Qualitative) that can be verified and used for "Claims Detection".
    2. For each, extract:
       - "sentence": the full literal sentence from the text containing the claim.
       - "original_claim": the specific quote or phrase that constitutes the factual claim itself.
       - "variableMeasured": the semantic name of the variable (e.g., "Monthly Revenue", "Global Temperature").
    3. Provide an INVESTIGATIVE assessment of the probability that each claim is "true" or "false" based on its internal consistency and logical context.
    
    DOCUMENT CONTENT:
    {content[:100000]}
    
    OUTPUT FORMAT:
    Return ONLY a JSON object with this schema:
    {{
      "claim": "a high-level, synthesized narrative of the document's core factual findings",
      "measurable_claims": [
        {{
          "claim": "the name or title of the identified claim (e.g. 'Measurement Campaigns')",
          "context": "the full literal sentence from the text containing the claim",
          "original_claim": "the specific quote or phrase constituting the claim",
          "variableMeasured": "schema.org name of the variable",
          "value": "extracted data value",
          "unit": "unit of measurement if any (e.g. °C, %, years)",
          "probability": 0.0 to 1.0,
          "explanation": "brief reasoning for the probability"
        }}
      ]
    }}
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        print(f"[Claims Detection] Extracting factual statements (Model: {model})...")
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"[Claims Detection] API Error {response.status_code}: {response.text}")
            return {"claim": f"API Error {response.status_code}", "measurable_claims": []}
        
        response_data = response.json()
        if "candidates" not in response_data:
            print("[Claims Detection] Error: No response candidates from AI.")
            return {"claim": "No AI candidates returned", "measurable_claims": []}

        result_raw = response_data["candidates"][0]["content"]["parts"][0]["text"].strip()
        # Clean potential markdown
        if result_raw.startswith("```"):
            result_raw = result_raw.split("\n", 1)[1].rsplit("\n", 1)[0]
        
        # Load and validate structure
        raw_data = json.loads(result_raw)
        
        # If model returns a list despite the prompt, wrap it
        if isinstance(raw_data, list):
            data = {
                "claim": "Aggregated findings from list output",
                "measurable_claims": raw_data
            }
        else:
            data = raw_data

        data["prov:wasAttributedTo"] = agent_did
        
        # Ensure measurable_claims exists and is a list
        if "measurable_claims" not in data or not isinstance(data["measurable_claims"], list):
            data["measurable_claims"] = []
            
        for c in data.get("measurable_claims", []):
            if isinstance(c, dict):
                c["prov:wasAttributedTo"] = agent_did
            
        return data
    except Exception as e:
        print(f"[Claims Detection] Analysis failed to parse JSON: {e}")
        return {"claim": f"Analysis failed: {str(e)}", "measurable_claims": []}

def main():
    parser = argparse.ArgumentParser(description="Claims Detection: Factual Statement Extraction & Probability Validation")
    parser.add_argument("source", help="Input: Raw string, URL, or Path to PDF")
    parser.add_argument("--json", action="store_true", help="Output pure JSON to stdout")
    args = parser.parse_args()
    
    source = args.source
    content = ""
    
    # 1. Determine Source Type
    if source.startswith(("http://", "https://")):
        print(f"[Data Expert] Fetching Web Content: {source}")
        content = load_url_contents(source)
    elif os.path.exists(source) and source.lower().endswith(".pdf"):
        print(f"[Data Expert] Reading PDF: {source}")
        content = extract_pdf_contents(source)
    elif os.path.exists(source):
        print(f"[Data Expert] Reading Local File: {source}")
        with open(source, "r") as f:
            content = f.read()
    else:
        # Assume it is a direct text input
        print(f"[Data Expert] Analyzing direct text input...")
        content = source
        
    if not content:
        print("[Data Expert] Error: Could not obtain content from source.")
        return

    # 2. Extract & Analyze (with Chunking)
    print(f"[Data Expert] Splitting content into chunks (max 255 chars)...")
    chunks = chunk_text(content, max_len=255)
    print(f"[Data Expert] Processing {len(chunks)} chunks...")
    
    all_measurable_claims = []
    narrative_parts = []
    
    for i, c in enumerate(chunks):
        print(f"[Data Expert] Analyzing chunk {i+1}/{len(chunks)}...")
        data = perform_data_analysis(c)
        if "measurable_claims" in data:
            for claim in data["measurable_claims"]:
                claim["chunk_id"] = i + 1
                all_measurable_claims.append(claim)
        if "claim" in data and data["claim"] not in ["Analysis failed", "Missing API Key"]:
            narrative_parts.append(data["claim"])

    # 3. Aggregate Data
    final_data = {
        "claim": " ".join(narrative_parts[:5]) + ("..." if len(narrative_parts) > 5 else ""),
        "measurable_claims": all_measurable_claims,
        "provenance": source,
        "total_chunks": len(chunks)
    }
    
    # 4. Post-Process: MD5 and schema alignment
    enhanced_claims = []
    base_id_url = "https://croissant.ai/claim/"
    
    # Ensure data is a dict (prevent AttributeError)
    if not isinstance(final_data, dict):
        final_data = {"claim": "System Error: Invalid response type", "measurable_claims": []}

    for entry in final_data.get("measurable_claims", []):
        if not isinstance(entry, dict):
            continue
        # Calculate unique MD5 hash for the claim context
        claim_text = entry.get("context", entry.get("claim", ""))
        claim_id = hashlib.md5(claim_text.encode('utf-8')).hexdigest()
        
        # Add metadata and schema enrichment
        entry["id"] = claim_id
        entry["@id"] = f"{base_id_url}{claim_id}"
        entry["link"] = entry["@id"]
        entry["provenance"] = source
        enhanced_claims.append(entry)

    # Add back to the main object
    final_data["measurable_claims"] = enhanced_claims

    # 5. Output
    if args.json:
        # Pure JSON output for piping/automation
        print(json.dumps(final_data, indent=2))
    else:
        print("\n--- CLAIMS DETECTION: FACTUAL ANALYSIS (CHUNKED) ---")
        print(json.dumps(final_data, indent=2))
    
    # Save to standard report path
    report_path = "data/claims.json"
    os.makedirs("data", exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(final_data, f, indent=2)
    
    if not args.json:
        print(f"\n[Claims Detection] Detailed report saved to: {os.path.abspath(report_path)}")

if __name__ == "__main__":
    main()
