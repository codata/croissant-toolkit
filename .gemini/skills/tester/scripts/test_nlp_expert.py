import subprocess
import os
import sys
import json

def main():
    text = "Google was founded by Larry Page and Sergey Brin in 1998 in California."
    print(f"Testing NLP Expert Skill with text: '{text}'")
    
    # Check if API KEY exists
    if not os.getenv("GEMINI_API_KEY"):
        print("SKIP: GEMINI_API_KEY not set, skipping live NLP test.")
        sys.exit(0)
    
    try:
        result = subprocess.run(
            ["python3", ".gemini/skills/nlp_expert/scripts/extract_entities.py", text],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            print(f"FAIL: NLP script exited with code {result.returncode}")
            print(result.stderr)
            sys.exit(1)
            
        if "Extracted Entities" in result.stdout:
            print("SUCCESS: NLP extraction successful.")
            # Archive for tracking
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            history_dir = os.path.join("data", "nlp_expert")
            if not os.path.exists(history_dir):
                os.makedirs(history_dir)
            history_file = os.path.join(history_dir, f"test_results_{timestamp}.txt")
            with open(history_file, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            print(f"> NLP test data archived to {history_file}")
        else:
            print("FAIL: NLP output missing expected markers.")
            print(result.stdout)
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR: Failed to run NLP expert skill: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
