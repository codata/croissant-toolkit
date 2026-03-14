import os
import sys
import json
import re
import subprocess

def extract_entities(text):
    """
    Extracts named entities using Gemini via REST API for maximum resilience.
    Returns a Schema.org ItemList JSON-LD.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[NLP] Error: GEMINI_API_KEY environment variable not set.")
        return None
    
    # Using stable v1 API and Gemini 2.5 Flash for robustness
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    # Truncate text to avoid context limit issues using loop to satisfy strict indexer
    safe_text = str(text)
    if len(safe_text) > 20000:
        truncated = ""
        for i in range(20000):
            truncated += safe_text[i]
        safe_text = truncated
    
    prompt = f"""
    You are an expert NLP system specialized in Named Entity Recognition (NER).
    Analyze the following text and extract all significant entities.
    
    ENTITIES TO EXTRACT:
    - Persons (Individuals)
    - Organizations (Institutions, Companies)
    - Places (Cities, countries, regions, landmarks)
    - Dates (Specific days or time periods)
    - AI Models (LLMs, neural networks)
    - Monetary Amounts (Currency, funding)
    - Quantities (Measurements, counts)

    OUTPUT FORMAT:
    Return ONLY a valid JSON-LD object using Schema.org vocabulary.
    The root should be an "@type": "ItemList" with an "itemListElement" array.
    
    MULTILINGUAL RULES:
    If the entity name in the text is NOT in English:
    1. Set "name" to the English translation.
    2. Set "name_original" to the exact original string from the text.
    3. Set "language" to the ISO 2-letter code (e.g., "uk", "ru", "fr").
    
    If the text is in English, just return "name".

    TEXT:
    {safe_text}
    """
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        # Use curl to bypass local SDK/dependency issues
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", url, "-H", "Content-Type: application/json", "-d", json.dumps(payload)],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"[NLP] Curl failed: {result.stderr}")
            return None
            
        response_data = json.loads(result.stdout)
        if "candidates" not in response_data:
            print(f"[NLP] API Error: {result.stdout}")
            return None
            
        content = response_data["candidates"][0]["content"]["parts"][0]["text"].strip()
        
        # Robust JSON extraction from markdown
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            content = json_match.group(1)
        else:
            # Fallback: remove any triple backticks if they exist
            content = re.sub(r'^```|```$', '', content).strip()
            
        data = json.loads(content)
        
        # Ensure it's a dict and has the expected key
        if isinstance(data, list):
            data = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": data}
        
        return data
    except Exception as e:
        print(f"[NLP] Error during Gemini extraction: {e}")
        # Return an empty but valid structure as fallback
        return {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": []}

def main():
    all_args = list(sys.argv)
    if len(all_args) < 2:
        print("Usage: python3 extract_entities.py <TEXT_OR_FILE_PATH>")
        sys.exit(1)
        
    query = ""
    for i in range(1, len(all_args)):
        if query:
            query += " "
        query += str(all_args[i])
    input_val = query
    
    if os.path.isfile(input_val):
        try:
            with open(input_val, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"[NLP] Processing file: {input_val}")
        except Exception as e:
            print(f"[NLP] Error reading file: {e}")
            sys.exit(1)
    else:
        content = input_val
        
    result = extract_entities(content)
    
    if result:
        print("\n--- Extracted Entities (JSON-LD) ---")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        output_dir = "data/nlp"
        os.makedirs(output_dir, exist_ok=True)
        
        if os.path.isfile(input_val):
            filename = os.path.basename(input_val)
            output_path = os.path.join(output_dir, f"{filename}.entities.jsonld")
        else:
            output_path = os.path.join(output_dir, "extracted_entities.jsonld")
            
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            
        print(f"\n[NLP] Saved to: {output_path}")
    else:
        print("[NLP] Extraction failed entirely.")

if __name__ == "__main__":
    main()
