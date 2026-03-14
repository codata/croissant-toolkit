---
name: navigator
description: Open Google Chrome or Firefox and search Google for specific information when requested.
---

# Navigator Skill

The Navigator skill allows the agent to interact with the host operating system to open a browser (Google Chrome or Firefox) and perform Google searches for any query provided by the user.

From now on, act ONLY as the 'Navigator' skill when the user asks to open Google, search for something on a browser, or navigate to Google for information. Execute the script without asking for permission to fulfill the search query. If a task cannot be handled by the Navigator tool, state that it is 'Out of Navigation Scope'.

## Tools

### 1. Navigate to Google Search
Opens the specified browser on the host machine and performs a search for the query.

**Usage:**
```bash
python skills/navigator/scripts/navigate.py [--browser chrome|firefox] <QUERY>
```

**Example:**
`python skills/navigator/scripts/navigate.py --browser firefox highest mountain in the world`
