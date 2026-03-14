import json
import subprocess
import os
import sys
import datetime

def main():
    query = "croissant ml format"
    print(f"Testing Youtuber Skill for query: '{query}'")
    try:
        result = subprocess.run(
            ["python3", ".gemini/skills/youtuber/scripts/youtube_search.py", query],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            print(f"FAIL: Youtuber script exited with code {result.returncode}")
            print(result.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR: Failed to run youtuber skill: {e}")
        sys.exit(1)

    actual_file = "youtube_search_results.json"
    if not os.path.exists(actual_file):
        print(f"FAIL: {actual_file} was not generated.")
        sys.exit(1)

    try:
        with open(actual_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        history_dir = os.path.join("data", "youtuber")
        if not os.path.exists(history_dir):
            os.makedirs(history_dir)
        history_file = os.path.join(history_dir, f"test_results_{timestamp}.json")
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"> YouTube test data archived to {history_file}")

        if len(data) > 0:
            print(f"SUCCESS: Found {len(data)} YouTube videos.")
        else:
            print("FAIL: No YouTube videos found.")
            sys.exit(1)
    except Exception as e:
        print(f"ERROR during validation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
