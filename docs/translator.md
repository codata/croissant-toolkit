# Translator

Recognize the language of input content or video scripts and translate them precisely into English using Gemini 3.

**Core functionality:** Detects the language of the provided text or file and translates the content into English. If a file path is provided, it saves the English version as a new file.

## Usage

Translate raw text:
```bash
python3 translator/scripts/translate.py "Hola, ¿cómo estás? me gustaría aprender sobre Croissant."
```

Translate a local file (e.g., a non-English transcript):
```bash
python3 translator/scripts/translate.py data/transcripts/NON_ENGLISH_VIDEO_ID.txt
```

## Example
```bash
python3 translator/scripts/translate.py Bonjour, c'est un plaisir de participer au Hackathon.
```
