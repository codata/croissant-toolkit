# 📊 Claims Detection (Data Expert) Skill

The `Claims Detection` skill (formerly Data Expert) is designed to transform unstructured text, PDFs, and web pages into high-fidelity factual datasets. It focuses on isolating verifiable measurements and qualitative claims with full semantic context.

## 🚀 Key Features

*   **Multimodal Semantic Parsing**: Direct support for URLs (via Playwright), local PDFs (via PyPDF2), and raw text.
*   **Original Claim Preservation**: Captures both the full `context` sentence and the specific `original_claim` quote for granular verification.
*   **Verifiable Identification**: Automatically generates a unique, reproducible **MD5 hash** for each claim.
*   **Investigative Probability**: Assigns a truth probability score based on internal consistency and AI-driven reasoning.
*   **Croissant Alignment**: Maps claims to `schema:variableMeasured` for seamless integration into Croissant metadata files.

## 🛠️ Typical Workflow

1.  **Ingestion**: Provide a source (URL, PDF path, or text).
2.  **Extraction**: Gemini 3 parses the content for factual statements.
3.  **Synthesis**: Generates a high-level narrative `claim` summarizing the entire dataset.
4.  **Export**: Saves the results to `data/claims.json` with full DID-based provenance.

## 💻 Example Usage

```bash
# Analyze a microclimate report and save structured claims
python3 .gemini/skills/data-expert/scripts/data_expert.py "microclimate_report.pdf"
```

```bash
# Pipe results to other tools in JSON format
python3 .gemini/skills/data-expert/scripts/data_expert.py "https://example.com" --json
```

## 📄 Output Schema (data/claims.json)

| Field | Description |
| :--- | :--- |
| **claim** | Narrative synthesis of the entire analysis. |
| **id** | MD5 hash of the claim context for tracking. |
| **context** | The full source sentence containing the claim. |
| **variableMeasured**| The Schema.org name for the measured variable. |
| **value** | The extracted quantitative or qualitative value. |
| **probability** | Factual reliability score (0.0 to 1.0). |
| **prov:wasAttributedTo**| The DID of the investigating agent. |
