import os
import sys
import json
import google.generativeai as genai

def translate_text(text):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return None
    
    genai.configure(api_key=api_key)
    # Using gemini-1.5-flash for speed and reliability in translation
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Act as a professional translator. 
    1. Detect the language of the following text.
    2. Precisely translate the text into English, maintaining the original meaning, tone, and technical context.
    
    Return your response ONLY as a valid JSON object in this format:
    {{
        "detected_language": "string",
        "translated_text": "string"
    }}
    
    TEXT:
    {text}
    """
    
    try:
        response = model.generate_content(prompt)
        content = response.text.strip()
        
        # Basic cleanup in case Gemini wraps the JSON in markdown blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        return json.loads(content)
    except Exception as e:
        print(f"Error during Gemini translation process: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 translate.py <TEXT_OR_FILE_PATH>")
        sys.exit(1)
        
    input_val = " ".join(sys.argv[1:])
    
    # Check if input is a file path
    if os.path.isfile(input_val):
        try:
            with open(input_val, 'r', encoding='utf-8') as f:
                text_to_translate = f.read()
                print(f"Transcribing/Translating content from file: {input_val}")
        except Exception as e:
            print(f"Error reading file {input_val}: {e}")
            sys.exit(1)
    else:
        text_to_translate = input_val
        
    result = translate_text(text_to_translate)
    
    if result:
        print(f"\n[Language Recognition]: {result.get('detected_language')}")
        print("-" * 50)
        print("[English Translation]:")
        print(result.get('translated_text'))
        print("-" * 50)
        
        # If it was a file, save the translation for persistence
        if os.path.isfile(input_val):
            base, ext = os.path.splitext(input_val)
            output_path = f"{base}_en.txt"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.get('translated_text'))
            print(f"Done! Translation saved to: {output_path}")
    else:
        print("Translation process failed.")

if __name__ == "__main__":
    main()
