# 📊 Presentation Expert Skill

The **Presentation Expert** is responsible for transforming complex research data, metadata, and insights into high-impact presentation decks.

## 🌟 Key Features
1.  **Semantic Storytelling**: Uses Gemini 3 to draft a narrative flow (Problem -> Solution -> Data -> Impact).
2.  **Slide Generation**: Produces Markdown-based slides (Marp/Reveal.js compatible).
3.  **Visual Layout Design**: Drafts prompts for the `creator` skill or image generation tools to create supporting visuals.
4.  **Data Integration**: Directly pulls from `croissant_expert` outputs to feature technical specifications in slides.

## 🛠️ Components
- `generate_slides.py`: The core orchestrator that takes a topic or JSON-LD and produces the deck content.
- `output/slides/`: Local storage for generated presentation files.

## 🚀 Usage
To generate a pitch deck for a specific dataset:
```bash
python3 .gemini/skills/presentation_expert/scripts/generate_slides.py "Dataset Title"
```
