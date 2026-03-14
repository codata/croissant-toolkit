from youtube_transcript_api import YouTubeTranscriptApi
import sys

video_id = 'zOQI49l6hfo'
try:
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)
    transcript = transcript_list.find_generated_transcript(['en']).fetch()
    print(f"Total lines: {len(transcript)}")
    for entry in transcript:
        # Check if entry is a dictionary or object
        if hasattr(entry, 'text'):
            print(f" - {entry.start}: {entry.text}")
        else:
            print(f" - {entry['start']}: {entry['text']}")
except Exception as e:
    print(f"Error fetching transcript: {e}")
