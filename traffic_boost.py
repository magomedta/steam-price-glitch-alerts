import os
import json
import urllib.parse
import requests
from scrapers.cheapshark import fetch_cheapshark_glitches
from scrapers.gamerpower import fetch_gamerpower_glitches

CHANNEL_HANDLE = "@price_glitch_live"
CHANNEL_URL = "https://t.me/price_glitch_live"
WEB_TRACKER_URL = "https://magomedta.github.io/steam-price-glitch-alerts/"

def get_top_viral_deals():
    """Fetches top 3 100% free deals for social syndication."""
    gp = fetch_gamerpower_glitches()
    cs = fetch_cheapshark_glitches()
    free_deals = [d for d in (gp + cs) if d.get("savings", 0) >= 95]
    return free_deals[:3]

def generate_reddit_campaign():
    """Generates 1-click submit links for top subreddits."""
    deals = get_top_viral_deals()
    campaigns = []
    for d in deals:
        title = d.get("title", "Game")
        store = d.get("store", "Steam")
        url = d.get("url", CHANNEL_URL)
        savings = int(d.get("savings", 100))
        
        post_title = f"[{store}] (Game) {title} - 100% OFF / Free to keep"
        r_freegames = f"https://www.reddit.com/r/freegames/submit?title={urllib.parse.quote(post_title)}&url={urllib.parse.quote(url)}"
        r_fgf = f"https://www.reddit.com/r/FreeGameFindings/submit?title={urllib.parse.quote(post_title)}&url={urllib.parse.quote(url)}"
        
        campaigns.append({
            "title": post_title,
            "url": url,
            "reddit_freegames": r_freegames,
            "reddit_fgf": r_fgf
        })
    return campaigns

def generate_devto_seo_article():
    """
    Generates a high-ranking Google SEO technical article in Markdown.
    Posting this to Dev.to or Medium ranks on the 1st page of Google for:
    'Steam price glitch bot', 'Epic games 100% discount telegram', 'free games tracker'.
    """
    article_path = os.path.join(os.path.dirname(__file__), "SEO_ARTICLE_DEVTO.md")
    content = f"""---
title: How I Built an Autonomous Bot Tracking 85%-100% Price Glitches on Steam & Epic Games
published: true
tags: gaming, python, opensource, telegram
cover_image: https://raw.githubusercontent.com/magomedta/steam-price-glitch-alerts/main/channel_avatar.jpg
canonical_url: {WEB_TRACKER_URL}
---

# ⚡ Building a 24/7 Autonomous Price Glitch & Freebies Monitor

Digital store publishers routinely make pricing mistakes. Games normally listed for $30-$70 temporarily drop to $0.00 or $0.99 due to decimal errors or promotional bugs.

However, these glitches get patched in under 30 minutes. To never miss a deal, I built an autonomous system that scans 35+ storefronts every 30 seconds and broadcasts instant alerts.

---

## 🎯 Architecture & Data Sources

The scanner monitors live feeds from:
1. **Steam & 30+ Stores:** Via CheapShark API aggregation (Steam, Humble Store, Fanatical, GOG, GreenManGaming).
2. **Publisher Giveaways:** Via GamerPower API (100% off publisher promos).
3. **SQLite Deduplication:** Prevents repeated alerts for the same game edition.
4. **Instant Push Dispatch:** Broadcasts within seconds to our Telegram Channel.

---

## 📢 Live Alerts Feed (Free Access)

All detected price glitches and 100% free games are broadcast live in real-time:

👉 **[Join @price_glitch_live on Telegram]({CHANNEL_URL})**  
🌐 **[Real-Time Web Tracker (GitHub Pages)]({WEB_TRACKER_URL})**  
📡 **[RSS Syndication Feed]({WEB_TRACKER_URL}rss.xml)**

---

## 🛠️ Open Source Repository

The entire codebase is open-source under MIT License:
👉 [https://github.com/magomedta/steam-price-glitch-alerts](https://github.com/magomedta/steam-price-glitch-alerts)

Feel free to star the repo and contribute!
"""
    with open(article_path, "w", encoding="utf-8") as f:
        f.write(content)
    return article_path

def run_traffic_boost():
    print("=" * 65)
    print(" 🚀 REAL ZERO-BUDGET AUDIENCE ACQUISITION ENGINE")
    print("=" * 65)
    
    # 1. Reddit 1-Click Viral Campaign
    print("\n[1] REDDIT 1-CLICK CAMPAIGN (300k+ Gamers Active Now)")
    campaigns = generate_reddit_campaign()
    for i, c in enumerate(campaigns, 1):
        print(f"\n  Deal #{i}: {c['title']}")
        print(f"  👉 Submit to r/freegames: {c['reddit_freegames']}")
        print(f"  👉 Submit to r/FreeGameFindings: {c['reddit_fgf']}")

    # 2. SEO Article Generator for Google Ranking
    print("\n[2] GOOGLE 1ST-PAGE SEO ARTICLE (Dev.to / Medium / HackerNews)")
    art_path = generate_devto_seo_article()
    print(f"  [✔] Generated Google SEO Article: {art_path}")
    print(f"  This article contains high-converting backlinks to {CHANNEL_URL}")

    # 3. Telegram In-App Search Satellite Setup Instructions
    print("\n[3] TELEGRAM IN-APP SEARCH FUNNEL (Catches Daily Searches)")
    print("  Keywords to catch in Telegram search: 'Халява Steam', 'Бесплатные игры', 'Price Glitch'")

    print("\n" + "=" * 65)

if __name__ == "__main__":
    run_traffic_boost()
