---
name: photograph
description: Captures visual snapshots (screenshots) of web pages and records screen sessions (video).
---

# 📸 Photograph Skill (formerly Screenshot Taker)

The Photograph skill allows the toolkit to capture visual snapshots of web pages and record screen activity. This is useful for archiving dataset sources, verifying page content, recording process execution for proof-of-work, or feeding visual data into Gemini's multimodal reasoning engine.

## Features
- **High-Quality Screenshots**: Capture web pages using Playwright (High-Fidelity).
- **Screen Recording**: Record the entire screen (macOS) while a specific process is running.
- **Headless Mode**: Captured quietly in the background (default for screenshots).
- **Auto-Consent Handling**: Automatically handles "Accept Cookies" popups.
- **Process Sync**: Video recording automatically starts before a command and stops when it finishes.

## Setup
This skill requires `playwright` and `ffmpeg`. Run the following commands to set it up:

```bash
pip install playwright
playwright install chromium
brew install ffmpeg  # On macOS
```

## Usage

### 1. Screenshots
Capture a web page. You can capture a single snapshot or two snapshots (Begin/End) to see how the page evolves (e.g., after popups are handled).

```bash
# Simple screenshot
python3 .gemini/skills/photograph/scripts/take_screenshot.py "https://mlcommons.org/croissant"

# Dual-state capture (Begin @ 0s, End @ 12s)
python3 .gemini/skills/photograph/scripts/take_screenshot.py "https://google.com" --dual-state --delay 12
```

### 2. Screen Recording (New!)
Record the screen while a specific command is being executed. The recording will automatically stop when the command completes.

```bash
python3 .gemini/skills/photograph/scripts/record_screen.py --command "python3 main.py run" --output demo.mp4
```

### 3. Fixed Duration Recording
Record the screen for 10 seconds.
```bash
python3 .gemini/skills/photograph/scripts/record_screen.py --duration 10 --output short_clip.mp4
```

### 4. Advanced Recording (New!)
Record a specific screen with audio, or list available devices.

```bash
# List available screens and microphones
python3 .gemini/skills/photograph/scripts/record_screen.py --list-devices

# Record Screen 1 with Audio enabled
python3 .gemini/skills/photograph/scripts/record_screen.py --screen 2 --audio --duration 5 --output multiscreen.mp4
```

## Integration
This skill can be used by the **Orchestrator** to visually verify pages or provide a video log of long-running data integration processes.
