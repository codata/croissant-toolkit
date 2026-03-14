---
name: nlp_expert
description: Extract named entities (persons, organizations, dates, locations) from text and provide them in structured JSON-LD format.
---

# NLP Expert Skill

The NLP Expert skill uses Gemini 3 to perform advanced Named Entity Recognition (NER). It identifies key entities within dataset descriptions, transcripts, or web results and maps them to standard Schema.org types in JSON-LD.

This is critical for establishing provenance, identifying dataset creators, and mapping geographic and temporal coverage in the Croissant specification.

## Tools

### 1. Extract Named Entities
Analyzes text or a file and returns all detected entities as JSON-LD. Results are stored in `./data/nlp/`.

**Usage:**
```bash
# Process raw text
python3 nlp_expert/scripts/extract_entities.py "Sergei Bodrov was born in Moscow in 1971."

# Process a file (e.g., a transcript)
python3 nlp_expert/scripts/extract_entities.py data/transcripts/6cWcZ2G53gE.txt
```

**Example Output (JSON-LD):**
```jsonld
{
  "@context": "https://schema.org/",
  "@type": "ItemList",
  "itemListElement": [
    {
      "@type": "Person",
      "name": "Sergei Bodrov"
    },
    {
      "@type": "Place",
      "name": "Moscow"
    }
  ]
}
```
