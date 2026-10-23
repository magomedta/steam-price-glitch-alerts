import os
import asyncio
import subprocess
import math
import wave
import struct
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import edge_tts

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "shorts_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Sound Generator Helper Functions
def generate_chime(output_path: str):
    """Generates an iOS/Telegram-style notification bell chime."""
    f = wave.open(output_path, 'w')
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(44100)
    dur = 0.5
    total = int(44100 * dur)
    data = []
    for i in range(total):
        t = i / 44100
        # Dual frequency bell (1046.5Hz and 1318.5Hz - C6 and E6 harmonic)
        val = (0.7 * math.sin(2 * math.pi * 1046.5 * t) + 0.3 * math.sin(2 * math.pi * 1318.5 * t)) * math.exp(-7 * t)
        data.append(int(18000 * val))
    f.writeframes(struct.pack('<' + 'h' * len(data), *data))
    f.close()

def generate_bg_beat(output_path: str, duration: float = 12.0):
    """Generates a rhythmic cyberpunk electronic background track."""
    f = wave.open(output_path, 'w')
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(44100)
    total = int(44100 * duration)
    data = []
    for i in range(total):
        t = i / 44100
        # 128 BPM Kick (every 0.46875s)
        beat_t = t % 0.46875
        kick = math.sin(2 * math.pi * 55 * math.exp(-18 * beat_t) * beat_t) * math.exp(-14 * beat_t) if beat_t < 0.22 else 0
        # Bass pulse
        bass_freq = 65.4 if (int(t * 2.133) % 4 < 2) else 49.0
        bass = 0.35 * math.sin(2 * math.pi * bass_freq * t) + 0.15 * math.sin(2 * math.pi * bass_freq * 2 * t)
        # Hi-hat on 16th notes
        hat_t = t % 0.117
        hat = (0.12 * (math.sin(i * 987.65 % 1) - 0.5) * math.exp(-50 * hat_t)) if hat_t < 0.05 else 0
        
        sample = int(7000 * (kick * 0.7 + bass * 0.25 + hat * 0.12))
        data.append(max(-32767, min(32767, sample)))
    f.writeframes(struct.pack('<' + 'h' * len(data), *data))
    f.close()

async def generate_voice(text: str, voice: str, output_path: str, rate: str = "+12%"):
    """Generates high-energy speech using edge-tts."""
    comm = edge_tts.Communicate(text, voice, rate=rate)
    await comm.save(output_path)

# 2. Scene Image Renderers
def get_fonts():
    try:
        return {
            "title": ImageFont.truetype("arialbd.ttf", 64),
            "h1": ImageFont.truetype("arialbd.ttf", 52),
            "h2": ImageFont.truetype("arialbd.ttf", 44),
            "body": ImageFont.truetype("arial.ttf", 36),
            "bold": ImageFont.truetype("arialbd.ttf", 38),
            "small": ImageFont.truetype("arial.ttf", 28)
        }
    except IOError:
        df = ImageFont.load_default()
        return {"title": df, "h1": df, "h2": df, "body": df, "bold": df, "small": df}

def draw_cyber_bg(img: Image.Image):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for y in range(h):
        ratio = y / h
        r = int(6 + 14 * ratio)
        g = int(8 + 18 * (1 - ratio))
        b = int(14 + 28 * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    # Subtle cyber grid
    for x in range(0, w, 80):
        draw.line([(x, 0), (x, h)], fill=(20, 28, 45, 40))
    for y in range(0, h, 80):
        draw.line([(0, y), (w, y)], fill=(20, 28, 45, 40))

def render_scene_1(deal: dict, output_path: str):
    """Scene 1: Hook + Phone Notification Pop-up."""
    w, h = 1080, 1920
    img = Image.new("RGB", (w, h))
    draw_cyber_bg(img)
    draw = ImageDraw.Draw(img)
    f = get_fonts()

    # Top Warning Pill
    draw.rounded_rectangle([200, 140, 880, 220], radius=40, fill="#7f1d1d", outline="#ef4444", width=3)
    draw.text((540, 180), "⚠️ URGENT GAMING ALERT", font=f["h2"], fill="#fecaca", anchor="mm")

    # Big Hook
    draw.text((540, 310), "STOP SCROLLING!", font=f["title"], fill="#ffffff", anchor="mm")
    draw.text((540, 390), "STEAM PRICING ERROR ACTIVE", font=f["h1"], fill="#facc15", anchor="mm")

    # iPhone / Telegram Floating Notification Card (Frosted Glass style)
    card_box = [60, 520, 1020, 840]
    draw.rounded_rectangle(card_box, radius=35, fill="#111827", outline="#00ffaa", width=4)

    # App Header inside card
    draw.ellipse([100, 560, 145, 605], fill="#0284c7")
    draw.text((122, 582), "⚡", font=f["h2"], fill="#ffffff", anchor="mm")
    draw.text((165, 582), "TELEGRAM • Price Glitch Live • now", font=f["small"], fill="#94a3b8", anchor="lm")

    # Notification Body
    title = deal.get("title", "Game")
    normal_price = deal.get("normal_price", 29.99)
    draw.text((100, 660), f"🚨 100% OFF: {title}", font=f["h1"], fill="#ffffff", anchor="lm")
    draw.text((100, 740), f"Price error detected! Normal price was ${normal_price:.2f}.", font=f["body"], fill="#38bdf8", anchor="lm")
    draw.text((100, 785), "Status: 100% FREE ($0.00). Tap to claim now!", font=f["bold"], fill="#22c55e", anchor="lm")

    # Game Artwork in Scene 1 Preview
    thumb_url = deal.get("thumb")
    if thumb_url:
        try:
            r = requests.get(thumb_url, timeout=5)
            if r.status_code == 200:
                t_img = Image.open(BytesIO(r.content)).convert("RGB")
                t_img = t_img.resize((920, 520), Image.Resampling.LANCZOS)
                draw.rounded_rectangle([75, 920, 1005, 1450], radius=25, fill="#0f172a", outline="#3b82f6", width=3)
                img.paste(t_img, (80, 925))
        except Exception:
            pass

    # Bottom Teaser
    draw.rounded_rectangle([150, 1560, 930, 1720], radius=30, fill="#0f172a", outline="#e2e8f0", width=2)
    draw.text((540, 1615), "👇 HOW TO CLAIM BEFORE PATCH 👇", font=f["h2"], fill="#ffffff", anchor="mm")
    draw.text((540, 1675), "Publisher fixes errors in minutes!", font=f["small"], fill="#f87171", anchor="mm")

    img.save(output_path)

def render_scene_2(deal: dict, output_path: str):
    """Scene 2: Proof & Deal Value Breakdown."""
    w, h = 1080, 1920
    img = Image.new("RGB", (w, h))
    draw_cyber_bg(img)
    draw = ImageDraw.Draw(img)
    f = get_fonts()

    # Top Badge
    draw.rounded_rectangle([140, 130, 940, 220], radius=45, fill="#064e3b", outline="#10b981", width=3)
    draw.text((540, 175), "🔥 VERIFIED PRICE GLITCH", font=f["h1"], fill="#6ee7b7", anchor="mm")

    # Title & Store
    title = deal.get("title", "Game Title")
    store = deal.get("store", "Steam Store")
    draw.text((540, 290), title, font=f["title"], fill="#ffffff", anchor="mm")
    draw.text((540, 360), f"STORE: {store.upper()} (OFFICIAL)", font=f["body"], fill="#38bdf8", anchor="mm")

    # Big Artwork
    thumb_url = deal.get("thumb")
    if thumb_url:
        try:
            r = requests.get(thumb_url, timeout=5)
            if r.status_code == 200:
                t_img = Image.open(BytesIO(r.content)).convert("RGB")
                t_img = t_img.resize((960, 560), Image.Resampling.LANCZOS)
                draw.rounded_rectangle([55, 420, 1025, 990], radius=30, fill="#0f172a", outline="#10b981", width=4)
                img.paste(t_img, (60, 425))
        except Exception:
            pass

    # Price Slashing Box
    normal_price = deal.get("normal_price", 29.99)
    sale_price = deal.get("sale_price", 0.0)
    savings = int(deal.get("savings", 100))

    draw.rounded_rectangle([80, 1050, 1000, 1370], radius=35, fill="#0f172a", outline="#f59e0b", width=3)
    draw.text((540, 1120), f"NORMAL STORE PRICE: ${normal_price:.2f}", font=f["h2"], fill="#94a3b8", anchor="mm")
    
    # Red Strikethrough line over normal price
    draw.line([(240, 1120), (840, 1120)], fill="#ef4444", width=6)

    # Glitch Price
    if sale_price == 0.0:
        draw.text((540, 1220), "GLITCH PRICE: $0.00 (100% FREE)", font=f["title"], fill="#22c55e", anchor="mm")
    else:
        draw.text((540, 1220), f"GLITCH PRICE: ${sale_price:.2f} (-{savings}%)", font=f["title"], fill="#22c55e", anchor="mm")
    
    draw.text((540, 1305), "✅ Permanent License Added to Library", font=f["body"], fill="#cbd5e1", anchor="mm")

    # Urgency Meter
    draw.rounded_rectangle([80, 1440, 1000, 1620], radius=30, fill="#1e1b4b", outline="#818cf8", width=3)
    draw.text((540, 1500), "⚡ Over 2,400 gamers claimed today!", font=f["h2"], fill="#ffffff", anchor="mm")
    draw.text((540, 1560), "Hurry, publisher is rolling out a patch!", font=f["body"], fill="#f43f5e", anchor="mm")

    img.save(output_path)

def render_scene_3(deal: dict, output_path: str):
    """Scene 3: Telegram CTA & Channel Mockup."""
    w, h = 1080, 1920
    img = Image.new("RGB", (w, h))
    draw_cyber_bg(img)
    draw = ImageDraw.Draw(img)
    f = get_fonts()

    # Header
    draw.text((540, 180), "WHERE TO GET DIRECT LINK:", font=f["h1"], fill="#38bdf8", anchor="mm")

    # Telegram Channel Card Mockup
    card_box = [80, 260, 1000, 920]
    draw.rounded_rectangle(card_box, radius=40, fill="#0f172a", outline="#0284c7", width=4)

    # Avatar & Title inside mockup
    draw.ellipse([140, 310, 240, 410], fill="#0284c7")
    draw.text((190, 360), "⚡", font=f["title"], fill="#ffffff", anchor="mm")

    draw.text((270, 340), "Price Glitch Live", font=f["h1"], fill="#ffffff", anchor="lm")
    draw.text((270, 390), "@price_glitch_live • 24/7 Bot Alerts", font=f["small"], fill="#38bdf8", anchor="lm")

    # Channel Description inside mockup
    draw.line([(120, 440), (960, 440)], fill="#334155", width=2)
    desc_lines = [
        "🚨 24/7 Autonomous Scanner for 85%-100% pricing errors",
        "🏪 Monitoring Steam, Epic Games, GOG, Humble Store",
        "🔔 Push notifications delivered 0 seconds after glitch drops"
    ]
    for i, line in enumerate(desc_lines):
        draw.text((130, 490 + i * 55), line, font=f["body"], fill="#cbd5e1", anchor="lm")

    # Mockup Buy Button
    draw.rounded_rectangle([130, 710, 950, 830], radius=25, fill="#0284c7")
    draw.text((540, 770), "🛒 CLAIM DEAL (100% FREE) &rarr;", font=f["h2"], fill="#ffffff", anchor="mm")

    # Big Neon Glowing Call To Action Section
    cta_box = [60, 1040, 1020, 1420]
    draw.rounded_rectangle(cta_box, radius=40, fill="#042f2e", outline="#00ffaa", width=5)

    draw.text((540, 1120), "👉 LINK IS IN MY BIO / PROFILE!", font=f["title"], fill="#ffffff", anchor="mm")
    draw.text((540, 1220), "t.me/price_glitch_live", font=f["title"], fill="#00ffaa", anchor="mm")
    draw.text((540, 1320), "Open Telegram & Search: @price_glitch_live", font=f["body"], fill="#99f6e4", anchor="mm")

    # Bottom Reminder
    draw.rounded_rectangle([100, 1530, 980, 1720], radius=30, fill="#111827", outline="#475569", width=2)
    draw.text((540, 1590), "🇷🇺 Ссылка на халяву в шапке профиля!", font=f["h2"], fill="#facc15", anchor="mm")
    draw.text((540, 1660), "Включите 🔔 чтобы не пропустить следующий баг!", font=f["small"], fill="#94a3b8", anchor="mm")

    img.save(output_path)

def produce_commercial_promo_video(deal: dict, output_filename: str = "viral_promo_ad.mp4") -> str:
    """
    Renders a multi-scene, broadcast-quality vertical promo video with voiceover,
    sound effects (notification chime), and electronic beat.
    """
    title = deal.get("title", "Sker Ritual")
    normal_price = int(deal.get("normal_price", 25))

    s1_img = os.path.join(OUTPUT_DIR, "scene1.png")
    s2_img = os.path.join(OUTPUT_DIR, "scene2.png")
    s3_img = os.path.join(OUTPUT_DIR, "scene3.png")
    
    render_scene_1(deal, s1_img)
    render_scene_2(deal, s2_img)
    render_scene_3(deal, s3_img)

    chime_path = os.path.join(OUTPUT_DIR, "chime.wav")
    bg_beat_path = os.path.join(OUTPUT_DIR, "bg_beat.wav")
    voice_path = os.path.join(OUTPUT_DIR, "ad_voiceover.mp3")
    final_video = os.path.join(OUTPUT_DIR, output_filename)

    # 1. Generate SFX & Beat
    generate_chime(chime_path)
    generate_bg_beat(bg_beat_path, duration=11.5)

    # 2. High-energy TikTok-style voiceover script
    script = (
        f"Wait, stop scrolling! Steam publishers just made a massive pricing error! "
        f"{title}, which normally costs {normal_price} dollars, is literally zero dollars right now! "
        f"Thousands of gamers are claiming it before store admins fix the price. "
        f"Our 24/7 bot caught it within seconds. Tap the link in my bio to claim it now in Telegram, at price glitch live!"
    )
    asyncio.run(generate_voice(script, "en-US-ChristopherNeural", voice_path, rate="+14%"))

    # 3. Create Scene video clips using ffmpeg with smooth zoom/motion
    # Scene 1: 3.2s
    # Scene 2: 4.2s
    # Scene 3: 4.1s
    s1_vid = os.path.join(OUTPUT_DIR, "s1.mp4")
    s2_vid = os.path.join(OUTPUT_DIR, "s2.mp4")
    s3_vid = os.path.join(OUTPUT_DIR, "s3.mp4")

    # Render s1
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", s1_img,
        "-t", "3.2", "-r", "30", "-pix_fmt", "yuv420p",
        "-vf", "scale=1080:1920", s1_vid
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Render s2
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", s2_img,
        "-t", "4.2", "-r", "30", "-pix_fmt", "yuv420p",
        "-vf", "scale=1080:1920", s2_vid
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Render s3
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", s3_img,
        "-t", "4.1", "-r", "30", "-pix_fmt", "yuv420p",
        "-vf", "scale=1080:1920", s3_vid
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Concat scenes
    concat_txt = os.path.join(OUTPUT_DIR, "concat.txt")
    with open(concat_txt, "w") as f:
        f.write(f"file '{s1_vid.replace(os.sep, '/')}'\n")
        f.write(f"file '{s2_vid.replace(os.sep, '/')}'\n")
        f.write(f"file '{s3_vid.replace(os.sep, '/')}'\n")

    video_only = os.path.join(OUTPUT_DIR, "video_merged.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-c", "copy", video_only
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Audio Mix:
    # - Chime at t=0.6s
    # - Voiceover at t=0.2s
    # - BG beat at 25% volume
    mixed_audio = os.path.join(OUTPUT_DIR, "mixed_audio.wav")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", bg_beat_path,
        "-i", voice_path,
        "-i", chime_path,
        "-filter_complex",
        "[0:a]volume=0.22[bg];[1:a]adelay=200|200,volume=1.0[voice];[2:a]adelay=650|650,volume=0.9[chime];[bg][voice][chime]amix=inputs=3:duration=shortest[aout]",
        "-map", "[aout]",
        mixed_audio
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Combine video + mixed audio into final video
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_only,
        "-i", mixed_audio,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        final_video
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    print(f"[✔] VIRAL COMMERCIAL PROMO CREATED: {final_video}")
    return final_video

if __name__ == "__main__":
    sample_deal = {
        "title": "Sker Ritual",
        "store": "Steam Store",
        "normal_price": 24.99,
        "sale_price": 0.00,
        "savings": 100,
        "thumb": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1492070/1e25b8656ab9ed661c6f6a7a1dc2e78f290263fa/capsule_231x87.jpg"
    }
    produce_commercial_promo_video(sample_deal)
