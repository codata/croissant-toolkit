# Photograph Skill

The Photograph skill enables the toolkit to capture visual snapshots of web pages and record screen activity. It uses Playwright for snapshots and FFmpeg for screen recording.

## Core functionality
- **High-Fidelity Captures**: Uses a real Chromium browser to render pages exactly as a user would see them.
- **Screen Recording**: Capture video of the OS screen while a command is running.
- **Dynamic Content Support**: Automatically waits for network activity to settle during web captures.
- **Process Sync**: Recording automatically tracks the life cycle of a subprocess.

## Setup

This skill requires `playwright`, `chromium`, and `ffmpeg`.

```bash
# Install playwright
pip install playwright
playwright install chromium

# Install FFmpeg (macOS)
brew install ffmpeg
```

## Usage

### 1. Simple Screenshot
Takes a standard 1280x800 screenshot and auto-generates a filename in `data/screenshots/`.
```bash
python3 .gemini/skills/photograph/scripts/take_screenshot.py "https://www.google.com"
```

### 2. Full Page Capture
Captures the entire scrollable area of the page.
```bash
python3 .gemini/skills/photograph/scripts/take_screenshot.py "https://mlcommons.org/croissant" --full_page
```

### 3. Screen Recording (New!)
Record the screen while running a process (e.g., the Wizard).
```bash
python3 .gemini/skills/photograph/scripts/record_screen.py --command "python3 .gemini/skills/wizard/scripts/wizard.py https://youtu.be/dQw4w9WgXcQ 'My Demo'" --output data/recordings/wizard_run.mp4
```

### 4. Duration-Based Recording
Record the screen for 5 seconds.
```bash
python3 .gemini/skills/photograph/scripts/record_screen.py --duration 5 --output data/recordings/quick_check.mp4
```

## Integration with Orchestrator

The Orchestrator Expert can transition to the Photograph skill when:
1.  A website is highly dynamic and cannot be scraped by simple HTML parsers.
2.  A visual record of the data source is required for provenance.
3.  The user wants to record a video log of an automated process for auditing or demonstration purposes.
