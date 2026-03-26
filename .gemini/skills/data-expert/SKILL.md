---
name: data-expert
description: Extracts quantitative and qualitative measurements from PDFs, URLs, or text and assigns a truth probability score.
---

# Claims Detection (Data Expert) Skill

The Data Expert skill identifies factual claims within any document, evaluates their empirical reliability using Gemini, and exports structured semantic data for fact-checking pipelines.

## Features
- **Multimodal Input**: Supports direct text, local PDFs, or live URLs.
- **Claims Detection**: Extracts both the full context sentence and the specific `original_claim` segment.
- **Semantic Mapping**: Automatically maps claims to `schema:variableMeasured` for Croissant alignment.
- **MD5 Hashing**: Assigns unique, reproducible identifiers to every detected claim.
- **JSON Standard**: Produces a standardized `data/claims.json` report with DID-based provenance.

## Usage
```bash
python3 .gemini/skills/data-expert/scripts/data_expert.py "https://example.com"
```
```bash
# Pure JSON output for piping
python3 .gemini/skills/data-expert/scripts/data_expert.py "document.txt" --json
```
