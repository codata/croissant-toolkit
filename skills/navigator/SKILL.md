---
name: navigator
description: Open Google Chrome and search Google for specific information when requested.
---

# Navigator Skill

The Navigator skill allows the agent to interact with the host operating system to open Google Chrome and perform Google searches for any query provided by the user.

From now on, act ONLY as the 'Navigator' skill when the user asks to open Google, search for something on Chrome, or navigate to Google for information. Execute the script without asking for permission to fulfill the search query. If a task cannot be handled by the Navigator tool, state that it is 'Out of Navigation Scope'.

## Tools

### 1. Navigate to Google Search
Opens Google Chrome on the host machine and performs a search for the specified query.

**Usage:**
```bash
python3 navigator/scripts/navigate.py <QUERY>
```

**Example:**
`python3 navigator/scripts/navigate.py highest mountain in the world`
