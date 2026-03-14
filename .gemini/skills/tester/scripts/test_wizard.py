import subprocess
import os
import sys

def main():
    # Use raw text input for a fast, reliable wizard test
    input_text = "The MNIST database is a large database of handwritten digits."
    dataset_name = "Wizard Test Dataset"
    print(f"Testing Wizard Skill with name: '{dataset_name}'")
    
    # We create a dummy transcript file to simulate transcribed input
    if not os.path.exists("data/transcripts"):
        os.makedirs("data/transcripts")
    with open("data/transcripts/wizard_dummy.txt", "w") as f:
        f.write(input_text)
        
    try:
        # Pass a long enough string to avoid it being detected as a YouTube ID (which is exactly 11 chars)
        # and ensure it's not a file path.
        result = subprocess.run(
            ["python3", ".gemini/skills/wizard/scripts/wizard.py", "This is a raw text input for the wizard test.", dataset_name],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            print(f"FAIL: Wizard failed with code {result.returncode}")
            print(result.stdout)
            print(result.stderr)
            sys.exit(1)
            
        output_filename = dataset_name.lower().replace(" ", "_") + ".jsonld"
        output_path = os.path.join("data", "croissant", output_filename)
        
        if os.path.exists(output_path):
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            history_dir = os.path.join("data", "wizard")
            if not os.path.exists(history_dir):
                os.makedirs(history_dir)
            history_file = os.path.join(history_dir, f"test_results_{timestamp}.json")
            import shutil
            shutil.copy(output_path, history_file)
            print(f"SUCCESS: Wizard generated {output_path} (archived to {history_file})")
        else:
            print(f"FAIL: {output_path} not found.")
            sys.exit(1)
            
    finally:
        # Cleanup
        if os.path.exists("data/transcripts/wizard_dummy.txt"):
            os.remove("data/transcripts/wizard_dummy.txt")
        if 'output_path' in locals() and os.path.exists(output_path):
            os.remove(output_path)

if __name__ == "__main__":
    main()
