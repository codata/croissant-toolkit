# Croissant Expert

Specialized in the MLCommons Croissant metadata specification. Can generate, validate, and serialize dataset metadata into compliant JSON-LD.

**Core functionality:** Transforms a structured metadata JSON into the final Croissant format. Output files are designed to pass the official Croissant validator and are stored locally in `./data/croissant/` as JSON-LD files.

## Usage
```bash
python3 croissant_expert/scripts/serialize.py <INPUT_METADATA_JSON> [OUTPUT_JSON_LD]
```

## Metadata Schema
The input JSON should follow this structure:
- `name`: String
- `description`: String
- `url`: String
- `license`: String
- `distribution`: List of `FileObject` or `FileSet`
- `recordSet`: List of `RecordSet` with `fields` and `source` information.

## Capabilities
- **Spec Interpretation**: Access to the latest MLCommons Croissant standard.
- **JSON-LD Generation**: Deep understanding of `@context`, `@type`, and linked data principles.
- **Validation-Ready**: Output files are designed to pass the official Croissant validator.
