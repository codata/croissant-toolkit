# 🎨 Creator Skill

The **Creator Skill** is responsible for generating visual and multi-media content to present and promote the results of the Croissant Toolkit.

## 🌟 Key Features
1. **Dynamic Slideshows**: Automatically generates high-quality visual presentations from toolkit data.
2. **Animated Intros**: Creates short (10-15s) animated sequences for demos and hackathon pitches.
3. **Markdown-to-Movie**: Transform structured `.md` slide decks (from `presentation_expert`) into high-quality MP4 movies with highlights and professional styling.
4. **High-Tech Aesthetic**: Uses AI-generated visuals to maintain a premium, futuristic look.

## 🛠️ Components
- `create_video.py`: The core script for stitching assets into a presentation.
- `markdown_to_video.py`: High-quality Markdown-to-MP4 converter.
- `assets/`: Directory containing high-fidelity slides and icons.

## 🚀 Usage
### Generating the toolkit intro:
```bash
python3 .gemini/skills/creator/scripts/create_video.py
```

### Converting a Markdown deck to Movie:
```bash
python3 .gemini/skills/creator/scripts/markdown_to_video.py path/to/slides.md --output final_movie.mp4
```

Results are saved in `.gemini/skills/creator/video_output/`.
