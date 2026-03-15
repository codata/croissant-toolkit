import os
import sys
from PIL import Image

def create_intro_presentation():
    """Stitches images into a 30-second presentation: Hackathon start -> Skill by Skill."""
    
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
    
    print(f"[Creator] Orchestrating 30-second skill-by-skill presentation ({len(image_paths)} slides)...")
    
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

    output_path = os.path.join(output_dir, "croissant_toolkit_skill_by_skill.gif")
    
    print(f"[Creator] Saving high-fidelity skill-by-skill sequence to: {output_path}")
    
    # Save as animated GIF (10fps)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
        optimize=False
    )
    
    print(f"[Creator] Skill-by-Skill Presentation Ready! [RESULT_PATH]: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    create_intro_presentation()
