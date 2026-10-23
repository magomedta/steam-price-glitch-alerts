import os
import urllib.parse
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def format_reddit_post(deal: Dict) -> Dict[str, str]:
    """
    Formats a deal strictly according to r/FreeGameFindings and r/freegames guidelines.
    Example: [Steam] (Game) Space Crew: Legendary Edition - 100% OFF
    """
    title = deal.get("title", "Game")
    store = deal.get("store", "PC")
    savings = int(deal.get("savings", 100))
    url = deal.get("url", "")
    normal_price = deal.get("normal_price", 0.0)

    # Format subreddit title standard
    if savings == 100:
        reddit_title = f"[{store}] (Game) {title} - 100% OFF (Free to keep)"
    else:
        reddit_title = f"[{store}] (Game) {title} (-{savings}% / Was ${normal_price:.2f})"

    body = (
        f"**Deal:** {title}\n"
        f"**Store:** {store}\n"
        f"**Discount:** {savings}%\n"
        f"**Store Link:** [Claim Deal Here]({url})\n\n"
        f"---\n"
        f"*⚡ Instant 0-second push alerts for pricing errors & free games:* [Telegram Feed](https://t.me/price_glitch_live)"
    )

    # 1-Click web submission URLs
    r_freegames_url = (
        f"https://www.reddit.com/r/freegames/submit?"
        f"title={urllib.parse.quote(reddit_title)}&url={urllib.parse.quote(url)}"
    )
    r_fgf_url = (
        f"https://www.reddit.com/r/FreeGameFindings/submit?"
        f"title={urllib.parse.quote(reddit_title)}&url={urllib.parse.quote(url)}"
    )

    return {
        "title": reddit_title,
        "body": body,
        "url": url,
        "submit_r_freegames": r_freegames_url,
        "submit_r_freegamefindings": r_fgf_url
    }

def print_reddit_formats(deals: List[Dict]):
    """
    Utility to display formatted reddit posts for manual or automated syndication.
    """
    for deal in deals[:5]:
        formatted = format_reddit_post(deal)
        print("="*60)
        print(f"TITLE: {formatted['title']}")
        print(f"SUBMIT r/freegames: {formatted['submit_r_freegames']}")
        print("="*60)

if __name__ == "__main__":
    from scrapers.gamerpower import fetch_gamerpower_glitches
    deals = fetch_gamerpower_glitches()
    print_reddit_formats(deals)
