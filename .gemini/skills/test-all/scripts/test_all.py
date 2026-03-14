import os
import subprocess
import sys
import glob

def main():
    print("--- Running All Tests ---")
    
    # Find all test scripts in the .gemini/skills directory
    project_root = os.getcwd() # Assume we run from project root
    search_pattern = os.path.join(project_root, ".gemini", "skills", "**", "scripts", "test_*.py")
    test_files = glob.glob(search_pattern, recursive=True)
    
    if not test_files:
        print("No tests found.")
        sys.exit(0)
        
    print(f"Found {len(test_files)} test file(s).")
    
    results = {}
    passed = 0
    failed = 0
    
    for test_file in test_files:
        # Avoid running ourselves in an infinite loop
        if test_file.endswith("test_all.py"):
            continue
            
        rel_path = os.path.relpath(test_file, project_root)
        print(f"\n[RUNNING] {rel_path}")
        try:
            result = subprocess.run(
                ["python3", test_file],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                print(f"[SUCCESS] {rel_path}")
                results[test_file] = "PASS"
                passed += 1
            else:
                print(f"[FAIL] {rel_path}")
                print(f"--- Output ---\n{result.stdout}")
                print(f"--- Error ---\n{result.stderr}")
                results[test_file] = "FAIL"
                failed += 1
                
        except Exception as e:
            print(f"[ERROR] Failed to execute {test_file}: {e}")
            results[test_file] = "ERROR"
            failed += 1
            
    print("\n--- Summary ---")
    print(f"Total Tests Run: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
