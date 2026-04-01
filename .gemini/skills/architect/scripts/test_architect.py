import os
import sys
import subprocess
from pathlib import Path

def test_architect_mermaid():
    print("Testing Architect Skill: Mermaid Diagram Generation...")
    
    script_path = Path(__file__).parent / "architect.py"
    
    # Run architect for a simple system
    result = subprocess.run(
        ["python3", str(script_path), "A simple web app with a database"],
        capture_output=True, text=True, check=True
    )
    
    # Check for Mermaid code blocks syntax
    if "graph TD" in result.stdout or "flowchart" in result.stdout:
         print("✅ Success: Mermaid diagram logic generated.")
    else:
         print("❌ Fail: Mermaid syntax not detected in output.")
         sys.exit(1)
         
    # Check for ADR (Architecture Decision Record)
    if "ADR" in result.stdout or "Architecture Decision" in result.stdout:
         print("✅ Success: ADR documentation included.")
    else:
         print("❌ Fail: ADR documentation missing.")
         sys.exit(1)

if __name__ == "__main__":
    test_architect_mermaid()
