import requests
import json
import logging
import urllib.parse
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

def format_glitch_message(deal: dict) -> str:
    """
    Constructs high-converting, bilingual alert text (English primary + Russian secondary).
    """
    title = deal.get("title")
    store = deal.get("store")
    normal_price = deal.get("normal_price")
    sale_price = deal.get("sale_price")
    savings = deal.get("savings")
    url = deal.get("url")

    if sale_price == 0.0:
        price_en = f"💰 Normal Price: <s>${normal_price:.2f}</s>\n🔥 <b>Glitch Price: FREE ($0.00)</b>"
        discount_badge_en = "100% FREE"
        discount_badge_ru = "100% ХАЛЯВА"
    else:
        price_en = f"💰 Was: <s>${normal_price:.2f}</s>\n🔥 <b>Now: ${sale_price:.2f}</b>"
        discount_badge_en = f"-{int(savings)}% OFF"
        discount_badge_ru = f"СКИДКА -{int(savings)}%"

    message = (
        f"🚨 <b>PRICE GLITCH DETECTED! ({discount_badge_en})</b>\n"
        f"🇷🇺 <i>Баг цены / {discount_badge_ru}</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📦 <b>{title}</b>\n"
        f"🏪 Store / Магазин: <b>{store}</b>\n\n"
        f"{price_en}\n"
        f"⚡ Discount / Скидка: <b>{discount_badge_en}</b>\n\n"
        f"⏳ <i>Status: ACTIVE (Hurry, price error will be patched!)</i>\n"
        f"⏳ <i>Успейте забрать, пока ошибку цен не исправили!</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👉 <a href='{url}'><b>[ 🛒 CLAIM DEAL / ЗАБРАТЬ ]</b></a>\n\n"
        f"⚡ <b>Feed / Канал:</b> @price_glitch_live | 🔔 <i>Turn ON / Включите 🔔</i>"
    )
    return message

def publish_to_telegram(deal: dict) -> bool:
    """
    Sends the formatted glitch alert with photo directly to the designated Telegram Channel.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
        # Simulation / Console Mode
        print(f"\n[DEMO ALERT] Would post to Telegram: {deal.get('title')} (-{deal.get('savings')}%)")
        return True

    text = format_glitch_message(deal)
    thumb = deal.get("thumb")
    title = deal.get("title", "Game Deal")
    savings = int(deal.get("savings", 100))
    share_text = urllib.parse.quote(f"🔥 Price Glitch / Баг цены: {title} (-{savings}%)! Заходи в канал с моментальными оповещениями:")
    share_url = f"https://t.me/share/url?url=https://t.me/price_glitch_live&text={share_text}"

    inline_keyboard = {
        "inline_keyboard": [
            [
                {"text": f"🛒 BUY / ЗАБРАТЬ (-{savings}%)", "url": deal.get("url")}
            ],
            [
                {"text": "📢 Share / Поделиться (+Invite)", "url": share_url},
                {"text": "⚡ Join / Подписаться", "url": "https://t.me/price_glitch_live"}
            ]
        ]
    }

    # 1. Try sending with photo first
    posted_successfully = False
    if thumb:
        photo_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        photo_payload = {
            "chat_id": TELEGRAM_CHANNEL_ID,
            "photo": thumb,
            "caption": text,
            "parse_mode": "HTML",
            "reply_markup": json.dumps(inline_keyboard)
        }
        try:
            resp = requests.post(photo_url, json=photo_payload, timeout=12)
            if resp.status_code == 200 and resp.json().get("ok"):
                posted_successfully = True
            else:
                logging.warning(f"[Telegram Photo] sendPhoto failed: {resp.text[:120]}, falling back to text...")
        except Exception as e:
            logging.warning(f"[Telegram Photo] Exception: {e}, falling back to text...")

    # 2. Fallback to standard text message if no photo or photo failed
    if not posted_successfully:
        msg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        msg_payload = {
            "chat_id": TELEGRAM_CHANNEL_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
            "reply_markup": json.dumps(inline_keyboard)
        }
        try:
            resp = requests.post(msg_url, json=msg_payload, timeout=10)
            if resp.status_code == 200 and resp.json().get("ok"):
                posted_successfully = True
            else:
                logging.error(f"[Telegram] Failed to send message: {resp.text}")
        except Exception as e:
            logging.error(f"[Telegram] Exception sending message: {e}")

    # Also broadcast to Discord if configured
    try:
        from discord_broadcaster import broadcast_to_discord
        broadcast_to_discord(deal)
    except Exception:
        pass

    return posted_successfully
