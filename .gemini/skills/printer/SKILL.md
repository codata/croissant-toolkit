---
name: printer
description: A high-fidelity web-to-PDF archival tool. Supports lazy loading, layout cleaning, and merging multiple pages into a single PDF document.
---

# Printer Skill

The Printer skill creates clean, professional archival PDF documents from one or more web pages. It is specifically designed to bypass "web noise" like ads and sticky headers while ensuring lazy-loaded content (like images and dynamic sections) is fully captured.

## Features
- **Clean Archival**: Automatically hides headers, footers, ads, and sticky navigation bars.
- **Lazy Loading**: Scrolls the entire page to trigger dynamic content loading before printing.
- **Multi-Page Merging**: Can combine multiple different URLs into a single unified PDF file.
- **Banner Dismissal**: Automatically clears common cookie consents and overlays.

## Usage

### 1. Print a Single Page
```bash
python3 .gemini/skills/printer/scripts/print_pages.py "https://example.com" --output "report.pdf"
```

### 2. Combine Multiple Pages into One PDF
```bash
python3 .gemini/skills/printer/scripts/print_pages.py "https://site-a.com" "https://site-b.com" --output "combined_archive.pdf"
```

## Setup
Requires Playwright and PyPDF2.
```bash
pip install playwright PyPDF2
playwright install chromium
```
