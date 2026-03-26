# 🎨 Creator Skill

The **Creator Skill** is responsible for generating visual and multi-media content to present and promote the results of the Croissant Toolkit. It turns raw data and markdown notes into cinematic experiences.

## 🌟 Key Features

*   **Cinematic Video Creation**: Synthesizes MP4 movies from toolkit metadata and assets using FFmpeg.
*   **Markdown-to-Movie**: Transform structured `.md` slide decks (from `Presentation Expert`) into high-quality movies with highlights and professional styling.
*   **Dynamic Slideshows**: Automatically generates visual presentations from toolkit data.
*   **Animated sequences**: Creates short (10-15s) animated sequences for demos and hackathon pitches.
*   **High-Tech Aesthetic**: Uses AI-generated visuals to maintain a premium, futuristic look.

## 🛠️ Components

- `create_video.py`: The core script for stitching assets into a presentation.
- `markdown_to_video.py`: High-quality Markdown-to-MP4 converter centered around Marp style.
- `generate_official_video.py`: Renders the official toolkit workforce video.

## 🚀 Usage

### Generating the toolkit intro:
```bash
python3 .gemini/skills/creator/scripts/create_video.py
```

### Converting a Markdown deck to Movie:
```bash
python3 .gemini/skills/creator/scripts/markdown_to_video.py path/to/slides.md --output final_movie.mp4
```

## 🎥 Results
Video outputs are saved in `.gemini/skills/creator/video_output/`.
The generator supports both **AVI** (lossless) and **MP4** (web-ready) formats.
