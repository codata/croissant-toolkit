import os
import sys
import json
import google.generativeai as genai

def extract_entities(text):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return None
    
    genai.configure(api_key=api_key)
    # Using gemini-3-flash-preview for semantic extraction
    model = genai.GenerativeModel('gemini-3-flash-preview')
    
    prompt = f"""
    Act as an expert NLP system. Analyze the following text and extract all named entities:
    - Persons (People)
    - Organizations (Companies, Institutions)
    - Locations (Cities, Countries, Landmarks)
    - Dates (Specific days, months, years)

    Return the result ONLY as a valid JSON-LD object using Schema.org types (e.g., Person, Organization, Place, Event/Date).
    The structure should be a Dataset or an ItemList containing these entities.

    TEXT:
    {text}
    """
    
    try:
        response = model.generate_content(prompt)
        content = response.text.strip()
        
        # Cleanup markdown formatting if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        return json.loads(content)
    except Exception as e:
        print(f"Error during NLP extraction: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_entities.py <TEXT_OR_FILE_PATH>")
        sys.exit(1)
        
    input_val = " ".join(sys.argv[1:])
    
    # Check if input is a file path
    if os.path.isfile(input_val):
        try:
            with open(input_val, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"Processing content from file: {input_val}")
        except Exception as e:
            print(f"Error reading file {input_val}: {e}")
            sys.exit(1)
    else:
        content = input_val
        
    result = extract_entities(content)
    
    if result:
        print("\n--- Extracted Entities (JSON-LD) ---")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Save output
        output_dir = "data/nlp"
        os.makedirs(output_dir, exist_ok=True)
        
        if os.path.isfile(input_val):
            filename = os.path.basename(input_val)
            output_path = os.path.join(output_dir, f"{filename}.entities.jsonld")
        else:
            output_path = os.path.join(output_dir, "extracted_entities.jsonld")
            
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            
        print(f"\n> Saved JSON-LD to: {output_path}")
    else:
        print("NLP extraction failed.")

if __name__ == "__main__":
    main()
