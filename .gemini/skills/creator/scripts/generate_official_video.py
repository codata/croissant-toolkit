import os
import subprocess
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

def get_font(size, bold=False):
    """Modern corporate/tech font."""
    paths = ["/System/Library/Fonts/Avenir Next.ttc", "/System/Library/Fonts/Helvetica.ttc"]
    for path in paths:
        if os.path.exists(path):
            index = 1 if bold else 0
            try: return ImageFont.truetype(path, size, index=index)
            except: return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def draw_worker_avatar(draw, x, y, size, color):
    """Draws a stylized 'Digital Human' avatar icon."""
    draw.ellipse((x + size*0.3, y, x + size*0.7, y + size*0.4), fill=color)
    draw.chord((x + size*0.1, y + size*0.4, x + size*0.9, y + size*1.2), 180, 0, fill=color)

def render_intro_slide(output_path, size=(1920, 1080)):
    """Renders the cinematic title slide at 1080p."""
    asset_dir = ".gemini/skills/creator/scripts/assets"
    hackathon_bg = os.path.join(asset_dir, "hackathon.png")
    img = Image.open(hackathon_bg).convert('RGB').resize(size, Image.Resampling.LANCZOS) if os.path.exists(hackathon_bg) else Image.new('RGB', size, color=(10, 15, 30))
    overlay = Image.new('RGBA', size, (0, 10, 30, 180)); img.paste(Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB'))
    draw = ImageDraw.Draw(img)
    f_huge, f_mid, f_sub = get_font(120, bold=True), get_font(60, bold=True), get_font(35)
    draw.text((100, 250), "CROISSANT TOOLKIT", font=f_huge, fill=(255, 255, 255))
    draw.text((100, 400), "POWERED BY PALE FIRE FRAMEWORK", font=f_mid, fill=(0, 255, 255))
    draw.line((100, 500, 1400, 500), fill=(0, 255, 255), width=15)
    draw.text((100, 550), "INTRODUCING THE AUTONOMOUS DIGITAL WORKFORCE.", font=f_mid, fill=(255, 255, 255))
    draw.text((100, 950), "PARIS // MARCH 2026 // POWERED BY GEMINI 3.1 PRO", font=f_sub, fill=(150, 160, 180))
    img.save(output_path)

def render_outro_slide(output_path, size=(1920, 1080)):
    """Renders the final call-to-action slide with GitHub link and Cast."""
    img = Image.new('RGB', size, color=(10, 12, 15))
    draw = ImageDraw.Draw(img)
    f_huge, f_mid, f_sub = get_font(100, bold=True), get_font(50, bold=True), get_font(40)
    f_cast_title = get_font(30, bold=True)
    f_cast_names = get_font(28)
    
    # Text Centered
    title = "CROISSANT TOOLKIT"
    link = "https://github.com/4tikhonov/croissant-toolkit"
    cast_title = "CAST:"
    cast_names = [
        "Slava Tykhonov",
        "Aymen El ouagouti",
        "Sacha Henneuveux",
        "Elio Bteich"
    ]
    
    # Draw Title
    bbox_t = draw.textbbox((0, 0), title, font=f_huge)
    draw.text(((size[0]-(bbox_t[2]-bbox_t[0]))/2, 150), title, font=f_huge, fill=(255, 255, 255))
    
    # Accent Line
    draw.line((size[0]//2 - 400, 280, size[0]//2 + 400, 280), fill=(0, 255, 255), width=8)
    
    # Draw Link
    bbox_l = draw.textbbox((0, 0), link, font=f_sub)
    draw.text(((size[0]-(bbox_l[2]-bbox_l[0]))/2, 320), link, font=f_sub, fill=(0, 255, 255))
    
    # Draw Cast
    y_cast = 450
    draw.text((size[0]//2 - 50, y_cast), cast_title, font=f_cast_title, fill=(255, 200, 0))
    y_cast += 50
    for name in cast_names:
        bbox_n = draw.textbbox((0, 0), name, font=f_cast_names)
        draw.text(((size[0]-(bbox_n[2]-bbox_n[0]))/2, y_cast), name, font=f_cast_names, fill=(240, 240, 240))
        y_cast += 45
    
    draw.text((size[0]//2 - 150, 950), "SCALING OPEN DATA.", font=f_mid, fill=(100, 110, 130))
    img.save(output_path)

def render_worker_dossier(title, role, dept, tasks, screenshot_path, output_path, worker_id, bg_color, size=(1920, 1080)):
    img = Image.new('RGB', size, color=bg_color); draw = ImageDraw.Draw(img)
    is_light = sum(bg_color) / 3 > 128
    c_p, c_a, c_h, c_s = ((255,255,255),(0,200,255),(255,200,0),(140,160,180)) if not is_light else ((15,15,20),(0,120,220),(200,140,0),(100,110,120))
    f_id, f_n, f_r, f_d, f_b, f_l = get_font(24, True), get_font(42, True), get_font(26), get_font(28, True), get_font(26), get_font(18, True)
    if screenshot_path and os.path.exists(screenshot_path):
        ss = Image.open(screenshot_path).convert('RGB'); ss.thumbnail((1150, 900), Image.Resampling.LANCZOS)
        x_ss, y_ss = 680 + (1240 - ss.size[0]) // 2, (1080 - ss.size[1]) // 2 + 20
        draw.rectangle((x_ss-8, y_ss-8, x_ss+ss.size[0]+8, y_ss+ss.size[1]+8), outline=c_a, width=4); img.paste(ss, (x_ss, y_ss))
        draw.text((700, y_ss - 40), "WORK_OUTPUT_MONITOR // HD_FEED_ACTIVE", font=f_l, fill=c_a)
    draw.line((670, 80, 670, 1000), fill=(40, 50, 70) if not is_light else (200, 210, 220), width=2)
    draw.rectangle((80, 80, 400, 115), fill=c_a); draw.text((95, 82), worker_id, font=f_id, fill=(255,255,255) if is_light else (0,0,0))
    draw_worker_avatar(draw, 80, 150, 100, c_a); draw.text((200, 155), title.upper(), font=f_n, fill=c_p); draw.text((200, 210), role, font=f_r, fill=c_a)
    draw.text((80, 350), "DEPARTMENT", font=f_l, fill=c_s); draw.text((80, 385), dept.upper(), font=f_d, fill=c_h)
    draw.text((80, 480), "ACTIVE_OPERATIONS", font=f_l, fill=c_s)
    y_ops = 530
    for t in tasks: draw.text((80, y_ops), "•", font=f_b, fill=c_a); draw.text((120, y_ops), t, font=f_b, fill=c_p); y_ops += 50
    draw.text((80, 950), "WORKER_STATUS: ACTIVE // SHIFT: 24/7 // CLEARANCE: L5", font=f_l, fill=(100, 200, 100))
    img.save(output_path); return img

def generate_full_roster_movie(output_mp4):
    screenshot_dir, temp_dir = "cookbook/screenshots", "temp_roster_final"
    if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    workforce = [
        ("The Wizard", "Chief Orchestrator", "Core Infra", ["Full pipeline automation", "Multi-skill coordination", "Zero-touch integration", "Autonomous recovery"], os.path.join(screenshot_dir, "gemini_31_discovery.png"), "DW-001"),
        ("The Navigator", "Field Research Agent", "Intel Discovery", ["Real-time scraping", "Consent handling", "Stealth crawling"], os.path.join(screenshot_dir, "navigator.png"), "DW-002"),
        ("The YouTuber", "Video Intelligence Analyst", "Media Analysis", ["Channel metadata", "Recursive discovery", "Content mapping"], os.path.join(screenshot_dir, "youtuber.png"), "DW-003"),
        ("The Transcriber", "Audio-to-Text Specialist", "Media Processing", ["Precision text extraction", "Temporal synchronization", "Indexing sync"], os.path.join(screenshot_dir, "croissant.png"), "DW-004"),
        ("The Translator", "Linguistic Expert", "Global Comms", ["English precision translation", "Multimodal parsing", "Nuance localizer"], os.path.join(screenshot_dir, "gemini_31_discovery.png"), "DW-005"),
        ("The Semanticist", "NLP Cognitive Analyst", "Semantic Analysis", ["Named Entity Recognition", "Schema.org mapping", "Context weighting"], os.path.join(screenshot_dir, "croissant.png"), "DW-006"),
        ("The Standardizer", "Croissant Metadata Expert", "Data Governance", ["JSON-LD compliance", "Metadata serialization", "Standard sync"], os.path.join(screenshot_dir, "croissant.png"), "DW-007"),
        ("The Obsidian", "Lead Knowledge Archivist", "Data Persistence", ["Dataset memory", "Semantic graph linking", "Visual mapping"], os.path.join(screenshot_dir, "obsidian.png"), "DW-008"),
        ("The Walker", "Recursive Explorer", "Reconnaissance", ["Deep crawling logic", "Directory tree mapping", "Asset discovery"], os.path.join(screenshot_dir, "walker.png"), "DW-009"),
        ("The Graphologist", "Neo4j Relational Architect", "Knowledge Eng", ["Graph ingestion", "Relationship mapping", "Query optimization"], os.path.join(screenshot_dir, "neo4j.png"), "DW-010"),
        ("The Notifier", "Communication Officer", "Operations Grid", ["SMTP protocols", "Automated reporting", "System heartbeat"], os.path.join(screenshot_dir, "email_report_mockup.png"), "DW-011"),
        ("The Messenger", "Telegram Comms Agent", "Mobile Ops", ["Direct broadcasting", "Real-time delivery", "Stakeholder alerts"], os.path.join(screenshot_dir, "telegram.png"), "DW-012"),
        ("The Photographer", "Screenshot Taker", "Visual QA", ["Web visual archiving", "Multimodal context", "Evidence capture"], os.path.join(screenshot_dir, "navigator.png"), "DW-013"),
        ("The Presenter", "Presentation Architect", "Stakeholder Intel", ["Marp slide generation", "Technical deck orchestration", "Storytelling"], os.path.join(screenshot_dir, "email_report_mockup.png"), "DW-014"),
        ("The Producer", "Creator Media Specialist", "Visual Assets", ["Dynamic slideshows", "Animated intro creation", "Video rendering"], os.path.join(screenshot_dir, "email_report_mockup.png"), "DW-015"),
        ("The Auditor", "System Quality Tester", "Quality Assurance", ["Integration execution", "Health checks", "Verification logic"], os.path.join(screenshot_dir, "gemini_31_discovery.png"), "DW-016"),
        ("The Strategist", "Orchestrator General", "Executive Strategy", ["Task delegation", "Goal resolution", "Full-stack decision"], os.path.join(screenshot_dir, "gemini_31_discovery.png"), "DW-017")
    ]
    fps, intro_sec, outro_sec = 24, 5, 5
    worker_total_sec = 50 / len(workforce)
    fade_sec, frame_count = 1.0, 0
    
    # 1. Intro
    intro_p = os.path.join(temp_dir, "intro.png"); render_intro_slide(intro_p); intro_img = Image.open(intro_p)
    for _ in range(int(fps * intro_sec)): intro_img.save(os.path.join(temp_dir, f"frame_{frame_count:04d}.png")); frame_count += 1
    
    # 2. Workers
    prev_img = intro_img
    for i, (name, role, dept, tasks, img_p, wid) in enumerate(workforce):
        bg = (10, 12, 15) if i % 2 == 0 else (245, 245, 250)
        curr_img = render_worker_dossier(name, role, dept, tasks, img_p, os.path.join(temp_dir, f"raw_{i}.png"), wid, bg)
        num_f = int(fps * fade_sec)
        for f in range(num_f): Image.blend(prev_img, curr_img, f/num_f).save(os.path.join(temp_dir, f"frame_{frame_count:04d}.png")); frame_count += 1
        for _ in range(int(fps * (worker_total_sec - fade_sec))): curr_img.save(os.path.join(temp_dir, f"frame_{frame_count:04d}.png")); frame_count += 1
        prev_img = curr_img
        
    # 3. Outro
    outro_p = os.path.join(temp_dir, "outro.png"); render_outro_slide(outro_p); outro_img = Image.open(outro_p)
    num_f = int(fps * fade_sec)
    for f in range(num_f): Image.blend(prev_img, outro_img, f/num_f).save(os.path.join(temp_dir, f"frame_{frame_count:04d}.png")); frame_count += 1
    for _ in range(int(fps * outro_sec)): outro_img.save(os.path.join(temp_dir, f"frame_{frame_count:04d}.png")); frame_count += 1
            
    subprocess.run(["ffmpeg", "-y", "-framerate", str(fps), "-i", os.path.join(temp_dir, "frame_%04d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23", "-preset", "slow", "-movflags", "+faststart", "-t", "60", output_mp4], check=True, capture_output=True)
    shutil.rmtree(temp_dir); print(f"[Creator] Final Movie Ready! [RESULT_PATH]: {os.path.abspath(output_mp4)}")

if __name__ == "__main__":
    out = ".gemini/skills/creator/video_output/croissant_youtube_1080p.mp4"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    generate_full_roster_movie(out)
