from youtube_transcript_api import YouTubeTranscriptApi
import sys

video_id = 'zOQI49l6hfo'
try:
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)
    print("Available transcripts:")
    for transcript in transcript_list:
        print(f" - {transcript.language} ({transcript.language_code}) [Manual: {transcript.is_generated == False}]")
except Exception as e:
    print(f"Error listing transcripts: {e}")
