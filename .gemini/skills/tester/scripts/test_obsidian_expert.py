import json
import subprocess
import os
import sys

def main():
    test_data = {
        "@context": {"sc": "https://schema.org/"},
        "@type": "sc:Dataset",
        "name": {"@value": "Obsidian Test Dataset"},
        "description": "A test for Obsidian export",
        "url": "https://example.com/obsidian-test",
        "creator": [{"name": "Wizard"}],
        "keywords": ["test", "obsidian"]
    }
    
    input_file = "temp_obsidian_input.json"
    with open(input_file, 'w') as f:
        json.dump(test_data, f)
        
    print("Testing Obsidian Expert Skill (Markdown Export)")
    
    try:
        result = subprocess.run(
            ["python3", ".gemini/skills/obsidian_expert/scripts/to_obsidian.py", input_file, "data/obsidian_test"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            print(f"FAIL: Obsidian export failed with code {result.returncode}")
            print(result.stdout)
            print(result.stderr)
            sys.exit(1)
            
        output_file = "data/obsidian_test/Obsidian_Test_Dataset.md"
        if os.path.exists(output_file):
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            history_dir = os.path.join("data", "obsidian_expert")
            if not os.path.exists(history_dir):
                os.makedirs(history_dir)
            history_file = os.path.join(history_dir, f"test_results_{timestamp}.md")
            import shutil
            shutil.copy(output_file, history_file)
            
            with open(output_file, 'r') as f:
                content = f.read()
            if "type: dataset/croissant" in content and "Obsidian Test Dataset" in content:
                print(f"SUCCESS: Obsidian note created and archived to {history_file}")
            else:
                print("FAIL: Markdown content is incorrect.")
                print(content)
                sys.exit(1)
        else:
            print(f"FAIL: {output_file} was not generated.")
            sys.exit(1)
            
    finally:
        # Cleanup
        if os.path.exists(input_file): os.remove(input_file)
        if 'output_file' in locals() and os.path.exists(output_file):
            os.remove(output_file)

if __name__ == "__main__":
    main()
