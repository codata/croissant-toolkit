---
name: fact-checker
description: High-fidelity "WebFetch" contradictions detector. Analyzes full rendered HTML using Gemini and records a cinematic proof of findings.
---

# Fact Checker Skill (WebFetch)

This skill utilizes a "WebFetch" approach—opening a target URL in a full browser context, rendering all elements (including lazy-loaded content), and sending the complete HTML to Gemini for deep cognitive analysis.

## Features
- **WebFetch Architecture**: Opens target URLs in Playwright/Chromium to ensure all scripts and dynamic content are triggered before analysis.
- **HTML Context**: Analyzes the raw rendered structure instead of just flat text, leading to better claim identification.
- **Cinematic Verification**: Records the highlight and comment process in a high-fidelity video format.

## Usage
```bash
python3 .gemini/skills/fact-checker/scripts/fact_check_record.py "https://example.com" --auto
```
