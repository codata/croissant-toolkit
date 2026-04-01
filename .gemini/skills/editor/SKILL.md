---
name: editor
description: A high-fidelity social media document generator. It transforms raw text or summaries into visually premium PDFs suitable for LinkedIn carousels and professional platform documents.
---

# Editor Skill

The Editor skill takes content (from the user, or summarized by the Visioner/Fact-Checker) and formats it into a high-end, boardroom-ready PDF. It is specifically designed to replicate the aesthetic of premium LinkedIn "PDF Carousels."

## Features
- **Social-Ready Aesthetics**: Clean typography, professional color palettes, and modern layout structures (similar to professional white papers).
- **Automated Formatting**: Transforms lists, tables of contents, and summaries into visually balanced slides.
- **Brand-Inspired Design**: Incorporates professional headers, dates, and navigation-inspired elements.

## Usage

### 1. Generating a LinkedIn-style Document from Text
```bash
python3 .gemini/skills/editor/scripts/create_social_document.py --title "AI Coding Habits" --items "['Develop Accountability', 'Document Context', 'Simple is Better']" --output "ai_coding_guide.pdf"
```

## Setup
Uses Playwright for high-fidelity rendering.
```bash
pip install playwright
playwright install chromium
```
