---
name: obsidian_expert
description: Convert Croissant datasets into structured Obsidian Markdown notes with frontmatter and semantic tags.
---

# 💎 Obsidian Expert Skill

The Obsidian Expert skill bridges the gap between structured machine learning metadata and personal knowledge management. It transforms Croissant JSON-LD files into beautiful, interlinked Markdown notes.

## Features
- **Semantic Mapping**: Automatically maps Croissant properties (creators, description, URL) to Obsidian frontmatter.
- **Tag Generation**: Converts keywords into searchable Obsidian tags (e.g., `#Volodymyr_Zelenskyy`).
- **Raw Integration**: Embeds the full JSON-LD source within the note for reference.
- **Vault Sync**: Supports automatic copying to your personal Obsidian vault via environment variables.

## Configuration
Set the path to your Obsidian vault to automatically sync notes:
```bash
export OBSIDIAN_VAULT_PATH="/Users/yourname/Documents/MyVault/CroissantNotes"
```

## Usage
### 1. Convert a Croissant file to a Note
```bash
python3 skills/obsidian_expert/scripts/to_obsidian.py "./data/croissant/my_dataset.jsonld"
```

### 2. Specify Output Directory
```bash
python3 skills/obsidian_expert/scripts/to_obsidian.py "./data/croissant/my_dataset.jsonld" "./my-vault"
```

## Note Structure
Each note follows a professional layout:
- **Frontmatter**: YAML metadata for Dataview compatibility.
- **Description**: The primary dataset summary.
- **Keywords**: Semantic tags for graph view organization.
- **Resources**: Clickable links to source and distribution files.
- **Raw Metadata**: The full technical JSON-LD source.
