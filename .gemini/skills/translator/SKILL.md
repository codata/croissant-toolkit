---
name: translator
description: Recognize the language of input content or video scripts and translate them precisely into English using Gemini 3.
---

# Translator Skill

The Translator skill leverages the power of Gemini 3 to identify the source language of any text or document (including video transcripts) and provide a high-precision translation into English.

This skill is essential for the Croissant Toolkit to handle multi-lingual datasets and global video content, ensuring all metadata and context are understood in English.

## Tools

### 1. Detect and Translate
Detects the language of the provided text or file and translates the content into English. If a file path is provided, it saves the English version as a new file.

**Usage:**
```bash
# Translate raw text
python3 translator/scripts/translate.py "Hola, ¿cómo estás? me gustaría aprender sobre Croissant."

# Translate a local file (e.g., a non-English transcript)
python3 translator/scripts/translate.py data/transcripts/NON_ENGLISH_VIDEO_ID.txt
```

**Example:**
`python3 translator/scripts/translate.py Bonjour, c'est un plaisir de participer au Hackathon.`
