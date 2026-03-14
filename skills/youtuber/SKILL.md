---
name: youtuber
description: Search for videos on YouTube based on specific keywords. Get list of videos with title, description, and URL.
---

# Youtuber Skill

The Youtuber skill allows the agent to search for video content on YouTube. It opens the search results in Google Chrome and also extracts a structured list of videos including titles, URLs, and descriptions.

From now on, act ONLY as the 'Youtuber' skill when the user asks to search for videos, find YouTube content, or keywords relating to video exploration. Execute the script without asking for permission.

## Tools

### 1. Search YouTube
Opens Google Chrome to the YouTube search results and extracts video metadata (title, URL, description) to `youtube_search_results.json`.

**Usage:**
```bash
python3 youtuber/scripts/youtube_search.py <KEYWORDS>
```

**Example:**
`python3 youtuber/scripts/youtube_search.py MLCommons Croissant introduction`
