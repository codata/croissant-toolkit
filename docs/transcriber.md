# Transcriber

Fetch and store transcripts from YouTube videos for deep content analysis.

**Core functionality:** Allows the agent to download the text transcript (closed captions) of YouTube videos. Transcripts are stored locally in `./data/transcripts/` as plain text files named by their YouTube Video ID.

## Usage

To use this skill, simply ask the AI agent:

Transcribe a specific video:
```text
Use the Transcriber skill to transcribe the video at <VIDEO_URL_OR_ID>.
```

Batch transcribe the results from the last Youtuber search:
```text
Use the Transcriber skill to batch transcribe the results from the last YouTube search.
```

## Example

```text
Use the Transcriber skill to transcribe the video at https://www.youtube.com/watch?v=6cWcZ2G53gE
```
