---
name: tester
description: Test the navigator skill by verifying that it returns at least 10 relevant search results for a given query.
---

# Tester Skill

This skill is used to verify the correctness of the Navigator skill by running a live search and validating that the output contains at least 10 results relevant to the search query.

## Usage

### Run Navigator Test
Executes the navigator script with the "gemini" query and validates the resulting `google_search_results.json`.

**Command:**
```bash
python3 skills/tester/scripts/test_navigator.py
```

## Resources

### scripts/
- `test_navigator.py`: Automates the execution and validation process.
