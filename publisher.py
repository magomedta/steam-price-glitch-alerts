import requests
import json
import logging
import urllib.parse
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

def format_glitch_message(deal: dict) -> str:
    """
    Constructs high-converting, viral English alert text for Telegram.
    """
    title = deal.get("title")
    store = deal.get("store")
    normal_price = deal.get("normal_price")
    sale_price = deal.get("sale_price")
    savings = deal.get("savings")
    url = deal.get("url")

    if sale_price == 0.0:
        price_line = f"💰 Normal Price: <s>${normal_price:.2f}</s>\n🔥 <b>Glitch Price: FREE ($0.00)</b>"
        discount_badge = "100% FREE"
    else:
        price_line = f"💰 Was: <s>${normal_price:.2f}</s>\n🔥 <b>Now: ${sale_price:.2f}</b>"
        discount_badge = f"-{int(savings)}% OFF"

    message = (
        f"🚨 <b>PRICE GLITCH DETECTED! ({discount_badge})</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📦 <b>{title}</b>\n"
        f"🏪 Store: <b>{store}</b>\n\n"
        f"{price_line}\n"
        f"⚡ Discount: <b>{discount_badge}</b>\n\n"
        f"⏳ <i>Status: ACTIVE (Price error may be fixed anytime!)</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👉 <a href='{url}'><b>[ 🛒 CLAIM DEAL / BUY NOW ]</b></a>\n\n"
        f"⚡ <b>Feed:</b> @price_glitch_live | 🔔 <i>Turn notifications ON!</i>"
    )
    return message

def publish_to_telegram(deal: dict) -> bool:
    """
    Sends the formatted glitch alert directly to the designated Telegram Channel.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
        # Simulation / Console Mode
        print(f"\n[DEMO ALERT] Would post to Telegram: {deal.get('title')} (-{deal.get('savings')}%)")
        return True

    text = format_glitch_message(deal)
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    title = deal.get("title", "Game Deal")
    savings = int(deal.get("savings", 100))
    share_text = urllib.parse.quote(f"🔥 Price Glitch Alert: {title} is {savings}% OFF! Join the live alert channel before it expires:")
    share_url = f"https://t.me/share/url?url=https://t.me/price_glitch_live&text={share_text}"

    inline_keyboard = {
        "inline_keyboard": [
            [
                {"text": f"🛒 CLAIM DEAL (-{savings}%)", "url": deal.get("url")}
            ],
            [
                {"text": "📢 Share Deal (+Invite)", "url": share_url},
                {"text": "⚡ Join Live Alerts", "url": "https://t.me/price_glitch_live"}
            ]
        ]
    }

    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
        "reply_markup": json.dumps(inline_keyboard)
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            return True
        else:
            logging.error(f"[Telegram] Failed to send message: {resp.text}")
            return False
    except Exception as e:
        logging.error(f"[Telegram] Exception sending message: {e}")
        return False
