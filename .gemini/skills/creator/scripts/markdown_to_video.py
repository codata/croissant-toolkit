import os
import sys
import argparse
import subprocess
import tempfile
import shutil
import re
from PIL import Image, ImageDraw, ImageFont

def parse_markdown_slides(md_path):
    """Parses a Markdown file into individual slides based on '---' separators."""
    if not os.path.exists(md_path):
        print(f"[Creator] Error: Markdown file not found at {md_path}")
        return []
        
    with open(md_path, 'r') as f:
        content = f.read()
        
    # Split by horizontal rules
    raw_slides = re.split(r'\n---+\n', content)
    slides = []
    
    for raw in raw_slides:
        clean = raw.strip()
        if clean and not clean.startswith('marp:'):
            slides.append(clean)
            
    return slides

def render_slide_to_image(text, output_path, size=(1280, 720)):
    """Renders Markdown text to a premium-looking slide image using AI-generated backgrounds."""
    
    asset_dir = os.path.join(os.path.dirname(__file__), "assets")
    
    # Intelligently select background based on content
    bg_map = {
        "Discovery": "bg_discovery.png",
        "Solution": "bg_discovery.png",
        "Problem": "bg_discovery.png",
        "Intelligence": "bg_intelligence.png",
        "NLP": "bg_intelligence.png",
        "Technical": "bg_intelligence.png",
        "Impact": "bg_persistence.png",
        "Future": "bg_persistence.png",
        "Knowledge": "bg_persistence.png"
    }
    
    bg_file = "bg_intro.png" # Default
    for key, val in bg_map.items():
        if key.lower() in text.lower():
            bg_file = val
            break
            
    bg_path = os.path.join(asset_dir, bg_file)
    
    if os.path.exists(bg_path):
        img = Image.open(bg_path).resize(size)
    else:
        img = Image.new('RGB', size, (15, 15, 15))
        
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Create Glassmorphism Overlay (Semi-transparent card)
    card_margin = 60
    draw.rectangle(
        [card_margin, card_margin, size[0] - card_margin, size[1] - card_margin],
        fill=(0, 0, 0, 160), # Dark translucent
        outline=(255, 255, 255, 40), # Subtle white border
        width=2
    )
    
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 60)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 40)
        body_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 32)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    lines = text.split('\n')
    y_offset = 120
    
    for line in lines:
        line = line.strip()
        if not line:
            y_offset += 25
            continue
            
        if line.startswith('# '):
            draw.text((100, y_offset), line[2:], font=title_font, fill=(255, 255, 255))
            y_offset += 90
        elif line.startswith('## '):
            draw.text((100, y_offset), line[3:], font=subtitle_font, fill=(66, 133, 244)) # Google Blue
            y_offset += 70
        else:
            # Bullet point or content
            text_color = (220, 220, 220, 255)
            draw.text((120, y_offset), line, font=body_font, fill=text_color)
            y_offset += 55
            
        if y_offset > size[1] - 120:
            break

    # Add a glowing 🥐 brand mark
    draw.text((size[0]-140, size[1]-130), "🥐", font=title_font, fill=(251, 188, 5))
    
    img.save(output_path)

def create_movie_from_md(md_path, output_name="presentation_movie.mp4"):
    """Orchestrates the conversion of MD slides to a high-quality video."""
    
    output_dir = os.path.join(os.path.dirname(__file__), "../video_output")
    os.makedirs(output_dir, exist_ok=True)
    final_output = os.path.join(output_dir, output_name)
    
    slides_text = parse_markdown_slides(md_path)
    if not slides_text:
        print("[Creator] No valid slides found in Markdown.")
        return

    temp_dir = tempfile.mkdtemp()
    print(f"[Creator] Rendering {len(slides_text)} slides to high-quality images...")
    
    try:
        slide_images = []
        for i, text in enumerate(slides_text):
            img_path = os.path.join(temp_dir, f"slide_{i:03d}.png")
            render_slide_to_image(text, img_path)
            slide_images.append(img_path)
            
        # Use FFmpeg to create video
        # We hold each slide for 5 seconds
        ffmpeg_bin = "/opt/homebrew/bin/ffmpeg"
        if not os.path.exists(ffmpeg_bin):
            print("[Creator] Error: FFmpeg not found. Cannot generate video.")
            return

        # Create a concat file for ffmpeg to handle variable durations if needed
        # but here we just use -framerate with duplicated inputs for simplicity
        # or -reloop if we want to be fancy.
        # Simplest: framerate 1/5 (1 frame every 5 seconds)
        
        cmd = [
            ffmpeg_bin, "-y",
            "-framerate", "1/5", # 5 seconds per slide
            "-i", os.path.join(temp_dir, "slide_%03d.png"),
            "-c:v", "libx264",
            "-r", "30", # Output 30fps video
            "-pix_fmt", "yuv420p",
            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", # Ensure even dimensions for h264
            final_output
        ]
        
        print(f"[Creator] Stitching video: {final_output}")
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"[Creator] High-Quality Movie Ready! [RESULT_PATH]: {os.path.abspath(final_output)}")
        
    except Exception as e:
        print(f"[Creator] Error: {e}")
    finally:
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert MD slides to a high-quality movie.")
    parser.add_argument("md_path", help="Path to the Markdown slides file")
    parser.add_argument("--output", default="presentation_movie.mp4", help="Output filename")
    args = parser.parse_args()
    
    create_movie_from_md(args.md_path, args.output)
