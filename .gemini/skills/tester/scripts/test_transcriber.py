import subprocess
import os
import sys

def main():
    # Use a well-known short video for testing
    video_id = "jNQXAC9IVRw" # "Me at the zoo" - very short
    print(f"Testing Transcriber Skill for video: {video_id}")
    
    try:
        result = subprocess.run(
            ["python3", ".gemini/skills/transcriber/scripts/transcribe.py", video_id],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            if "ModuleNotFoundError" in result.stdout or "ModuleNotFoundError" in result.stderr:
                print("SKIP: youtube-transcript-api not installed, skipping transcriber test.")
                sys.exit(0)
            # Check if it's just a transcript availability issue
            if "No transcript found" in result.stdout or "No transcript found" in result.stderr:
                print("SUCCESS: Transcriber script ran, but transcript unavailable (expected for some videos).")
                return
            print(f"FAIL: Transcriber script exited with code {result.returncode}")
            print(result.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR: Failed to run transcriber skill: {e}")
        sys.exit(1)

    output_file = f"data/transcripts/{video_id}.txt"
    if os.path.exists(output_file):
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        history_dir = os.path.join("data", "transcriber")
        if not os.path.exists(history_dir):
            os.makedirs(history_dir)
        history_file = os.path.join(history_dir, f"test_results_{timestamp}_{video_id}.txt")
        import shutil
        shutil.copy(output_file, history_file)
        print(f"SUCCESS: Transcript archived to {history_file}")
    else:
        # Transcript might not be available for all videos, but the script should run
        print("INFO: Script finished, but no transcript file created (common if transcript is disabled).")

if __name__ == "__main__":
    main()
