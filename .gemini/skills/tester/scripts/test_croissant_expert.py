import json
import subprocess
import os
import sys

def main():
    test_metadata = {
        "name": "Test Dataset",
        "description": "A metadata serialization test",
        "url": "https://example.com/test",
        "distribution": [
            {"name": "file-1", "contentUrl": "data.csv", "encodingFormat": "text/csv"}
        ],
        "recordSet": [
            {
                "name": "default",
                "field": [
                    {"name": "test-col", "dataType": "sc:Text", "source_file": "file-1", "extract_column": "col1"}
                ]
            }
        ]
    }
    
    input_file = "temp_test_metadata.json"
    output_file = "temp_test_croissant.json"
    
    with open(input_file, 'w') as f:
        json.dump(test_metadata, f)
        
    print("Testing Croissant Expert Skill (Serialization)")
    
    try:
        result = subprocess.run(
            ["python3", ".gemini/skills/croissant_expert/scripts/serialize.py", input_file, "temp_test_croissant.json"],
            capture_output=True,
            text=True,
            check=False
        )
        
        # The script prepends 'data/croissant/' to the output filename if no path is provided
        actual_output_path = os.path.join("data", "croissant", output_file)
        
        if result.returncode != 0:
            print(f"FAIL: Serialization failed with code {result.returncode}")
            print(result.stderr)
            sys.exit(1)
            
        if not os.path.exists(actual_output_path):
            print(f"FAIL: {actual_output_path} was not generated.")
            sys.exit(1)
            
        with open(actual_output_path, 'r') as f:
            croissant_data = json.load(f)
            
        if croissant_data.get("@type") == "sc:Dataset" and croissant_data.get("name", {}).get("@value") == "Test Dataset":
            print("SUCCESS: Croissant JSON-LD generated correctly.")
            # Archive for tracking
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            history_dir = os.path.join("data", "croissant_expert")
            if not os.path.exists(history_dir):
                os.makedirs(history_dir)
            history_file = os.path.join(history_dir, f"test_results_{timestamp}.json")
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(croissant_data, f, indent=4, ensure_ascii=False)
            print(f"> Croissant test data archived to {history_file}")
        else:
            print("FAIL: Generated Croissant data structure is incorrect.")
            print(json.dumps(croissant_data, indent=2))
            sys.exit(1)
            
    finally:
        # Cleanup
        if os.path.exists(input_file): os.remove(input_file)
        actual_output_path = os.path.join("data", "croissant", "temp_test_croissant.json")
        if os.path.exists(actual_output_path): os.remove(actual_output_path)

if __name__ == "__main__":
    main()
