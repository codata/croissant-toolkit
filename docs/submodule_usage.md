# Using Croissant Toolkit as a Git Submodule

You can easily reuse the **Croissant Toolkit** and all its specialized skills in your other projects by adding it as a Git submodule. This allows you to maintain the toolkit as a linked repository that can be updated independently.

## 1. Add the Submodule
Navigate to the root of your target project and run:

```bash
git submodule add https://github.com/codata/croissant-toolkit.git vendor/croissant-toolkit
```

This will clone the toolkit into a `vendor/croissant-toolkit` directory and track it in your `.gitmodules` file.

## 2. Initialize and Update
If you are cloning a project that already contains this submodule, you must initialize it:

```bash
git submodule update --init --recursive
```

To update to the latest version of the toolkit later:
```bash
git submodule update --remote vendor/croissant-toolkit
```

## 3. Reusing Skills in Python

To use the skills from the toolkit in your project's Python scripts, you need to add the toolkit directory to your `sys.path`.

### Method A: Runtime Path Addition
Add this snippet at the beginning of your scripts:

```python
import sys
import os
from pathlib import Path

# Path to the submodule
toolkit_root = Path(__file__).parent / "vendor" / "croissant-toolkit"
sys.path.append(str(toolkit_root))

# Now you can import or run toolkit scripts
# Example: Using the ODRL expert identity
from vendor.croissant_toolkit.skills.odrl_expert.scripts import odrl_client
```

### Method B: Environment Variable
Alternatively, set the `PYTHONPATH` before running your scripts:

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/vendor/croissant-toolkit
```

## 4. Example: Executing a Skill from another Repo

If you want to run a skill directly from your project's CLI:

```bash
# Execute the YouTuber skill within the submodule
python3 vendor/croissant-toolkit/.gemini/skills/youtuber/scripts/search_youtube.py "Data Engineering"
```

## 📐 Recommended Directory Structure

```text
my-new-project/
├── .git/
├── .gitmodules
├── src/
│   └── main.py (Reusing toolkit logic)
└── vendor/
    └── croissant-toolkit/ (The Submodule)
        ├── .gemini/skills/ (Available Skills)
        └── ...
```

By using submodules, you ensure that any improvements or new skills added to the main **Croissant Toolkit** repo can be easily pulled into all your active projects.
