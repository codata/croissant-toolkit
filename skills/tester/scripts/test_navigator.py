import json
import subprocess
import os
import sys

def main():
    # 1. Run the navigator skill for "gemini"
    print("Running navigator skill for 'gemini'...")
    try:
        # Use absolute or relative path to the navigator script
        # We assume we are running from the project root
        result = subprocess.run(
            ["python3", "skills/navigator/scripts/navigate.py", "gemini"],
            capture_output=True,
            text=True,
            check=False
        )
        print(result.stdout)
        if result.stderr:
            print(f"Error output: {result.stderr}")
    except Exception as e:
        print(f"Failed to run navigator skill: {e}")
        sys.exit(1)

    # 2. Paths to the files
    actual_file = "google_search_results.json"

    if not os.path.exists(actual_file):
        print(f"FAIL: {actual_file} was not generated.")
        sys.exit(1)

    # 3. Validate the results
    try:
        with open(actual_file, 'r', encoding='utf-8') as f:
            actual_data = json.load(f)

        # 4. Save results to data folder for tracking
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        history_file = os.path.join("data", f"test_results_{timestamp}.json")
        
        try:
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(actual_data, f, indent=4, ensure_ascii=False)
            print(f"> Test data archived to {history_file}")
        except Exception as e:
            print(f"Warning: Could not archive test data: {e}")

        print(f"Validating {len(actual_data)} results...")

        # 1. Check count
        if len(actual_data) < 10:
            print(f"FAIL: Expected at least 10 results, but found {len(actual_data)}.")
            sys.exit(1)

        # 2. Check relevance (heuristic: at least 80% should mention 'gemini')
        query_terms = ["gemini"]
        relevant_results = []
        for r in actual_data:
            text_to_check = (r.get('title', '') + " " + r.get('snippet', '')).lower()
            if any(term in text_to_check for term in query_terms):
                relevant_results.append(r)
        
        relevance_ratio = len(relevant_results) / len(actual_data)
        
        if len(relevant_results) >= 8:
            print(f"SUCCESS: Found {len(actual_data)} results, with {len(relevant_results)} being highly relevant ({relevance_ratio:.0%}).")
        else:
            print(f"FAIL: Only {len(relevant_results)} out of {len(actual_data)} results seem relevant to 'gemini'.")
            sys.exit(1)

    except Exception as e:
        print(f"Error during validation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
