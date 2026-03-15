# Orchestrator Expert

The Orchestrator Expert is the master agent that has comprehensive knowledge and command over all available skills in this toolkit. It understands how to pipe data between different skills to achieve complex, multi-step goals.

**Core functionality:** Acts as an orchestrator that leverages the full suite of specialized agents/skills to complete broad user requests. It knows the input/output schemas of every skill and sequences them efficiently.

## Available Skills Knowledge

The Orchestrator Expert knows how to use the following skills:
- **Communication Officer (`communication_officer`)**: Sends results via email.
- **Croissant Expert (`croissant_expert`)**: Generates MLCommons Croissant metadata.
- **Navigator (`navigator`)**: Performs web searches for information gathering.
- **NLP Expert (`nlp_expert`)**: Handles text summarization, keyword extraction, and entities detection.
- **Telegram Expert (`telegram_expert`)**: Sends notifications and files to Telegram.
- **Tester (`tester`, `skills-testor`)**: Validates that other skills function correctly.
- **Transcriber (`transcriber`)**: Converts video audio to text.
- **Translator (`translator`)**: Translates text across multiple languages.
- **YouTuber (`youtuber`)**: Extracts informative metadata and transcripts from YouTube videos.

## Usage

To use this skill, simply ask the AI agent:
```text
Use the Orchestrator Expert skill to coordinate multiple skills and build an end-to-end pipeline to [YOUR COMPLEX GOAL].
```
