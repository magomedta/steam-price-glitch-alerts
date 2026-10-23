import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

SITEMAP_URL = "https://magomedta.github.io/steam-price-glitch-alerts/sitemap.xml"
CHANNEL_URL = "https://t.me/price_glitch_live"

def ping_search_engines():
    """
    Pings search engine crawlers (Google, Bing) to index the live glitch monitor.
    """
    targets = [
        f"https://www.google.com/ping?sitemap={SITEMAP_URL}",
        f"https://www.bing.com/ping?sitemap={SITEMAP_URL}",
    ]

    for url in targets:
        try:
            resp = requests.get(url, timeout=10)
            logging.info(f"Pinged {url.split('?')[0]}: Status {resp.status_code}")
        except Exception as e:
            logging.warning(f"Failed pinging {url}: {e}")

def ping_telegram_directories():
    """
    Pings Telegram channel aggregators to accelerate channel discovery.
    """
    directories = [
        f"https://tgstat.com/channel/@price_glitch_live",
        f"https://telemetr.io/en/channels?search=price_glitch_live",
    ]
    for url in directories:
        try:
            resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            logging.info(f"Pinged Telegram directory {url}: Status {resp.status_code}")
        except Exception as e:
            logging.warning(f"Directory ping notice for {url}: {e}")

def run_indexing():
    logging.info("[*] Starting automated catalog & search indexing...")
    ping_search_engines()
    ping_telegram_directories()
    logging.info("[✔] Indexing pings finished.")

if __name__ == "__main__":
    run_indexing()
