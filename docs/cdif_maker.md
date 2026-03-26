# 🏷️ CDIF Maker Skill

The **CDIF Maker** skill enables the Croissant Toolkit to interact with specialized CDIF (Cross-Domain Interoperability Framework) semantic services. It allows for the discovery and structured mapping of variables into standard formats.

## 🌟 Key Features

*   **Semantic Discovery**: Translates natural language queries (e.g., "sea surface temperature") into precise scientific variables.
*   **Variable Inventory**: Generates structured variable inventories including definitions, units, and dimensions (time, depth, location).
*   **Integration**: Seamlessly outputs JSON files that can be consumed by the `Croissant Expert` for metadata enrichment.
*   **Ollama Powered**: Uses a dedicated Ollama model hosted at CODATA for high-precision semantic mapping.

## 🛠️ Usage

To discover variables and generate an inventory:

```bash
python3 .gemini/skills/cdif-maker/scripts/cdif_maker.py "variable name or description"
```

### Example
```bash
python3 .gemini/skills/cdif-maker/scripts/cdif_maker.py "soil moisture at 10cm depth"
```

## ⚙️ Configuration

The skill connects to the CODATA CDIF service:
*   **Endpoint**: `https://cdif-4-xas.dev.codata.org/ollama`
*   **Default Model**: `gpt-oss:latest`

## 📂 Output
The results are saved as structured JSON files in the `./data/cdif/` directory, ready for integration into larger dataset metadata files.
