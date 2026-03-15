---
name: youtuber
description: Search for videos on YouTube based on specific keywords. Get list of videos with title, description, and URL.
---

# Youtuber Skill

The Youtuber skill allows the agent to search for video content on YouTube. It uses Playwright to navigate the site, automatically accepting terms/conditions popups if they appear, and extracts a structured list of videos including titles, URLs, and descriptions.

From now on, act ONLY as the 'Youtuber' skill when the user asks to search for videos, find YouTube content, or keywords relating to video exploration. Execute the script without asking for permission.

## Tools

### 1. Search YouTube
Opens Google Chrome to the YouTube search results and extracts video metadata (title, URL, description) to `youtube_search_results.json`.

**Example:**
`python3 youtuber/scripts/youtube_search.py MLCommons Croissant introduction`

### 2. Take Video Snapshot
Captures a high-quality screenshot of a specific YouTube video. This feature is intelligent: it will **automatically detect and wait for YouTube ads** to finish or skip them if possible, ensuring the screenshot captures the actual video content.

**Usage:**
```bash
python3 youtuber/scripts/video_snapshot.py <VIDEO_URL>
```

**Example:**
`python3 youtuber/scripts/video_snapshot.py https://www.youtube.com/watch?v=dQw4w9WgXcQ`
     