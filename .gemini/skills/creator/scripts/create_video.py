import os
import sys
from PIL import Image

def create_intro_presentation():
    """Stitches generated slides and cookbook screenshots into a 30-second presentation."""
    
    asset_dir = os.path.join(os.path.dirname(__file__), "assets")
    screenshot_dir = os.path.join(os.path.dirname(__file__), "../../../../cookbook/screenshots")
    output_dir = os.path.join(os.path.dirname(__file__), "../video_output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Sequence of images (Slides + Screenshots)
    image_paths = [
        os.path.join(asset_dir, "slide_1.png"),
        os.path.join(asset_dir, "hackathon.png"),
        os.path.join(screenshot_dir, "navigator.png"),
        os.path.join(screenshot_dir, "walker.png"),
        os.path.join(asset_dir, "slide_2.png"),
        os.path.join(screenshot_dir, "gemini_31_discovery.png"),
        os.path.join(screenshot_dir, "youtuber.png"),
        os.path.join(asset_dir, "slide_3.png"),
        os.path.join(screenshot_dir, "croissant.png"),
        os.path.join(asset_dir, "slide_4.png"),
        os.path.join(screenshot_dir, "neo4j.png"),
        os.path.join(screenshot_dir, "obsidian.png"),
        os.path.join(screenshot_dir, "email_report_mockup.png"),
        os.path.join(screenshot_dir, "telegram.png"),
        os.path.join(asset_dir, "slide_5.png")
    ]
    
    frames = []
    target_size = (1024, 768) # Standard 4:3 for slides/browsing
    
    print(f"[Creator] Processing {len(image_paths)} images for 30-second presentation...")
    
    for path in image_paths:
        if not os.path.exists(path):
            print(f"[Creator] Warning: Image missing at {path}")
            continue
            
        img = Image.open(path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Resize/Pad to maintain aspect ratio and consistency
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        new_img = Image.new("RGB", target_size, (0, 0, 0))
        # Center the image
        new_img.paste(img, ((target_size[0] - img.size[0]) // 2, (target_size[1] - img.size[1]) // 2))
            
        # 15 images * 20 frames (at 10fps) = 300 frames = 30 seconds
        for _ in range(20):
            frames.append(new_img.copy())
            
    if not frames:
        print("[Creator] No frames gathered. Aborting.")
        return

    output_path = os.path.join(output_dir, "croissant_toolkit_full_demo.gif")
    
    print(f"[Creator] Saving 30-second high-fidelity demo to: {output_path}")
    
    # Save as animated GIF (100ms per frame = 10fps)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
        optimize=False # Optimization can be slow for 300 frames
    )
    
    print(f"[Creator] 30-second Demo Ready! [RESULT_PATH]: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    create_intro_presentation()
