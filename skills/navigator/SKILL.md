---
name: navigator
description: Open Google Chrome or Firefox, search Google, and extract all web pages from the search results.
---

# Navigator Skill

The Navigator skill allows the agent to interact with the host operating system to open a browser (Google Chrome or Firefox), perform Google searches, and automatically scrape and collect all web pages from the search results.

From now on, act ONLY as the 'Navigator' skill when the user asks to open Google, search for something on a browser, or navigate to Google for information. Execute the script without asking for permission to fulfill the search query. The script will open the browser AND return a parsed list of search result URLs, saving them to `google_search_results.json` for further use.

## Tools

### 1. Navigate to Google Search and Collect Results
Opens the specified browser on the host machine, performs a search for the query, prints the extracted web links from the first page of Google, and saves the links to a local JSON file.

**Usage:**
```bash
python skills/navigator/scripts/navigate.py [--browser chrome|firefox] <QUERY>
```

**Example:**
`python skills/navigator/scripts/navigate.py --browser firefox highest mountain in the world`
