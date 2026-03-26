# 📊 Presentation Expert Skill

The **Presentation Expert** is responsible for transforming complex research data, metadata, and insights into high-impact presentation decks. It bridges technical data and storytelling.

## 🌟 Key Features

*   **Semantic Storytelling**: Uses Gemini 3 to draft a narrative flow (Problem -> Solution -> Data -> Impact).
*   **Slide Generation**: Produces Markdown-based slides (Marp/Reveal.js compatible).
*   **Visual Layout Design**: Drafts prompts for the `Creator` skill to create supporting visuals.
*   **Data Integration**: Directly pulls from `Croissant Expert` outputs to include technical specifications.
*   **Strategic Narrative**: Analyzes dataset descriptions to find the strongest "hook" for scientific and research audiences.

## 🛠️ Components

- `generate_slides.py`: Orchestrates the slide creation process.
- `output/slides/`: Local storage for generated presentation files.

## 🚀 Usage

To generate a pitch deck for a specific dataset or search result:

```bash
python3 .gemini/skills/presentation_expert/scripts/generate_slides.py "Dataset Title or Topic"
```

The resulting Markdown file will be saved in `.gemini/skills/presentation_expert/output/slides/`. After generation, use the `Creator` skill to convert these slides into a video:

```bash
python3 .gemini/skills/creator/scripts/markdown_to_video.py .gemini/skills/presentation_expert/output/slides/your_deck.md
```
