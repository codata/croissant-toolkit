---
name: walker
description: Deep crawl functionality that extracts and visits internal links from a webpage.
---

# 🚶 Walker Skill

The Walker skill provides "deep dive" capabilities for the toolkit. It allows the agent to explore a website by extracting all internal links from a given page and optionally visiting them in a browser.

This is particularly useful when a high-level search (via `Navigator`) doesn't provide enough information and the agent needs to "drill down" into a specific domain.

## Features
- **Link Extraction**: Parses HTML to find all links sharing the same domain as the parent page.
- **Normalization**: Automatically handles relative paths and cleans fragments.
- **Automated Navigation**: Can trigger the host browser to visit discovered pages.
- **Data Persistence**: Stores lists of discovered links in `./data/walker/` for future reference.

## Usage

### 1. Extract Links from a URL
```bash
python3 skills/walker/scripts/walk.py "https://example.com"
```

### 2. Extract and Automatically Open in Browser
```bash
python3 skills/walker/scripts/walk.py "https://example.com" --navigate --limit 3
```

## How it integrates
When the **Navigator** or **Wizard** encounters a page that seems relevant but lacks detail, the **Walker** can be invoked to expand the search perimeter within that specific site.
