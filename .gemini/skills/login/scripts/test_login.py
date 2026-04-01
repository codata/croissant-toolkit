import os
import sys
import subprocess
from pathlib import Path

def test_login_unvault():
    print("Testing Login Skill: Automated Unvaulting...")
    
    script_path = Path(__file__).parent / "login_orchestrator.py"
    
    # Run login - should result in successful unpack of at least one skill
    result = subprocess.run(
        ["python3", str(script_path)],
        capture_output=True, text=True, check=True
    )
    
    # Check for authentication Success
    if "Restored successfully" in result.stdout:
         print("✅ Success: Skill unvaulted using authorized candidates.")
    else:
         print("❌ Fail: Unvaulting failed!")
         # print("Output was:", result.stdout)
         sys.exit(1)

if __name__ == "__main__":
    test_login_unvault()
