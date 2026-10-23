import os
import asyncio
import requests
import subprocess
from PIL import Image, ImageDraw, ImageFont
import edge_tts

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "shorts_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def generate_voiceover(text: str, voice: str, output_path: str):
    """
    Generates high-quality AI voiceover using edge-tts.
    """
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def create_short_poster(deal: dict, poster_path: str):
    """
    Generates a 1080x1920 vertical poster for TikTok / YouTube Shorts.
    """
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), color="#090a10")
    draw = ImageDraw.Draw(img)

    # Gradient-like background accents
    for y in range(height):
        ratio = y / height
        r = int(9 + 15 * ratio)
        g = int(10 + 20 * (1 - ratio))
        b = int(16 + 30 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Try loading default system fonts or fallback
    try:
        font_huge = ImageFont.truetype("arialbd.ttf", 68)
        font_large = ImageFont.truetype("arialbd.ttf", 52)
        font_med = ImageFont.truetype("arial.ttf", 40)
        font_bold = ImageFont.truetype("arialbd.ttf", 44)
    except IOError:
        font_huge = ImageFont.load_default()
        font_large = ImageFont.load_default()
        font_med = ImageFont.load_default()
        font_bold = ImageFont.load_default()

    # 1. Top Header Badge
    draw.rounded_rectangle([80, 120, 1000, 240], radius=30, fill="#111827", outline="#00ffaa", width=4)
    draw.text((540, 180), "🚨 PRICING GLITCH ALERT!", font=font_huge, fill="#00ffaa", anchor="mm")

    # 2. Store Tag
    store = deal.get("store", "Steam / Epic Games")
    draw.text((540, 310), f"STORE: {store.upper()}", font=font_med, fill="#94a3b8", anchor="mm")

    # 3. Game Thumbnail (Centered)
    thumb_url = deal.get("thumb")
    thumb_box = [80, 390, 1000, 950]
    draw.rounded_rectangle(thumb_box, radius=25, fill="#1e293b", outline="#38bdf8", width=3)
    
    if thumb_url:
        try:
            resp = requests.get(thumb_url, timeout=6)
            if resp.status_code == 200:
                from io import BytesIO
                thumb_img = Image.open(BytesIO(resp.content)).convert("RGB")
                thumb_img = thumb_img.resize((920, 560), Image.Resampling.LANCZOS)
                img.paste(thumb_img, (80, 390))
        except Exception as e:
            print(f"Could not download thumb: {e}")

    # 4. Title
    title = deal.get("title", "Game Title")
    if len(title) > 30:
        title = title[:28] + "..."
    draw.text((540, 1030), title, font=font_large, fill="#ffffff", anchor="mm")

    # 5. Price Section
    normal_price = deal.get("normal_price", 29.99)
    sale_price = deal.get("sale_price", 0.0)
    savings = int(deal.get("savings", 100))

    draw.rounded_rectangle([80, 1120, 1000, 1400], radius=30, fill="#0f172a", outline="#f59e0b", width=3)
    draw.text((540, 1190), f"NORMAL PRICE: ${normal_price:.2f}", font=font_med, fill="#94a3b8", anchor="mm")
    
    if sale_price == 0.0:
        draw.text((540, 1280), "🔥 100% FREE ($0.00)", font=font_huge, fill="#22c55e", anchor="mm")
    else:
        draw.text((540, 1280), f"🔥 NOW: ${sale_price:.2f} (-{savings}%)", font=font_huge, fill="#22c55e", anchor="mm")

    draw.text((540, 1350), "⚡ HURRY! Mistake will be fixed soon!", font=font_med, fill="#fbbf24", anchor="mm")

    # 6. Bottom CTA (Telegram Channel)
    draw.rounded_rectangle([80, 1500, 1000, 1750], radius=35, fill="#0284c7", outline="#ffffff", width=4)
    draw.text((540, 1580), "👉 CLAIM IN TELEGRAM:", font=font_bold, fill="#ffffff", anchor="mm")
    draw.text((540, 1660), "@price_glitch_live", font=font_huge, fill="#ffffff", anchor="mm")
    draw.text((540, 1820), "Link in bio / description to get direct game link", font=font_med, fill="#64748b", anchor="mm")

    img.save(poster_path)

def render_short_video(deal: dict, output_filename: str = None) -> str:
    """
    Renders a complete vertical 9:16 video clip with AI voiceover.
    """
    title = deal.get("title", "Free Game")
    normal_price = deal.get("normal_price", 29.99)
    clean_name = "".join(c for c in title if c.isalnum() or c in (" ", "_")).rstrip().replace(" ", "_")
    if not output_filename:
        output_filename = f"short_{clean_name}.mp4"

    poster_path = os.path.join(OUTPUT_DIR, f"poster_{clean_name}.png")
    audio_path = os.path.join(OUTPUT_DIR, f"voice_{clean_name}.mp3")
    final_video = os.path.join(OUTPUT_DIR, output_filename)

    # 1. Create poster image
    create_short_poster(deal, poster_path)

    # 2. Generate voiceover text
    script = (
        f"Gamer alert! Steam and publishers just made a massive pricing error! "
        f"{title}, which normally costs {int(normal_price)} dollars, is currently one hundred percent free! "
        f"Grab it right now before store admins patch it! "
        f"Link is in our Telegram channel, price glitch live! Link in bio!"
    )
    asyncio.run(generate_voiceover(script, "en-US-ChristopherNeural", audio_path))

    # 3. Use ffmpeg to combine image and voiceover into 9:16 vertical MP4
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", poster_path,
        "-i", audio_path,
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        final_video
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    print(f"[✔] Short Video Rendered: {final_video}")
    return final_video

if __name__ == "__main__":
    sample_deal = {
        "title": "Sker Ritual",
        "store": "Steam / Epic Games",
        "normal_price": 24.99,
        "sale_price": 0.00,
        "savings": 100,
        "thumb": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1492070/1e25b8656ab9ed661c6f6a7a1dc2e78f290263fa/capsule_231x87.jpg"
    }
    render_short_video(sample_deal)
