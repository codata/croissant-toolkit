import os
import subprocess
import shutil
from PIL import Image, ImageDraw, ImageFont

def render_text_to_image(text, output_path, size=(1024, 768), bg_color=(15, 15, 15), text_color=(240, 240, 240)):
    """Renders a single slide text to a PNG image."""
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        font_body = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
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
            
    # Draw Title
    draw.text((50, 50), title, font=font_title, fill=(0, 200, 255))
    
    # Draw Body
    y_text = 120
    for line in body_lines:
        draw.text((50, y_text), line, font=font_body, fill=text_color)
        y_text += 40
        
    img.save(output_path)

def generate_video_from_markdown(md_path, output_avi):
    """Parses MD, renders slides, and compiles AVI."""
    with open(md_path, 'r') as f:
        content = f.read()
        
    slides = content.split('---')
    temp_dir = "temp_slides_official"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    
    frame_count = 0
    fps = 10
    seconds_per_slide = 4
    
    print(f"[Presentation Expert] Rendering {len(slides)} slides...")
    
    for i, slide_text in enumerate(slides):
        if not slide_text.strip() or "marp: true" in slide_text or "theme: default" in slide_text:
            continue
            
        slide_img_path = os.path.join(temp_dir, f"slide_{i:03d}.png")
        render_text_to_image(slide_text, slide_img_path)
        
        # Create multiple frames for each slide
        for _ in range(fps * seconds_per_slide):
            frame_path = os.path.join(temp_dir, f"frame_{frame_count:04d}.png")
            shutil.copy(slide_img_path, frame_path)
            frame_count += 1
            
    # Compile with FFmpeg
    print(f"[Creator] Compiling AVI: {output_avi}")
    cmd = [
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", os.path.join(temp_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", output_avi
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    
    # Cleanup
    shutil.rmtree(temp_dir)
    print(f"[Creator] Finished! [RESULT_PATH]: {os.path.abspath(output_avi)}")

if __name__ == "__main__":
    md_file = ".gemini/skills/presentation_expert/output/slides/official_croissant_presentation.md"
    output_file = ".gemini/skills/creator/video_output/official_croissant_toolkit.avi"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    generate_video_from_markdown(md_file, output_file)
