import subprocess
import os
import sys

def main():
    recipient = "test@example.com"
    subject = "Wizard Skill: Test Email"
    body = "This is a test of the Communication Officer skill."
    print(f"Testing Communication Officer Skill (Sending to {recipient})")
    
    # Check for credentials
    if not os.getenv("SMTP_USER") or not os.getenv("SMTP_PASS"):
        print("SKIP: SMTP credentials not set, skipping live email test.")
        sys.exit(0)
    
    try:
        result = subprocess.run(
            ["python3", ".gemini/skills/communication_officer/scripts/send_email.py", recipient, subject, body],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0 and "successfully sent" in result.stdout.lower():
            print("SUCCESS: Email sent successfully.")
            # Archive for tracking
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            history_dir = os.path.join("data", "communication_officer")
            if not os.path.exists(history_dir):
                os.makedirs(history_dir)
            history_file = os.path.join(history_dir, f"test_results_{timestamp}.txt")
            with open(history_file, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            print(f"> Communication test data archived to {history_file}")
        else:
            print("FAIL: Communication script failed.")
            print(result.stdout)
            print(result.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR: Failed to run communication officer skill: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
