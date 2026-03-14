# NLP Expert

Extract named entities (persons, organizations, dates, locations) from text and provide them in structured JSON-LD format.

**Core functionality:** Uses Gemini 3 to perform advanced Named Entity Recognition (NER). It identifies key entities within dataset descriptions, transcripts, or web results and maps them to standard Schema.org types in JSON-LD. Results are stored in `./data/nlp/`.

## Usage

To use this skill, simply ask the AI agent:

Process raw text:
```text
Use the NLP Expert skill to extract entities from "Sergei Bodrov was born in Moscow in 1971."
```

Process a file (e.g., a transcript):
```text
Use the NLP Expert skill to extract entities from data/transcripts/6cWcZ2G53gE.txt
```

## Example Output (JSON-LD)
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
