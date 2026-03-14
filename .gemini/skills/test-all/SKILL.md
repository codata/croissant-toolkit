---
name: test-all
description: Discovers and executes all test scripts across all skills in the project to verify system integrity. Use this to run a comprehensive test suite.
---

# Test All Skill

This skill automatically discovers and runs all available test scripts (files named `test_*.py`) within the `skills/` directories, providing a consolidated report of successes and failures.

## Usage

### Run All Tests
Execute the script to find and run all tests.

**Command:**
```bash
python3 skills/test-all/scripts/test_all.py
```

## Resources

### scripts/
- `test_all.py`: The main test runner script.
