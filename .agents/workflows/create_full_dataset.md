---
description: Create a comprehensive dataset using all possible inputs and skills
---

# Create Dataset with All Possible Inputs Workflow

This workflow utilizes the `Orchestrator Expert` to combine all available skills and create a rich, multi-dimensional dataset format.

## Prerequisites
- Working API keys for all tools in the toolkit (Serper, Deepgram, DeepL, etc.) stored in the `.env` file.
- Python 3.10+ and requirements installed.

## Steps to Execute

1. **Information Gathering (Navigator & YouTuber)**
   - Start by defining a root topic (e.g., "AI regulations 2026").
   - Use the `navigator` skill to fetch recent articles and search results on the topic.
   - Use the `youtuber` skill to discover relevant YouTube videos and download their audio.

2. **Data Processing (Transcriber & Translator)**
   - Wait for the audio files to finish downloading, then run the `transcriber` skill on the output audio to get raw text.
   - If any text or parsed articles are not in the target dataset language (e.g., English), use the `translator` skill to translate the content.

3. **Data Refinement (NLP Expert)**
   - Pass the gathered search texts and translated transcripts to the `nlp_expert` skill.
   - Instruct the `nlp_expert` to extract key entities, generate summaries, and clean the text.

4. **Creation of the Dataset Metadata (Croissant Expert)**
   - Consolidate all the processed files, source URLs, and descriptions into a final metadata JSON structure.
   - Use the `croissant_expert` skill to convert this metadata JSON into a fully validated MLCommons Croissant distribution.

5. **Validation (Tester)**
   - Run the `skills-testor` or validation scripts over the final `data/croissant/*.json` to ensure the outputs are correctly formatted.

## Running Automatically

You can issue the following prompt to the agent to kick off this workflow:
```
I want to run the 'create_full_dataset' workflow. Use the Orchestrator Expert to navigate the topic "Global Climate Tech Advances", extract videos, transcribe them, translate any non-English content, summarize them via NLP, and finally package it all via Croissant Expert.
```
