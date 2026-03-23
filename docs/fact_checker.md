# 🕵️ Fact Checker Skill

The `Fact Checker` skill provides high-fidelity, investigative AI analysis for documents, URLs, and video content. It is designed to identify sensitive information, analyze innovation potential, and provide visual evidence of its reasoning.

## 🚀 Key Features

*   **Sensitive Data Discovery**: Automatically identifies claims related to legal conflicts, contract terminations, and sensitive corporate data.
*   **Innovation Synthesis**: Extracts the "Innovation Impact" and "Cognitive Potential" of the document's core concepts.
*   **Visual Reasoning (VizHighlight)**: Automatically generates screen recordings (MP4) with visual highlighting of internal passages used as evidence.
*   **Evidence Mapping**: Links each finding to its source (URL or file path) and assigns an investigative probability score.
*   **Investigative Summary**: Synthesizes multiple findings into a coherent "Investigative Narrative".

## 🛠️ Typical Workflow

1.  **Ingestion**: Provide a source (URL or text).
2.  **Analysis**: Gemini 3 performs deep cognitive reasoning.
3.  **Visualization**: Automatically triggers the `Photograph` skill to record the screen while highlighting findings.
4.  **Reporting**: Saves a structured JSON report and the associated video evidence.

## 💻 Example Usage

```bash
# Analyze a confidential report and record the reasoning process
python3 .gemini/skills/fact-checker/scripts/fact_check_record.py "https://example.com/sensitive-report"
```

## 🎥 Visual Evidence (VizHighlight)

The tool doesn't just claim truth; it shows it. Every fact-check produces a visual artifact where the agent **literally** highlights the evidence on the screen while explaining its reasoning. 

## 🛡️ Attribution & DID
All findings are attributed to the agent's **DID** (`did:oyd:zQmcVHWDMeXtj273A9gNAnEG2EdrGEjtQiFuw9PncyVgs9z`), ensuring accountability and provenance in the Croissant ecosystem.
