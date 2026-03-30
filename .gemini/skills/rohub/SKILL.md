---
name: rohub
description: Deposit research objects and add semantic annotations to the RO-Hub portal using the rohub library.
---

# ROHub Skill

The **ROHub** skill enables the Croissant Toolkit to deposit research data and metadata into the **RO-Hub** portal (https://rohub.org). It handles the creation of Research Objects (ROs) and the addition of semantic triples for rich provenance and discoverability.

## 🌟 Key Features

1.  **RO Creation**: Programmatically create new Research Objects with titles, descriptions, and research areas.
2.  **RO Loading**: Access and update existing Research Objects using their persistent identifiers (DOIs/UUIDs).
3.  **Semantic Annotations**: Add structured triples (Subject-Predicate-Object) to research objects to describe variables, spatial coverage, and temporal coverage.
4.  **Integration**: Harmonizes with the `RO-Crate Expert` and `Croissant Expert` to translate machine-readable metadata into RO-Hub semantic structures.
5.  **Authentication**: Securely logs in to the RO-Hub API using environment variables.

## 🛠️ Configuration

The following environment variables are required for authentication:
- `ROHUB_USER`: Your RO-Hub username (e.g., your email).
- `ROHUB_PASSWORD`: Your RO-Hub password.

## 🚀 Usage

### Deposit a new Research Object
```bash
python3 .gemini/skills/rohub/scripts/deposit.py --title "Arctic Radioisotopes" --description "Sea surface observations" --areas "Radiobiology"
```

### Add annotations from a JSON-LD file (e.g., Croissant)
```bash
python3 .gemini/skills/rohub/scripts/deposit.py --id "ea792c69-9037-4d06-84a8-6fded7356e12" --metadata path/to/croissant.jsonld
```

### Add annotations from a local metadata file
```bash
python3 .gemini/skills/rohub/scripts/deposit.py --id "85d38a45-d0cc-4269-9ca6-44d71b0c6ef7" --metadata path/to/metadata.jsonld
```

## ⚙️ Service Details
- **API Endpoint**: https://api.rohub.org/
- **Library**: `rohub` (python package)
