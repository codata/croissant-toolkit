import os
import subprocess
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def create_gradient(size, color1, color2):
    """Creates a vertical gradient image."""
    base = Image.new('RGB', size, color1)
    top = Image.new('RGB', size, color2)
    mask = Image.new('L', size)
    mask_data = []
    for y in range(size[1]):
        mask_data.extend([int(255 * (y / size[1]))] * size[0])
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def render_text_to_image(text, output_path, size=(1024, 768)):
    """Renders a slide with a nice gradient background and icons."""
    # Tech-aesthetic gradient (Dark Blue to Deep Purple)
    color1 = (10, 20, 40)
    color2 = (40, 10, 60)
    img = create_gradient(size, color1, color2)
    draw = ImageDraw.Draw(img)
    
    # Try to load a font
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 50)
        font_body = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 25)
    except:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()

    lines = text.strip().split('\n')
    title = ""
    body_lines = []
    
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
        elif line.strip():
            body_lines.append(line.strip())
            
    # Draw Title with a slight glow/shadow
    draw.text((52, 52), title, font=font_title, fill=(0, 50, 100))
    draw.text((50, 50), title, font=font_title, fill=(0, 255, 255)) # Cyan title
    
    # Draw a separator line
    draw.line((50, 110, 974, 110), fill=(0, 255, 255), width=2)
    
    # Draw Body
    y_text = 150
    for line in body_lines:
        # Highlight bullet points
        if line.startswith('- '):
            draw.text((50, y_text), "•", font=font_body, fill=(0, 255, 255))
            draw.text((80, y_text), line[2:], font=font_body, fill=(240, 240, 240))
        else:
            draw.text((50, y_text), line, font=font_body, fill=(200, 200, 200))
        y_text += 45
        
    # Add a "Powered by" watermark
    draw.text((800, 730), "Powered by Gemini 3", font=font_body, fill=(100, 100, 150))
    
    img.save(output_path)

def generate_video_from_markdown(md_path, output_avi):
    """Parses MD, renders aesthetic slides, and compiles AVI."""
    with open(md_path, 'r') as f:
        content = f.read()
        
    slides = content.split('---')
    temp_dir = "temp_slides_aesthetic"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    
    frame_count = 0
    fps = 10
    seconds_per_slide = 4
    
    print(f"[Presentation Expert] Rendering {len(slides)} aesthetic slides...")
    
    for i, slide_text in enumerate(slides):
        if not slide_text.strip() or "marp: true" in slide_text or "theme: default" in slide_text:
            continue
            
        slide_img_path = os.path.join(temp_dir, f"slide_{i:03d}.png")
        render_text_to_image(slide_text, slide_img_path)
        
        for _ in range(fps * seconds_per_slide):
            frame_path = os.path.join(temp_dir, f"frame_{frame_count:04d}.png")
            shutil.copy(slide_img_path, frame_path)
            frame_count += 1
            
    # Compile with FFmpeg
    print(f"[Creator] Compiling Aesthetic AVI: {output_avi}")
    cmd = [
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", os.path.join(temp_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", output_avi
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    
    shutil.rmtree(temp_dir)
    print(f"[Creator] Aesthetic Movie Ready! [RESULT_PATH]: {os.path.abspath(output_avi)}")

if __name__ == "__main__":
    md_file = ".gemini/skills/presentation_expert/output/slides/official_croissant_presentation.md"
    output_file = ".gemini/skills/creator/video_output/croissant_toolkit_aesthetic.avi"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    generate_video_from_markdown(md_file, output_file)
