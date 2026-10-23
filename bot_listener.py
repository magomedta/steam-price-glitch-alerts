import time
import requests
import logging
from config import TELEGRAM_BOT_TOKEN

def start_bot_polling():
    """
    Polls for /start commands sent directly to the bot and redirects them to the channel.
    Runs in a background thread without blocking.
    """
    if not TELEGRAM_BOT_TOKEN:
        return

    last_update_id = 0
    logging.info("[Bot Listener] Starting Telegram interaction listener...")

    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
            params = {"offset": last_update_id + 1, "timeout": 20}
            resp = requests.get(url, params=params, timeout=25)

            if resp.status_code == 200:
                data = resp.json()
                for update in data.get("result", []):
                    last_update_id = update["update_id"]
                    message = update.get("message")
                    if message and "chat" in message:
                        chat_id = message["chat"]["id"]
                        text = message.get("text", "")

                        if text.startswith("/start"):
                            reply_text = (
                                "⚡ <b>Welcome to Price Glitch & Freebies Alert!</b>\n"
                                "We scan 35+ global digital stores (Steam, Epic Games, GOG, Humble Store) "
                                "every 30 seconds for <b>85% - 100% pricing errors and free giveaways</b>.\n\n"
                                "🇷🇺 <b>Добро пожаловать в Price Glitch Live!</b>\n"
                                "Мы отслеживаем 35+ игровых магазинов в реальном времени. "
                                "Узнавайте о <b>багах цен и 100% халяве</b> первыми до фикса!\n\n"
                                "👉 <b>Join our live feed / Подписаться на канал:</b>\n"
                                "📢 @price_glitch_live"
                            )
                            reply_keyboard = {
                                "inline_keyboard": [
                                    [{"text": "⚡ OPEN CHANNEL / КАНАЛ", "url": "https://t.me/price_glitch_live"}],
                                    [{"text": "📢 Share / Поделиться", "url": "https://t.me/share/url?url=https://t.me/price_glitch_live&text=Price%20Glitches%20&%20Баги%20цен%20в%20Steam!"}]
                                ]
                            }
                            send_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                            requests.post(send_url, json={
                                "chat_id": chat_id,
                                "text": reply_text,
                                "parse_mode": "HTML",
                                "reply_markup": reply_keyboard
                            }, timeout=10)

        except Exception as e:
            # Silent backoff on transient network issues
            time.sleep(5)
            continue

        time.sleep(1)
