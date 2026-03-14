---
name: orchestrator_expert
description: Orchestrator agent that has comprehensive knowledge and command over all available skills in this toolkit to create complex workflows.
---

# Orchestrator Expert Skill

This skill acts as an orchestrator that leverages the full suite of specialized agents/skills to complete broad user requests. It knows the input/output schemas of every skill and sequences them efficiently.

## Available Skills Knowledge

The Orchestrator Expert knows how to use the following skills seamlessly together:
1. **Croissant Expert (`croissant_expert`)**: Generates MLCommons Croissant metadata.
2. **Navigator (`navigator`)**: Performs web searches for information gathering.
3. **NLP Expert (`nlp_expert`)**: Handles text summarization, keyword extraction, and structural text adjustments.
4. **Tester (`tester`, `skills-testor`)**: Validates that other skills function correctly.
5. **Transcriber (`transcriber`)**: Converts audio files to text.
6. **Translator (`translator`)**: Translates text across multiple languages.
7. **YouTuber (`youtuber`)**: Extracts informative metadata and audio from YouTube videos.

## Usage

You can use the Orchestrator Expert to set up a pipeline. For example, to run the `create_full_dataset` workflow:
```
Use the Orchestrator Expert to execute the 'create_full_dataset' workflow. 
Navigate the topic '[YOUR TOPIC]', extract videos with 'youtuber', transcribe the audio, translate any non-English content, summarize using 'nlp_expert', and package the final result into Croissant metadata.
```
