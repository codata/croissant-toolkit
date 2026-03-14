# Transcriber

Fetch and store transcripts from YouTube videos for deep content analysis.

**Core functionality:** Allows the agent to download the text transcript (closed captions) of YouTube videos. Transcripts are stored locally in `./data/transcripts/` as plain text files named by their YouTube Video ID.

## Usage

Transcribe a specific video:
```bash
python3 transcriber/scripts/transcribe.py <VIDEO_URL_OR_ID>
```

Batch transcribe the results from the last Youtuber search:
```bash
python3 transcriber/scripts/transcribe.py
```

## Example
```bash
python3 transcriber/scripts/transcribe.py https://www.youtube.com/watch?v=6cWcZ2G53gE
```
