---
name: wizard
description: The ultimate data integrator. Orchestrates transcription, translation, NLP analysis, and Croissant serialization into a single automated pipeline.
---

# Wizard Skill

The Wizard skill is the high-level conductor of the Croissant Toolkit. It automates the entire journey from a raw data source (like a YouTube video or a foreign-language document) to a fully compliant and enriched Croissant JSON-LD file.

## Workflow
1.  **Acquisition**: Fetches content via `Transcriber` (for videos) or reads local files.
2.  **Harmonization**: Passes content through the `Translator` to ensure it's in English and refined.
3.  **Intelligence**: Uses the `NLP Expert` (via the Croissant Expert integration) to automatically detect creators, locations, and dates.
4.  **Finalization**: Generates the standardized `Croissant JSON-LD` file in `./data/croissant/`.

## Tools

### 1. The Automated Pipeline
Runs the full integration flow on any provided content or URL.

**Usage:**
```bash
# Process a YouTube video into a Croissant file
python3 wizard/scripts/wizard.py "https://www.youtube.com/watch?v=VIDEO_ID" "My Dataset Name"

# Process a local file
python3 wizard/scripts/wizard.py ./data/my_notes.txt "Notes Dataset"

# Process raw text
python3 wizard/scripts/wizard.py "Long description of my dataset..." "My Dataset"
```

## Capabilities
- **Multi-Skill Orchestration**: Zero-config coordination between Transcriber, Translator, NLP, and Croissant skills.
- **Smart Detection**: Automatically handles YouTube URLs vs. local files vs. raw strings.
- **Auto-Enrichment**: Always applies NLP analysis to maximize metadata quality.
