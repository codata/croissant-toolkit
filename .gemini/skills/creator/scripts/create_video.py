import os
import sys
from PIL import Image

def create_intro_presentation():
    """Stitches images into a GIF presentation: Hackathon start -> Skill by Skill."""
    
    asset_dir = os.path.join(os.path.dirname(__file__), "assets")
    screenshot_dir = os.path.join(os.path.dirname(__file__), "../../../../cookbook/screenshots")
    output_dir = os.path.join(os.path.dirname(__file__), "../video_output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Precise Sequence: Hackathon -> Title -> Section Head -> Illustrations
    image_paths = [
        os.path.join(asset_dir, "hackathon.png"),      # 1. The Start (Paris 2026)
        os.path.join(asset_dir, "slide_1.png"),       # 2. Main Title
        
        os.path.join(asset_dir, "slide_2.png"),       # 3. HEADER: Discovery Skills
        os.path.join(screenshot_dir, "navigator.png"), # 4. Nav Illustration
        os.path.join(screenshot_dir, "walker.png"),    # 5. Walker Illustration
        os.path.join(screenshot_dir, "gemini_31_discovery.png"), # 6. Discovery Flow
        os.path.join(screenshot_dir, "youtuber.png"),  # 7. YouTuber Illustration
        
        os.path.join(asset_dir, "slide_3.png"),       # 8. HEADER: Analysis & NLP
        os.path.join(screenshot_dir, "croissant.png"), # 9. Standardized Metadata
        
        os.path.join(asset_dir, "slide_4.png"),       # 10. HEADER: Knowledge & Reporting
        os.path.join(screenshot_dir, "neo4j.png"),     # 11. Graph Discovery
        os.path.join(screenshot_dir, "obsidian.png"),  # 12. Persistent Notes
        os.path.join(screenshot_dir, "email_report_mockup.png"), # 13. Professional Alerting
        os.path.join(screenshot_dir, "telegram.png"),  # 14. Mobile Notifications
        
        os.path.join(asset_dir, "slide_5.png")        # 15. The Vision (Conclusion)
    ]
    
    frames = []
    target_size = (1024, 768)
    
    print(f"[Creator] Orchestrating GIF skill-by-skill presentation ({len(image_paths)} slides)...")
    
    for path in image_paths:
        if not os.path.exists(path):
            print(f"[Creator] Warning: Missing illustration at {path}")
            continue
            
        img = Image.open(path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Standardize aspect ratio
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        new_img = Image.new("RGB", target_size, (0, 0, 0))
        new_img.paste(img, ((target_size[0] - img.size[0]) // 2, (target_size[1] - img.size[1]) // 2))
            
        # 10fps * 2s = 20 frames per image
        for _ in range(20):
            frames.append(new_img.copy())
            
    if not frames:
        print("[Creator] Error: No frames gathered.")
        return

    output_path_gif = os.path.join(output_dir, "croissant_toolkit_presentation.gif")
    output_path_avi = os.path.join(output_dir, "croissant_toolkit_presentation.avi")
    
    print(f"[Creator] Saving high-fidelity skill-by-skill GIF to: {output_path_gif}")
    
    # Save as animated GIF (10fps)
    frames[0].save(
        output_path_gif,
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
        optimize=False
    )
    
    # Try to generate AVI using FFmpeg
    ffmpeg_bin = "/opt/homebrew/bin/ffmpeg"
    if os.path.exists(ffmpeg_bin):
        print(f"[Creator] Generating AVI video using FFmpeg: {output_path_avi}")
        import subprocess
        import tempfile
        import shutil
        
        temp_dir = tempfile.mkdtemp()
        try:
            # Save frames as temporary PNGs
            for i, frame in enumerate(frames):
                frame.save(os.path.join(temp_dir, f"frame_{i:04d}.png"))
            
            # Use ffmpeg to stitch PNGs into AVI
            # -y: overwrite, -framerate 10: speed, -i: input pattern, -c:v mpeg4: codec
            cmd = [
                ffmpeg_bin, "-y", "-framerate", "10",
                "-i", os.path.join(temp_dir, "frame_%04d.png"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                output_path_avi
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"[Creator] AVI Video Ready! [RESULT_PATH]: {os.path.abspath(output_path_avi)}")
        except Exception as e:
            print(f"[Creator] Error generating AVI: {e}")
        finally:
            shutil.rmtree(temp_dir)
    else:
        print("[Creator] FFmpeg not found at expected path. Skipping AVI generation.")
    
    print(f"[Creator] Finished! GIF available at: {os.path.abspath(output_path_gif)}")

if __name__ == "__main__":
    create_intro_presentation()
