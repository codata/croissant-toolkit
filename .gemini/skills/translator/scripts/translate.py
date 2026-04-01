import os
import sys
import json
import subprocess

def translate_text(text, target_language="English"):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return None
    
    # Using stable v1 API and Gemini 2.5 Flash
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    prompt = f"""
    Act as a professional translator. 
    1. Detect the language of the following text.
    2. Precisely translate the text into {target_language}, maintaining the original meaning, tone, and technical context.
    
    Return your response ONLY as a valid JSON object in this format:
    {{
        "detected_language": "string",
        "translated_text": "string"
    }}
    
    TEXT:
    {text}
    """
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        # Use curl to bypass local library issues
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", url, "-H", "Content-Type: application/json", "-d", json.dumps(payload)],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Curl failed: {result.stderr}")
            return None
            
        response_data = json.loads(result.stdout)
        if "candidates" not in response_data:
            print(f"API Error: {result.stdout}")
            return None
            
        content = response_data["candidates"][0]["content"]["parts"][0]["text"].strip()
        
        # Basic cleanup in case Gemini wraps the JSON in markdown blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        return json.loads(content)
    except Exception as e:
        print(f"Error during Gemini translation process: {e}")
        return None

def compute_unf(text):
    """Call the unf skill to compute hash."""
    unf_script = ".gemini/skills/unf/scripts/unf_hash.py"
    if not os.path.exists(unf_script):
        return None
    
    try:
        result = subprocess.run(
            ["python3", unf_script, text],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Error computing UNF: {e}")
        return None

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Translator Skill with UNF support.")
    parser.add_argument("input", help="Text or file path to translate.")
    parser.add_argument("--target", default="English", help="Target language (e.g., French).")
    parser.add_argument("--unf", action="store_true", help="Compute UNF hash of the translated output.")
    
    args = parser.parse_args()
    
    input_val = args.input
    
    # Check if input is a file path
    if os.path.exists(input_val) and os.path.isfile(input_val):
        try:
            with open(input_val, 'r', encoding='utf-8') as f:
                text_to_translate = f.read()
                print(f"Translating content from file: {input_val}")
        except Exception as e:
            print(f"Error reading file {input_val}: {e}")
            sys.exit(1)
    else:
        text_to_translate = input_val
        
    result = translate_text(text_to_translate, target_language=args.target)
    
    if result:
        print(f"\n[Language Recognition]: {result.get('detected_language')}")
        print(f"[Target Language]: {args.target}")
        print("-" * 50)
        translated_text = result.get('translated_text')
        print(f"[{args.target} Translation]:")
        print(translated_text)
        print("-" * 50)
        
        if args.unf:
            unf_val = compute_unf(translated_text)
            print(f"[UNF Fingerprint]: {unf_val}")
            print("-" * 50)
        
        # If it was a file, save the translation for persistence
        if os.path.exists(input_val) and os.path.isfile(input_val):
            suffix = args.target[:2].lower()
            base, ext = os.path.splitext(input_val)
            output_path = f"{base}_{suffix}.txt"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translated_text)
            print(f"Done! Translation saved to: {output_path}")
    else:
        print("Translation process failed.")

if __name__ == "__main__":
    main()
