import os
import sys
import subprocess
from pathlib import Path

def test_unf_hashing():
    print("Testing UNF Skill: String Hashing...")
    
    script_path = Path(__file__).parent / "unf_hash.py"
    
    # Test 1: Simple string
    result = subprocess.run(
        ["python3", str(script_path), "temperature is celcius"],
        capture_output=True, text=True, check=True
    )
    unf1 = result.stdout.strip().split(": ")[-1]
    
    # Test 2: Order-invariant string (should be same as Test 1)
    result = subprocess.run(
        ["python3", str(script_path), "celcius is temperature"],
        capture_output=True, text=True, check=True
    )
    unf2 = result.stdout.strip().split(": ")[-1]
    
    if unf1 == unf2:
        print(f"✅ Success: Semantic hashing is order-invariant. UNF: {unf1}")
    else:
        print(f"❌ Fail: UNF mismatch! {unf1} != {unf2}")
        sys.exit(1)

if __name__ == "__main__":
    test_unf_hashing()
