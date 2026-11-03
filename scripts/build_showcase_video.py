#!/usr/bin/env python3
"""
High-Production Developer Showcase Video & GIF Generator
for Pranav Sharma's GitHub Profile README.
"""
import os
import sys
import math
import wave
import struct
import random
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1280, 720
FPS = 30
DURATION = 25.0
TOTAL_FRAMES = int(FPS * DURATION)

FONT_DIR = "/System/Library/Fonts"

try:
    font_mono_xs = ImageFont.truetype(f"{FONT_DIR}/Menlo.ttc", 13)
    font_mono_sm = ImageFont.truetype(f"{FONT_DIR}/Menlo.ttc", 15)
    font_mono_md = ImageFont.truetype(f"{FONT_DIR}/Menlo.ttc", 18)
    font_mono_bold = ImageFont.truetype(f"{FONT_DIR}/Menlo.ttc", 19, index=1)
    font_mono_lg = ImageFont.truetype(f"{FONT_DIR}/Menlo.ttc", 24, index=1)
    
    font_sans_xs = ImageFont.truetype(f"{FONT_DIR}/Helvetica.ttc", 13)
    font_sans_sm = ImageFont.truetype(f"{FONT_DIR}/Helvetica.ttc", 16)
    font_sans_md = ImageFont.truetype(f"{FONT_DIR}/Helvetica.ttc", 18)
    font_sans_bold = ImageFont.truetype(f"{FONT_DIR}/Helvetica.ttc", 20, index=1)
    font_sans_lg = ImageFont.truetype(f"{FONT_DIR}/Helvetica.ttc", 25, index=1)
    font_sans_xl = ImageFont.truetype(f"{FONT_DIR}/Helvetica.ttc", 36, index=1)
except Exception as e:
    print(f"Font loading error: {e}")
    font_mono_xs = font_mono_sm = font_mono_md = font_mono_bold = font_mono_lg = ImageFont.load_default()
    font_sans_xs = font_sans_sm = font_sans_md = font_sans_bold = font_sans_lg = font_sans_xl = ImageFont.load_default()

# Colors
BG_DARK = (9, 13, 22)
SURFACE_DARK = (15, 21, 35)
CARD_BG = (18, 26, 44)
BORDER_MUTED = (30, 42, 64)
BORDER_ACTIVE = (45, 65, 96)
TEXT_WHITE = (248, 250, 252)
TEXT_MUTED = (148, 163, 184)
TEXT_DIM = (100, 116, 139)

NEON_GREEN = (0, 255, 157)
NEON_CYAN = (0, 229, 255)
AMBER_LEET = (255, 161, 22)
ROSE_ACCENT = (244, 114, 182)
BLUE_ACCENT = (56, 189, 248)

# Paths to Real Project Assets
PHOTO_PATH = "../personal_stuff/Personal.jpeg"
FLASHDROP_PATH = "../Project_Stuff/flashDrop_Daashboard .png"
RECALL_CARDS_PATH = "../Project_Stuff/recall_stuff/2.png"
RECALL_LOGO_PATH = "../Project_Stuff/recall_stuff/recalLc.png"
LEETCOMETE_LOGO_PATH = "../LeetComete/logo.png"
LEETCOMETE_POPUP_PATH = "../LeetComete/images/640x400/4_autocomplete_keywords.png"
LEETCODE_STAT_PATH = "../Project_Stuff/Screenshot 2026-10-30 at 12.33.18 AM.png"

def round_image_corners(im, radius):
    mask = Image.new("L", im.size, 255)
    d = ImageDraw.Draw(mask)
    # create rounded corner mask
    d.rectangle([(0, 0), im.size], fill=0)
    d.rounded_rectangle([(0, 0), im.size], radius=radius, fill=255)
    rounded = Image.new("RGBA", im.size, (0, 0, 0, 0))
    rounded.paste(im.convert("RGBA"), (0, 0), mask=mask)
    return rounded

def load_all_assets():
    assets = {}
    
    # 1. Professional Photo (Circular crop)
    if os.path.exists(PHOTO_PATH):
        try:
            raw = Image.open(PHOTO_PATH).convert("RGBA")
            w, h = raw.size
            dim = min(w, h)
            left = (w - dim) // 2
            top = (h - dim) // 2
            sq = raw.crop((left, top, left + dim, top + dim)).resize((140, 140), Image.Resampling.LANCZOS)
            
            mask = Image.new("L", (140, 140), 0)
            dmask = ImageDraw.Draw(mask)
            dmask.ellipse([(0, 0), (140, 140)], fill=255)
            
            circ = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
            circ.paste(sq, (0, 0), mask=mask)
            assets['photo'] = circ
        except Exception as e:
            print("Photo load error:", e)
            assets['photo'] = None
    else:
        assets['photo'] = None

    # 2. FlashDrop Screenshot
    if os.path.exists(FLASHDROP_PATH):
        try:
            im = Image.open(FLASHDROP_PATH).convert("RGB")
            w, h = im.size
            crop_box = (int(w * 0.05), int(h * 0.1), int(w * 0.95), int(h * 0.95))
            cropped = im.crop(crop_box).resize((570, 400), Image.Resampling.LANCZOS)
            assets['flashdrop'] = round_image_corners(cropped, 10)
        except Exception as e:
            print("Flashdrop load error:", e)
            assets['flashdrop'] = None
    else:
        assets['flashdrop'] = None

    # 3. RecalLC Mockup
    if os.path.exists(RECALL_CARDS_PATH) and os.path.exists(RECALL_LOGO_PATH):
        try:
            cards_im = Image.open(RECALL_CARDS_PATH).convert("RGB")
            cw, ch = cards_im.size
            cards_crop = cards_im.crop((int(cw * 0.16), int(ch * 0.08), int(cw * 0.84), int(ch * 0.65)))
            cards_resized = cards_crop.resize((570, 310), Image.Resampling.LANCZOS)
            
            logo_raw = Image.open(RECALL_LOGO_PATH).convert("RGBA").resize((76, 76), Image.Resampling.LANCZOS)
            
            recall_frame = Image.new("RGB", (570, 400), (18, 20, 29))
            recall_frame.paste(cards_resized, (0, 90))
            recall_frame.paste(logo_raw, (15, 8), mask=logo_raw)
            
            rf_draw = ImageDraw.Draw(recall_frame)
            rf_draw.text((105, 20), "RecalLC • LeetCode Spaced Repetition", font=font_sans_bold, fill=TEXT_WHITE)
            rf_draw.text((105, 48), "SM-2 Interval Scheduling & Problem Mastery Queues", font=font_mono_xs, fill=AMBER_LEET)
            assets['recall'] = round_image_corners(recall_frame, 10)
        except Exception as e:
            print("RecalLC load error:", e)
            assets['recall'] = None
    else:
        assets['recall'] = None

    # 4. LeetComete Mockup
    if os.path.exists(LEETCOMETE_LOGO_PATH) and os.path.exists(LEETCOMETE_POPUP_PATH):
        try:
            lc_logo = Image.open(LEETCOMETE_LOGO_PATH).convert("RGBA").resize((170, 170), Image.Resampling.LANCZOS)
            lc_popup = Image.open(LEETCOMETE_POPUP_PATH).convert("RGB").resize((360, 290), Image.Resampling.LANCZOS)
            
            lc_frame = Image.new("RGB", (570, 400), (16, 20, 32))
            lc_frame.paste(lc_logo, (15, 110), mask=lc_logo)
            lc_frame.paste(lc_popup, (195, 95))
            
            lc_draw = ImageDraw.Draw(lc_frame)
            lc_draw.text((20, 20), "LeetComete Autocomplete Engine", font=font_sans_bold, fill=TEXT_WHITE)
            lc_draw.text((20, 48), "Monaco Editor Integration • 15+ Languages • Zero Telemetry", font=font_mono_xs, fill=ROSE_ACCENT)
            assets['leetcomete'] = round_image_corners(lc_frame, 10)
        except Exception as e:
            print("LeetComete load error:", e)
            assets['leetcomete'] = None
    else:
        assets['leetcomete'] = None

    # 5. LeetCode Stat Widget
    if os.path.exists(LEETCODE_STAT_PATH):
        try:
            raw_stat = Image.open(LEETCODE_STAT_PATH).convert("RGB").resize((84, 62), Image.Resampling.LANCZOS)
            assets['lc_stat'] = round_image_corners(raw_stat, 8)
        except Exception as e:
            print("LC stat load error:", e)
            assets['lc_stat'] = None
    else:
        assets['lc_stat'] = None

    return assets

ASSETS = load_all_assets()

def generate_audio_track(output_wav_path, duration_sec):
    sr = 44100
    n_samples = int(sr * duration_sec)
    
    def chord_freqs(t):
        cycle = 6.25
        idx = int(t / cycle) % 4
        if idx == 0:
            return [110.0, 220.0, 261.63, 329.63, 440.0]  # Am
        elif idx == 1:
            return [87.31, 174.61, 220.0, 261.63, 349.23] # F
        elif idx == 2:
            return [130.81, 196.0, 261.63, 329.63, 392.0] # C
        else:
            return [98.0, 196.0, 246.94, 293.66, 392.0]  # G

    samples = []
    for i in range(n_samples):
        t = i / sr
        freqs = chord_freqs(t)
        
        val_l = 0.0
        val_r = 0.0
        for j, f in enumerate(freqs):
            amp = 0.15 / (j + 1)
            detune = 0.002 * (j - 2)
            val_l += amp * math.sin(2 * math.pi * f * (1 + detune) * t)
            val_r += amp * math.sin(2 * math.pi * f * (1 - detune) * t + 0.3)
        
        # Soft techno beat pulse
        beat_t = t % 0.5
        if beat_t < 0.04:
            env = math.exp(-beat_t * 90)
            pulse = math.sin(2 * math.pi * 1400 * beat_t) * env * 0.035
            val_l += pulse
            val_r += pulse

        # Typing clicks in intro
        if t < 4.2 and (t % 0.11) < 0.015:
            click = random.uniform(-0.03, 0.03) * math.exp(-(t % 0.11) * 250)
            val_l += click
            val_r += click
            
        # Subtle sweep whoosh
        for trans_t in [4.2, 8.4, 12.6, 16.8, 21.0]:
            diff = t - trans_t
            if -0.2 < diff < 0.2:
                sweep_freq = 600 + (diff + 0.2) * 2200
                env = math.cos(diff / 0.2 * math.pi * 0.5) ** 2
                whoosh = math.sin(2 * math.pi * sweep_freq * t) * env * 0.035
                val_l += whoosh
                val_r += whoosh
                
        # Fade in & out
        if t < 0.8:
            fade = t / 0.8
        elif t > duration_sec - 1.2:
            fade = max(0.0, (duration_sec - t) / 1.2)
        else:
            fade = 1.0
            
        val_l = max(-0.95, min(0.95, val_l * fade))
        val_r = max(-0.95, min(0.95, val_r * fade))
        
        s_l = int(val_l * 32767)
        s_r = int(val_r * 32767)
        samples.append(struct.pack('<hh', s_l, s_r))

    with wave.open(output_wav_path, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(b''.join(samples))
    print(f"Audio synthesized successfully -> {output_wav_path}")

def draw_rounded_rect(draw, box, radius, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def render_frame(f_idx):
    t = f_idx / FPS
    progress = f_idx / (TOTAL_FRAMES - 1)
    
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    # 1. Perspective Background Grid
    grid_offset = int((t * 10) % 40)
    for x in range(grid_offset, W, 40):
        draw.line([(x, 44), (x, H - 36)], fill=(14, 20, 33), width=1)
    for y in range(44, H - 36, 40):
        draw.line([(0, y), (W, y)], fill=(14, 20, 33), width=1)
        
    # 2. Window Chrome Bar (macOS Terminal)
    draw.rectangle([(0, 0), (W, 44)], fill=(13, 17, 27))
    draw.line([(0, 44), (W, 44)], fill=BORDER_MUTED, width=1)
    
    # Window traffic lights
    draw.ellipse([(20, 16), (32, 28)], fill=(255, 95, 86))
    draw.ellipse([(42, 16), (54, 28)], fill=(255, 189, 46))
    draw.ellipse([(64, 16), (76, 28)], fill=(39, 201, 63))
    
    # Terminal Title Bar
    title = "pranav@terminal: ~/PranavSharma1008 (main) --profile=showcase"
    draw.text((95, 13), title, font=font_mono_sm, fill=TEXT_MUTED)
    
    # Live Status Badge
    dot_color = NEON_GREEN if int(t * 2) % 2 == 0 else (0, 180, 110)
    draw.ellipse([(W - 195, 18), (W - 187, 26)], fill=dot_color)
    draw.text((W - 178, 13), "OPEN TO WORK", font=font_mono_bold, fill=NEON_GREEN)
    
    # 3. Bottom Status Bar & Progress Line
    draw.rectangle([(0, H - 36), (W, H)], fill=(13, 17, 27))
    draw.line([(0, H - 36), (W, H - 36)], fill=BORDER_MUTED, width=1)
    
    status_text = "PRANAV SHARMA // FULL STACK & LOW-LATENCY SYSTEMS // DSA SPECIALIST"
    draw.text((25, H - 26), status_text, font=font_mono_xs, fill=TEXT_DIM)
    
    time_str = f"[{int(t):02d}:{int((t%1)*100):02d} / 25:00]  1080p 60fps"
    draw.text((W - 240, H - 26), time_str, font=font_mono_xs, fill=TEXT_MUTED)
    
    # Neon progress indicator at bottom edge
    progress_w = int(W * progress)
    draw.rectangle([(0, H - 3), (progress_w, H)], fill=NEON_GREEN)

    # 4. Scenes Routing
    if t < 4.2:
        render_scene_intro(draw, img, t)
    elif t < 8.4:
        render_scene_tech_stack(draw, img, t - 4.2)
    elif t < 12.6:
        render_scene_flashdrop(draw, img, t - 8.4)
    elif t < 16.8:
        render_scene_recall(draw, img, t - 12.6)
    elif t < 21.0:
        render_scene_leetcomete(draw, img, t - 16.8)
    else:
        render_scene_outro(draw, img, t - 21.0)

    return img

def render_scene_intro(draw, img, st):
    card_box = (80, 75, W - 80, H - 70)
    draw_rounded_rect(draw, card_box, radius=14, fill=SURFACE_DARK, outline=BORDER_ACTIVE, width=2)
    
    draw.rectangle([(80, 75), (W - 80, 125)], fill=(19, 26, 42))
    draw.line([(80, 125), (W - 80, 125)], fill=BORDER_MUTED, width=1)
    
    cursor = "_" if int(st * 4) % 2 == 0 else " "
    prompt_full = "$ whoami --role='Software Engineer' && cat identity.json"
    type_len = min(len(prompt_full), int(st * 26))
    prompt_typed = prompt_full[:type_len] + cursor
    draw.text((105, 93), prompt_typed, font=font_mono_md, fill=NEON_CYAN)

    # Left: Professional Portrait Card
    port_box = (120, 155, 300, 420)
    draw_rounded_rect(draw, port_box, radius=12, fill=(12, 17, 28), outline=BORDER_MUTED, width=1)
    
    center_x = (120 + 300) // 2
    if ASSETS.get('photo'):
        pulse = 0.5 + 0.5 * math.sin(st * 5.0)
        ring_col = (0, int(200 + 55 * pulse), int(120 + 37 * pulse))
        draw.ellipse([(center_x - 73, 172), (center_x + 73, 318)], outline=ring_col, width=3)
        img.paste(ASSETS['photo'], (center_x - 70, 175), mask=ASSETS['photo'])
    else:
        draw.ellipse([(center_x - 70, 175), (center_x + 70, 315)], fill=(30, 45, 70), outline=NEON_GREEN, width=2)
        draw.text((center_x - 25, 230), "PS", font=font_sans_xl, fill=TEXT_WHITE)

    name_w = int(draw.textlength("PRANAV SHARMA", font=font_mono_bold))
    draw.text((center_x - (name_w // 2), 345), "PRANAV SHARMA", font=font_mono_bold, fill=TEXT_WHITE)
    
    role_w = int(draw.textlength("Computer Science Engineer", font=font_sans_xs))
    draw.text((center_x - (role_w // 2), 375), "Computer Science Engineer", font=font_sans_xs, fill=NEON_GREEN)

    # Right Content Area
    draw.text((335, 155), "Hi, I'm Pranav Sharma", font=font_sans_xl, fill=TEXT_WHITE)
    draw.text((335, 210), "Software Engineer | Full Stack & Low-Latency Systems", font=font_sans_lg, fill=NEON_GREEN)
    
    line1 = "Passionate engineer specialized in high-throughput architectures, distributed systems,"
    line2 = "algorithmic problem solving (DSA in Java/C++), and privacy-first developer tools."
    draw.text((335, 260), line1, font=font_sans_sm, fill=TEXT_MUTED)
    draw.text((335, 288), line2, font=font_sans_sm, fill=TEXT_MUTED)

    # Badges
    pills_row1 = [
        (">> Full-Stack & Systems", NEON_CYAN),
        (">> DSA & Backend Focus", AMBER_LEET),
        (">> 85 WPM Touch Typist", NEON_GREEN),
    ]
    px = 335
    for text, col in pills_row1:
        tw = int(draw.textlength(text, font=font_mono_xs)) + 24
        draw_rounded_rect(draw, (px, 335, px + tw, 370), radius=6, fill=(20, 28, 44), outline=col, width=1)
        draw.text((px + 12, 345), text, font=font_mono_xs, fill=col)
        px += tw + 14

    pills_row2 = [
        ("[*] Comp Science Eng", TEXT_WHITE),
        ("[*] @badshahcoder1008 (YouTube)", ROSE_ACCENT),
        ("[*] Open to Global Roles", BLUE_ACCENT),
    ]
    px2 = 335
    for text, col in pills_row2:
        tw = int(draw.textlength(text, font=font_mono_xs)) + 24
        draw_rounded_rect(draw, (px2, 385, px2 + tw, 420), radius=6, fill=(20, 28, 44), outline=BORDER_MUTED, width=1)
        draw.text((px2 + 12, 395), text, font=font_mono_xs, fill=col)
        px2 += tw + 14

    # Terminal Code Block
    draw_rounded_rect(draw, (120, 445, W - 120, 605), radius=10, fill=(12, 17, 27), outline=BORDER_MUTED, width=1)
    
    term_lines = [
        ("const engineer = {", TEXT_MUTED),
        ("  name: 'Pranav Sharma', role: 'Software Engineer', focus: 'High-Throughput Systems',", TEXT_WHITE),
        ("  coreCompetencies: ['Data Structures & Algorithms', 'Low-Latency Sockets', 'System Design'],", NEON_CYAN),
        ("  primaryLanguages: ['Java', 'C++', 'Python', 'JavaScript', 'TypeScript'],", NEON_GREEN),
        ("  philosophy: 'Clean architecture, zero telemetry, and maximum performance.'", AMBER_LEET),
        ("};", TEXT_MUTED),
    ]
    ty = 458
    for l_text, l_col in term_lines:
        draw.text((140, ty), l_text, font=font_mono_xs, fill=l_col)
        ty += 23

def render_scene_tech_stack(draw, img, st):
    draw_rounded_rect(draw, (80, 70, W - 80, 130), radius=10, fill=SURFACE_DARK, outline=BORDER_ACTIVE, width=1)
    draw.text((105, 80), ":: ENGINEERING COMPETENCIES & TECH STACK ::", font=font_mono_bold, fill=TEXT_WHITE)
    draw.text((105, 106), "Architected for Scalability, High Throughput, and Rock-Solid Stability", font=font_sans_sm, fill=NEON_GREEN)
    
    cards = [
        {
            "box": (80, 150, 620, 365),
            "title": "PROGRAMMING LANGUAGES",
            "accent": NEON_CYAN,
            "badge": "POLYGLOT",
            "items": ["C", "C++", "Java 17 (DSA Core)", "Python 3", "JavaScript", "TypeScript"],
            "desc1": "High-speed socket operations, algorithmic efficiency, and OOP.",
            "desc2": "Production-tested across backend services and browser platforms."
        },
        {
            "box": (660, 150, W - 80, 365),
            "title": "BACKEND & SYSTEMS",
            "accent": NEON_GREEN,
            "badge": "HIGH CONCURRENCY",
            "items": ["Node.js", "Express.js", "Spring Boot", "TCP Sockets", "WebSockets / Socket.IO"],
            "desc1": "RESTful microservices, event-driven socket pipelines, and P2P protocols.",
            "desc2": "Low-level buffer management and bi-directional real-time streaming."
        },
        {
            "box": (80, 385, 620, 605),
            "title": "DATABASES & CLOUD INFRA",
            "accent": AMBER_LEET,
            "badge": "DATA & INFRA",
            "items": ["MongoDB", "MySQL", "IndexedDB", "Linux / Unix", "Git / GitHub", "Vercel / Render"],
            "desc1": "ACID transactional guarantees, document modeling, and local IndexedDB.",
            "desc2": "Automated deployments, robust version control, and Linux environments."
        },
        {
            "box": (660, 385, W - 80, 605),
            "title": "FRONTEND & BROWSER EXTENSIONS",
            "accent": ROSE_ACCENT,
            "badge": "CLIENT TOOLS",
            "items": ["React 18", "Tailwind CSS", "Chrome MV3", "Monaco Editor", "Vitest", "HTML5/CSS3"],
            "desc1": "Local-first Chrome extensions with zero tracking or telemetry overhead.",
            "desc2": "Accessible responsive UIs and comprehensive Vitest unit test suites."
        }
    ]

    for c in cards:
        x0, y0, x1, y1 = c['box']
        draw_rounded_rect(draw, (x0, y0, x1, y1), radius=12, fill=SURFACE_DARK, outline=BORDER_ACTIVE, width=1)
        
        draw.line([(x0, y0 + 42), (x1, y0 + 42)], fill=BORDER_MUTED, width=1)
        draw.text((x0 + 18, y0 + 12), c['title'], font=font_mono_bold, fill=c['accent'])
        
        badge_w = int(draw.textlength(c['badge'], font=font_mono_xs)) + 16
        draw_rounded_rect(draw, (x1 - badge_w - 18, y0 + 10, x1 - 18, y0 + 32), radius=5, fill=(22, 30, 48), outline=c['accent'], width=1)
        draw.text((x1 - badge_w - 10, y0 + 14), c['badge'], font=font_mono_xs, fill=c['accent'])
        
        ix = x0 + 18
        iy = y0 + 56
        for item in c['items']:
            iw = int(draw.textlength(item, font=font_mono_xs)) + 18
            if ix + iw > x1 - 18:
                ix = x0 + 18
                iy += 32
            draw_rounded_rect(draw, (ix, iy, ix + iw, iy + 25), radius=5, fill=(20, 28, 44), outline=BORDER_MUTED, width=1)
            draw.text((ix + 9, iy + 5), item, font=font_mono_xs, fill=TEXT_WHITE)
            ix += iw + 8
            
        draw.text((x0 + 18, y1 - 48), c['desc1'], font=font_sans_xs, fill=TEXT_MUTED)
        draw.text((x0 + 18, y1 - 28), c['desc2'], font=font_sans_xs, fill=TEXT_MUTED)

def render_scene_flashdrop(draw, img, st):
    draw_rounded_rect(draw, (80, 65, W - 80, 125), radius=10, fill=SURFACE_DARK, outline=BORDER_ACTIVE, width=1)
    draw.text((105, 76), "// FEATURED PROJECT 01 OF 03", font=font_mono_sm, fill=NEON_CYAN)
    draw.text((105, 96), "FlashDrop -- High-Speed Local P2P File Transfer Engine", font=font_sans_lg, fill=TEXT_WHITE)
    
    # Left Details Panel
    draw_rounded_rect(draw, (80, 140, 590, 605), radius=12, fill=SURFACE_DARK, outline=BORDER_ACTIVE, width=1)
    
    draw_rounded_rect(draw, (105, 160, 290, 190), radius=6, fill=(16, 28, 46), outline=NEON_CYAN, width=1)
    draw.text((117, 168), "NETWORK ARCHITECTURE", font=font_mono_xs, fill=NEON_CYAN)
    
    draw.text((105, 205), "Direct IP-to-IP File Sharing", font=font_sans_lg, fill=TEXT_WHITE)
    
    bullets = [
        "- Transfers large files directly between devices at line rate.",
        "- Zero cloud dependency -- 100% private and decentralized.",
        "- Low-level socket buffer tuning and packet chunking protocols.",
        "- Clean Flask web interface with dynamic IP / QR device pairing.",
        "- Engineered with Python, TCP Sockets, Flask, and Web UI."
    ]
    by = 250
    for b in bullets:
        draw.text((105, by), b, font=font_sans_sm, fill=TEXT_MUTED)
        by += 32
        
    tags = ["Python", "TCP Sockets", "Flask", "P2P Transfer", "Buffer Tuning"]
    tx = 105
    for tag in tags:
        tw = int(draw.textlength(tag, font=font_mono_xs)) + 16
        draw_rounded_rect(draw, (tx, 480, tx + tw, 508), radius=5, fill=(20, 30, 48), outline=NEON_GREEN, width=1)
        draw.text((tx + 8, 488), tag, font=font_mono_xs, fill=NEON_GREEN)
        tx += tw + 10
        
    draw_rounded_rect(draw, (105, 530, 565, 575), radius=8, fill=(13, 19, 31), outline=BORDER_MUTED, width=1)
    draw.text((120, 544), ">> github.com/PranavSharma1008/FlashDrop", font=font_mono_sm, fill=NEON_CYAN)

    # Right Mockup Panel
    mock_box = (615, 140, W - 80, 605)
    draw_rounded_rect(draw, mock_box, radius=12, fill=SURFACE_DARK, outline=NEON_GREEN, width=2)
    
    draw.rectangle([(615, 140), (W - 80, 178)], fill=(18, 24, 38))
    draw.line([(615, 178), (W - 80, 178)], fill=BORDER_MUTED, width=1)
    draw.ellipse([(630, 154), (640, 164)], fill=(255, 95, 86))
    draw.ellipse([(648, 154), (658, 164)], fill=(255, 189, 46))
    draw.ellipse([(666, 154), (676, 164)], fill=(39, 201, 63))
    draw.text((690, 152), "FlashDrop Dashboard -- http://192.168.1.100:5000", font=font_mono_xs, fill=TEXT_MUTED)
    
    if ASSETS.get('flashdrop'):
        img.paste(ASSETS['flashdrop'], (625, 188), mask=ASSETS['flashdrop'])

def render_scene_recall(draw, img, st):
    draw_rounded_rect(draw, (80, 65, W - 80, 125), radius=10, fill=SURFACE_DARK, outline=BORDER_ACTIVE, width=1)
    draw.text((105, 76), "// FEATURED PROJECT 02 OF 03", font=font_mono_sm, fill=AMBER_LEET)
    draw.text((105, 96), "RecalLC -- LeetCode Spaced Repetition Assistant", font=font_sans_lg, fill=TEXT_WHITE)
    
    # Left Details Panel
    draw_rounded_rect(draw, (80, 140, 590, 605), radius=12, fill=SURFACE_DARK, outline=BORDER_ACTIVE, width=1)
    
    draw_rounded_rect(draw, (105, 160, 310, 190), radius=6, fill=(34, 25, 14), outline=AMBER_LEET, width=1)
    draw.text((117, 168), "CHROME EXTENSION (MV3)", font=font_mono_xs, fill=AMBER_LEET)
    
    draw.text((105, 205), "Algorithmic Spaced Repetition", font=font_sans_lg, fill=TEXT_WHITE)
    
    bullets = [
        "- Privacy-first Chrome MV3 extension with zero external telemetry.",
        "- Custom SuperMemo SM-2 interval spaced repetition engine.",
        "- Struggle score tracking and personalized revision queue generation.",
        "- 100% client-side persistence via high-performance IndexedDB.",
        "- Topic-wise mastery analytics across DP, Trees, Graphs, and Greedy."
    ]
    by = 250
    for b in bullets:
        draw.text((105, by), b, font=font_sans_sm, fill=TEXT_MUTED)
        by += 32
        
    tags = ["Chrome MV3", "React 18", "TypeScript", "IndexedDB", "SM-2 Algo"]
    tx = 105
    for tag in tags:
        tw = int(draw.textlength(tag, font=font_mono_xs)) + 16
        draw_rounded_rect(draw, (tx, 480, tx + tw, 508), radius=5, fill=(32, 24, 16), outline=AMBER_LEET, width=1)
        draw.text((tx + 8, 488), tag, font=font_mono_xs, fill=AMBER_LEET)
        tx += tw + 10
        
    draw_rounded_rect(draw, (105, 530, 565, 575), radius=8, fill=(13, 19, 31), outline=BORDER_MUTED, width=1)
    draw.text((120, 544), ">> github.com/PranavSharma1008/RecalLc", font=font_mono_sm, fill=AMBER_LEET)

    # Right Mockup Panel
    mock_box = (615, 140, W - 80, 605)
    draw_rounded_rect(draw, mock_box, radius=12, fill=SURFACE_DARK, outline=AMBER_LEET, width=2)
    
    draw.rectangle([(615, 140), (W - 80, 178)], fill=(18, 24, 38))
    draw.line([(615, 178), (W - 80, 178)], fill=BORDER_MUTED, width=1)
    draw.ellipse([(630, 154), (640, 164)], fill=(255, 95, 86))
    draw.ellipse([(648, 154), (658, 164)], fill=(255, 189, 46))
    draw.ellipse([(666, 154), (676, 164)], fill=(39, 201, 63))
    draw.text((690, 152), "RecalLC Extension -- Spaced Repetition Mastery Engine", font=font_mono_xs, fill=TEXT_MUTED)
    
    if ASSETS.get('recall'):
        img.paste(ASSETS['recall'], (625, 188), mask=ASSETS['recall'])

def render_scene_leetcomete(draw, img, st):
    draw_rounded_rect(draw, (80, 65, W - 80, 125), radius=10, fill=SURFACE_DARK, outline=BORDER_ACTIVE, width=1)
    draw.text((105, 76), "// FEATURED PROJECT 03 OF 03", font=font_mono_sm, fill=ROSE_ACCENT)
    draw.text((105, 96), "LeetComete -- VS Code-Style Autocomplete Extension", font=font_sans_lg, fill=TEXT_WHITE)
    
    # Left Details Panel
    draw_rounded_rect(draw, (80, 140, 590, 605), radius=12, fill=SURFACE_DARK, outline=BORDER_ACTIVE, width=1)
    
    draw_rounded_rect(draw, (105, 160, 290, 190), radius=6, fill=(34, 18, 28), outline=ROSE_ACCENT, width=1)
    draw.text((117, 168), "DEVELOPER TOOLING", font=font_mono_xs, fill=ROSE_ACCENT)
    
    draw.text((105, 205), "Sub-Millisecond Autocomplete", font=font_sans_lg, fill=TEXT_WHITE)
    
    bullets = [
        "- Local-first code completion for LeetCode, GFG & Codeforces.",
        "- Monaco editor integration with 15+ language syntax trees.",
        "- Sub-millisecond latency -- executes purely within browser context.",
        "- Complete zero telemetry policy -- private and local.",
        "- Validated with comprehensive Vitest unit and regression suites."
    ]
    by = 250
    for b in bullets:
        draw.text((105, by), b, font=font_sans_sm, fill=TEXT_MUTED)
        by += 32
        
    tags = ["Chrome MV3", "TypeScript", "Monaco", "Vitest", "Zero-Telemetry"]
    tx = 105
    for tag in tags:
        tw = int(draw.textlength(tag, font=font_mono_xs)) + 14
        draw_rounded_rect(draw, (tx, 480, tx + tw, 508), radius=5, fill=(32, 18, 28), outline=ROSE_ACCENT, width=1)
        draw.text((tx + 7, 488), tag, font=font_mono_xs, fill=ROSE_ACCENT)
        tx += tw + 8
        
    draw_rounded_rect(draw, (105, 530, 565, 575), radius=8, fill=(13, 19, 31), outline=BORDER_MUTED, width=1)
    draw.text((120, 544), ">> github.com/PranavSharma1008/LeetComete", font=font_mono_sm, fill=ROSE_ACCENT)

    # Right Mockup Panel
    mock_box = (615, 140, W - 80, 605)
    draw_rounded_rect(draw, mock_box, radius=12, fill=SURFACE_DARK, outline=ROSE_ACCENT, width=2)
    
    draw.rectangle([(615, 140), (W - 80, 178)], fill=(18, 24, 38))
    draw.line([(615, 178), (W - 80, 178)], fill=BORDER_MUTED, width=1)
    draw.ellipse([(630, 154), (640, 164)], fill=(255, 95, 86))
    draw.ellipse([(648, 154), (658, 164)], fill=(255, 189, 46))
    draw.ellipse([(666, 154), (676, 164)], fill=(39, 201, 63))
    draw.text((690, 152), "LeetComete Extension -- Intelligent Monaco Autocomplete", font=font_mono_xs, fill=TEXT_MUTED)
    
    if ASSETS.get('leetcomete'):
        img.paste(ASSETS['leetcomete'], (625, 188), mask=ASSETS['leetcomete'])

def render_scene_outro(draw, img, st):
    draw_rounded_rect(draw, (80, 65, W - 80, 125), radius=10, fill=SURFACE_DARK, outline=NEON_GREEN, width=1)
    draw.text((105, 76), "// CODING HIGHLIGHTS & CONTACT", font=font_mono_sm, fill=NEON_GREEN)
    draw.text((105, 96), "Ready to Ship High-Performance, Scalable Software", font=font_sans_lg, fill=TEXT_WHITE)
    
    # 3 Metrics Cards Row
    card_w = (W - 160 - 40) // 3
    
    # Metric 1: Monkeytype Typist
    draw_rounded_rect(draw, (80, 140, 80 + card_w, 235), radius=10, fill=SURFACE_DARK, outline=BORDER_ACTIVE, width=1)
    draw.text((100, 156), "[*] 85 WPM PEAK SPEED", font=font_mono_bold, fill=NEON_GREEN)
    draw.text((100, 185), "100% Accuracy on Monkeytype", font=font_sans_sm, fill=TEXT_WHITE)
    draw.text((100, 208), "MacBook Air M2 • Touch Typist", font=font_mono_xs, fill=TEXT_MUTED)

    # Metric 2: LeetCode & GFG Algorithmic Solver
    mx2 = 80 + card_w + 20
    draw_rounded_rect(draw, (mx2, 140, mx2 + card_w, 235), radius=10, fill=SURFACE_DARK, outline=BORDER_ACTIVE, width=1)
    draw.text((mx2 + 18, 156), "[*] ALGORITHMIC FOCUS", font=font_mono_bold, fill=AMBER_LEET)
    draw.text((mx2 + 18, 183), "LeetCode & GeeksforGeeks", font=font_sans_sm, fill=TEXT_WHITE)
    draw.text((mx2 + 18, 206), "DP, Graphs, Trees in Java", font=font_mono_xs, fill=TEXT_MUTED)
    if ASSETS.get('lc_stat'):
        img.paste(ASSETS['lc_stat'], (mx2 + card_w - 92, 154), mask=ASSETS['lc_stat'])

    # Metric 3: YouTube Channel
    mx3 = mx2 + card_w + 20
    draw_rounded_rect(draw, (mx3, 140, mx3 + card_w, 235), radius=10, fill=SURFACE_DARK, outline=BORDER_ACTIVE, width=1)
    draw.text((mx3 + 18, 156), "[*] TECH CONTENT CREATOR", font=font_mono_bold, fill=ROSE_ACCENT)
    draw.text((mx3 + 18, 185), "@badshahcoder1008 (YouTube)", font=font_sans_sm, fill=TEXT_WHITE)
    draw.text((mx3 + 18, 208), "Tutorials & system walkthroughs", font=font_mono_xs, fill=TEXT_MUTED)

    # Big CTA Card
    cta_box = (80, 255, W - 80, 605)
    draw_rounded_rect(draw, cta_box, radius=14, fill=(14, 20, 32), outline=BORDER_ACTIVE, width=2)
    
    draw.text((115, 280), "Looking for a Software Engineer who ships clean, robust code?", font=font_sans_lg, fill=TEXT_WHITE)
    draw.text((115, 318), "Open to Full-Time Software Engineering & Backend Roles Globally", font=font_sans_md, fill=NEON_GREEN)
    
    contacts = [
        (">> Email", "pranav2410991479@gmail.com", NEON_CYAN),
        (">> Portfolio", "pranavsharmaportfolio.vercel.app", TEXT_WHITE),
        (">> LinkedIn", "linkedin.com/in/pranavsharma1008", NEON_CYAN),
        (">> GitHub", "github.com/PranavSharma1008", TEXT_WHITE),
    ]
    cx = 115
    cy = 365
    for label, val, col in contacts:
        draw_rounded_rect(draw, (cx, cy, cx + 520, cy + 46), radius=8, fill=(19, 27, 43), outline=BORDER_MUTED, width=1)
        draw.text((cx + 16, cy + 13), label, font=font_mono_bold, fill=col)
        val_x = cx + int(draw.textlength(label, font=font_mono_bold)) + 18
        draw.text((val_x, cy + 14), val, font=font_mono_xs, fill=TEXT_WHITE)
        cy += 56
        if cy > 430 and cx == 115:
            cx = 665
            cy = 365

    # Glowing Pulsing Call to Action Button
    pulse = 0.5 + 0.5 * math.sin(st * 6.0)
    btn_col = (0, int(210 + 45 * pulse), int(130 + 27 * pulse))
    draw_rounded_rect(draw, (115, 510, W - 115, 575), radius=10, fill=(15, 30, 38), outline=btn_col, width=2)
    btn_text = "[*] LET'S BUILD SOMETHING IMPACTFUL TOGETHER [*]"
    btw = int(draw.textlength(btn_text, font=font_mono_bold))
    draw.text(((W - btw) // 2, 532), btn_text, font=font_mono_bold, fill=btn_col)

def main():
    os.makedirs("assets", exist_ok=True)
    audio_path = "/tmp/showcase_audio.wav"
    mp4_path = "assets/profile-showcase.mp4"
    gif_path = "assets/profile-showcase.gif"
    
    print("Synthesizing audio soundtrack...")
    generate_audio_track(audio_path, DURATION)

    print(f"Rendering MP4 video ({TOTAL_FRAMES} frames @ {FPS} fps)...")
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", audio_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        mp4_path
    ]
    
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    
    for f in range(TOTAL_FRAMES):
        if f % 150 == 0:
            print(f"  Frame {f}/{TOTAL_FRAMES} ({f/TOTAL_FRAMES*100:.1f}%)")
        frame_img = render_frame(f)
        proc.stdin.write(frame_img.tobytes())
        
    proc.stdin.close()
    proc.wait()
    print(f"MP4 Video generated: {mp4_path} (return code: {proc.returncode})")

    print("Generating optimized animated GIF for GitHub README...")
    palette_path = "/tmp/palette.png"
    
    p1 = subprocess.run([
        "ffmpeg", "-y",
        "-i", mp4_path,
        "-vf", "fps=15,scale=800:-1:flags=lanczos,palettegen=max_colors=128",
        palette_path
    ], capture_output=True)
    
    p2 = subprocess.run([
        "ffmpeg", "-y",
        "-i", mp4_path,
        "-i", palette_path,
        "-lavfi", "fps=15,scale=800:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=3",
        gif_path
    ], capture_output=True)
    print(f"GIF generated: {gif_path} (return code: {p2.returncode})")
    
    if os.path.exists(mp4_path):
        print(f"MP4 File Size: {os.path.getsize(mp4_path) / 1024 / 1024:.2f} MB")
    if os.path.exists(gif_path):
        print(f"GIF File Size: {os.path.getsize(gif_path) / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    main()
