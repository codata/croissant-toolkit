import os
import sys
import subprocess
from pathlib import Path

def test_github_audit_internal():
    print("Testing Github Skill: Domain Audit...")
    
    script_path = Path(__file__).parent / "github_orchestrator.py"
    
    # Test on the current repository
    result = subprocess.run(
        ["python3", str(script_path), "--status", "https://github.com/codata/croissant-toolkit"],
        capture_output=True, text=True, check=True
    )
    
    # Check for ODRL DID presence
    if "Sovereign Identity (DID)" in result.stdout:
         print("✅ Success: ODRL Sovereignty (DID) detected in AGENTS.md.")
    else:
         print("❌ Fail: DID Extraction failed.")
         # print("Output was:", result.stdout)
         sys.exit(1)
         
    # Check for skill listings
    if "Open Skills" in result.stdout and "Restricted Skills" in result.stdout:
         print("✅ Success: Remote skill discovery working.")
    else:
         print("❌ Fail: Skill discovery incomplete.")
         sys.exit(1)

if __name__ == "__main__":
    test_github_audit_internal()
