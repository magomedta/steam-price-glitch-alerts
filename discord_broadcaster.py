import os
import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Can store multiple comma-separated Discord webhook URLs
DISCORD_WEBHOOKS = [w.strip() for w in os.getenv("DISCORD_WEBHOOK_URL", "").split(",") if w.strip()]

def broadcast_to_discord(deal: dict) -> bool:
    """
    Broadcasts a price glitch / giveaway deal to configured Discord webhooks.
    Includes Telegram channel attribution.
    """
    if not DISCORD_WEBHOOKS:
        return False

    title = deal.get("title", "Game Deal")
    store = deal.get("store", "Store")
    normal_price = deal.get("normal_price", 0.0)
    sale_price = deal.get("sale_price", 0.0)
    savings = int(deal.get("savings", 100))
    url = deal.get("url", "")
    thumb = deal.get("thumb", "")

    price_text = f"~~${normal_price:.2f}~~ ➔ **FREE ($0.00)**" if sale_price == 0.0 else f"~~${normal_price:.2f}~~ ➔ **${sale_price:.2f}** (-{savings}%)"

    embed = {
        "title": f"🚨 PRICE GLITCH ({savings}% OFF): {title}",
        "url": url,
        "color": 0x00FFAA, # Cyber neon emerald
        "thumbnail": {"url": thumb} if thumb else None,
        "fields": [
            {"name": "Store", "value": store, "inline": True},
            {"name": "Price", "value": price_text, "inline": True},
            {"name": "Savings", "value": f"-{savings}%", "inline": True},
            {
                "name": "⚡ Instant 0-Second Alerts",
                "value": "[Join Telegram Channel @price_glitch_live](https://t.me/price_glitch_live)\n*Get notified before pricing errors are fixed!*",
                "inline": False
            }
        ],
        "footer": {
            "text": "Price Glitch Live Monitor | t.me/price_glitch_live",
            "icon_url": "https://raw.githubusercontent.com/magomedta/steam-price-glitch-alerts/main/channel_avatar.jpg"
        }
    }

    payload = {
        "username": "Price Glitch Alert",
        "avatar_url": "https://raw.githubusercontent.com/magomedta/steam-price-glitch-alerts/main/channel_avatar.jpg",
        "embeds": [embed]
    }

    success = True
    for webhook_url in DISCORD_WEBHOOKS:
        try:
            r = requests.post(webhook_url, json=payload, timeout=8)
            if r.status_code not in (200, 204):
                logging.warning(f"[Discord Webhook] Status {r.status_code}: {r.text[:100]}")
                success = False
        except Exception as e:
            logging.error(f"[Discord Webhook] Exception: {e}")
            success = False

    return success

if __name__ == "__main__":
    test_deal = {
        "title": "Test Glitch: Cyber Game 2077",
        "store": "Epic Games",
        "normal_price": 59.99,
        "sale_price": 0.00,
        "savings": 100,
        "url": "https://t.me/price_glitch_live",
        "thumb": ""
    }
    print("[*] Discord broadcaster initialized. Configured webhooks:", len(DISCORD_WEBHOOKS))
