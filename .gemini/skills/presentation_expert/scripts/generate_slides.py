import os
import sys
import argparse
import json

def generate_slide_deck(topic, output_file=None):
    """Generates a structured slide deck in Markdown format."""
    
    print(f"[Presentation Expert] Drafting presentation for: {topic}")
    
    # In a real scenario, this would call Gemini 3 to brainstorm the content
    # For the toolkit, we use a high-fidelity template based on our patterns
    
    slides = [
        {
            "title": topic,
            "subtitle": "Powered by Croissant Toolkit & Gemini 3",
            "content": ["Unlocking the Potential of Autonomous Research", "Paris 2026 Hackathon Presentation"]
        },
        {
            "title": "The Problem",
            "subtitle": "Data fragmentation and manual labor",
            "content": [
                "- Web is messy and full of walls (ads/consent)",
                "- Manual metadata entry is error-prone",
                "- High-quality training data is hard to discover"
            ]
        },
        {
            "title": "The Solution: Agentic Research",
            "subtitle": "Multi-skill autonomous pipelines",
            "content": [
                "- **Autonomous Discovery**: YouTuber & Navigator",
                "- **Deep Extraction**: Walker & Transcriber",
                "- **Standardization**: Croissant Expert"
            ]
        },
        {
            "title": "Technical Innovation",
            "subtitle": "MLCommons Croissant Integration",
            "content": [
                "- Seamless JSON-LD metadata generation",
                "- Relational Discovery via Neo4j Knowledge Graphs",
                "- Persistent Intelligence with Obsidian"
            ]
        },
        {
            "title": "Impact & Future",
            "subtitle": "Scaling Open Data",
            "content": [
                "- 10x faster dataset preparation",
                "- Truly global and multi-lingual discovery",
                "- Bridging raw web content to ML training"
            ]
        }
    ]
    
    markdown_content = "---\nmarp: true\ntheme: default\nclass: invert\n---\n\n"
    
    for slide in slides:
        markdown_content += f"# {slide['title']}\n"
        if slide['subtitle']:
            markdown_content += f"## {slide['subtitle']}\n\n"
        
        for bullet in slide['content']:
            markdown_content += f"{bullet}\n"
        
        markdown_content += "\n---\n\n"
        
    if not output_file:
        safe_name = topic.lower().replace(" ", "_")
        output_file = f".gemini/skills/presentation_expert/output/slides/{safe_name}_presentation.md"
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w") as f:
        f.write(markdown_content)
        
    print(f"[Presentation Expert] Presentation deck saved to: {output_file}")
    print(f"[RESULT_PATH]: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a presentation deck.")
    parser.add_argument("topic", help="The topic or dataset title for the presentation")
    parser.add_argument("--output", help="Optional custom output path")
    args = parser.parse_args()
    
    generate_slide_deck(args.topic, args.output)
