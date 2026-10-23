import requests
import urllib.parse
import webbrowser
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

CHANNEL_USERNAME = "price_glitch_live"
CHANNEL_URL = "https://t.me/price_glitch_live"
WEB_TRACKER_URL = "https://magomedta.github.io/steam-price-glitch-alerts/"

CATALOGS = [
    {
        "name": "TGStat",
        "description": "Top Global Telegram Analytics & Directory",
        "url": f"https://tgstat.com/channel/@{CHANNEL_USERNAME}",
        "action": "Send '/add @price_glitch_live' to @tgstat_bot in Telegram."
    },
    {
        "name": "Telemetr",
        "description": "Leading Telegram Directory & Discovery Platform",
        "url": f"https://telemetr.io/en/channels?search={CHANNEL_USERNAME}",
        "action": "Direct search crawl indexing."
    },
    {
        "name": "Tlgrm.eu",
        "description": "Largest European & Russian Telegram Channels Catalog",
        "url": f"https://tlgrm.eu/channels/add",
        "action": "Free submit form: paste https://t.me/price_glitch_live"
    },
    {
        "name": "TelegramChannels.me",
        "description": "English Global Telegram Channel Index",
        "url": f"https://telegramchannels.me/add-channel",
        "action": "Free submission for gaming/deals category"
    },
    {
        "name": "ChannelCrawler",
        "description": "Automated Web Search Engine for Telegram",
        "url": f"https://channelcrawler.com/",
        "action": "Auto-crawls channels with public web mentions."
    }
]

def ping_directories():
    print("=" * 65)
    print(" 🚀 AUTOMATED TELEGRAM CHANNEL & WEB TRACKER SYNDICATION")
    print("=" * 65)
    for cat in CATALOGS:
        print(f"\n[+] {cat['name']} ({cat['description']})")
        print(f"    URL:    {cat['url']}")
        print(f"    Action: {cat['action']}")

    # Ping web indexing
    print("\n[*] Pinging web aggregator backlinks...")
    try:
        r = requests.get(f"https://api.hackertarget.com/pagelinks/?q={urllib.parse.quote(WEB_TRACKER_URL)}", timeout=10)
        print("    Backlink crawler pinged successfully.")
    except Exception as e:
        print(f"    Backlink notice: {e}")

if __name__ == "__main__":
    ping_directories()
