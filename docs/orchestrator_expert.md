# Orchestrator Expert

The Orchestrator Expert is the master agent that has comprehensive knowledge and command over all available skills in this toolkit. It understands how to pipe data between different skills to achieve complex, multi-step goals.

**Core functionality:** Acts as an orchestrator that leverages the full suite of specialized agents/skills to complete broad user requests. It knows the input/output schemas of every skill and sequences them efficiently.

## Available Skills Knowledge

The Orchestrator Expert knows how to use the following skills:
- **Communication Officer (`communication_officer`)**: Sends results via email.
- **Croissant Expert (`croissant_expert`)**: Generates MLCommons Croissant metadata.
- **Data Expert (`data-expert`)**: Extracts claims and identifies technical metadata patterns.
- **Fact Checker (`fact-checker`)**: Performs deep investigative analysis with visual evidence.
- **Navigator (`navigator`)**: Performs web searches for information gathering.
- **NLP Expert (`nlp_expert`)**: Handles text summarization, keyword extraction, and entities detection.
- **ODRL Expert (`odrl-expert`)**: Manages decentralized IDs (DIDs) and usage policies.
- **Photograph (`photograph`)**: Captures visual snapshots of web pages and records screen sessions.
- **Presentation Expert (`presentation_expert`)**: Generates technical pitch decks from data.
- **RO-Crate Expert (`ro-crate-expert`)**: Packages research data into RO-Crate objects.
- **Telegram Expert (`telegram_expert`)**: Sends notifications and files to Telegram.
- **Tester (`tester`, `skills-testor`)**: Validates that other skills function correctly.
- **Transcriber (`transcriber`)**: Converts video audio to text.
- **Translator (`translator`)**: Translates text across multiple languages.
- **YouTuber (`youtuber`)**: Extracts informative metadata and transcripts from YouTube videos.
- **CDIF Maker (`cdif-maker`)**: Produces structured variable inventories for cross-domain interoperability.
- **Creator (`creator`)**: Renders cinematic MP4/AVI videos from toolkit assets.
- **Architect (`architect`)**: Translates complex technical requirements into visually intuitive architectural diagrams (Mermaid.js).
- **TRIZ Expert (`triz`)**: Inventive problem-solving framework based on 40 Principles and contradiction resolution (ODRL Protected - Requires Vault access).
- **UNF Skill (`unf`)**: Computes format-agnostic Universal Numeric Fingerprints (UNF v6) for data strings or files for precise versioning and integrity.

## Usage

To use this skill, simply ask the AI agent:
```text
Use the Orchestrator Expert skill to coordinate multiple skills and build an end-to-end pipeline to [YOUR COMPLEX GOAL].
```
