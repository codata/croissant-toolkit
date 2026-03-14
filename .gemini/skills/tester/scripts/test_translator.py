import subprocess
import os
import sys

def main():
    text = "Ceci est un test pour le traducteur."
    print(f"Testing Translator Skill with text: '{text}'")
    
    # Check if API KEY exists
    if not os.getenv("GEMINI_API_KEY"):
        print("SKIP: GEMINI_API_KEY not set, skipping live translation test.")
        sys.exit(0)
    
    try:
        result = subprocess.run(
            ["python3", ".gemini/skills/translator/scripts/translate.py", text],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            print(f"FAIL: Translator script exited with code {result.returncode}")
            print(result.stderr)
            sys.exit(1)
            
        if "English Translation" in result.stdout:
            print("SUCCESS: Live translation successful.")
            # Archive for tracking
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            history_dir = os.path.join("data", "translator")
            if not os.path.exists(history_dir):
                os.makedirs(history_dir)
            history_file = os.path.join(history_dir, f"test_results_{timestamp}.txt")
            with open(history_file, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            print(f"> Translation test data archived to {history_file}")
        else:
            print("FAIL: Translation output missing expected keywords.")
            print(result.stdout)
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR: Failed to run translator skill: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
