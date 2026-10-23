import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from scrapers.cheapshark import fetch_cheapshark_glitches
from scrapers.gamerpower import fetch_gamerpower_glitches

def generate_feeds():
    """
    Generates rss.xml and feed.json in the repository root for external syndication
    (Discord webhooks, RSS readers, social cross-posters).
    """
    cs_deals = fetch_cheapshark_glitches()
    gp_deals = fetch_gamerpower_glitches()
    all_deals = (gp_deals + cs_deals)[:20]

    # 1. Generate feed.json (JSON Feed v1.1)
    json_feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": "Price Glitch Live - 100% Free Games & Pricing Errors",
        "home_page_url": "https://magomedta.github.io/steam-price-glitch-alerts/",
        "feed_url": "https://magomedta.github.io/steam-price-glitch-alerts/feed.json",
        "description": "Real-time alerts for 85%-100% price glitches, publisher mistakes, and free giveaways.",
        "icon": "https://raw.githubusercontent.com/magomedta/steam-price-glitch-alerts/main/channel_avatar.jpg",
        "favicon": "https://raw.githubusercontent.com/magomedta/steam-price-glitch-alerts/main/channel_avatar.jpg",
        "items": []
    }

    # 2. Generate rss.xml (RSS 2.0)
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "Price Glitch Live - 100% Free Games & Pricing Errors"
    ET.SubElement(channel, "link").text = "https://t.me/price_glitch_live"
    ET.SubElement(channel, "description").text = "Autonomous monitor detecting 85%-100% discounts and price glitches."
    ET.SubElement(channel, "language").text = "en-us"
    ET.SubElement(channel, "lastBuildDate").text = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

    for deal in all_deals:
        title = deal.get("title", "Game Deal")
        store = deal.get("store", "Digital Store")
        savings = int(deal.get("savings", 100))
        sale_price = deal.get("sale_price", 0.0)
        normal_price = deal.get("normal_price", 19.99)
        url = deal.get("url", "https://t.me/price_glitch_live")
        deal_id = deal.get("id", str(hash(title)))

        price_str = "100% FREE ($0.00)" if sale_price == 0.0 else f"${sale_price:.2f} (-{savings}%)"

        item_desc = (
            f"🚨 PRICE GLITCH ({savings}% OFF): {title} on {store}.\n"
            f"Regular Price: ${normal_price:.2f} -> Glitch Price: {price_str}\n\n"
            f"Claim link: {url}\n\n"
            f"⚡ For 0-second push notifications, join Telegram: https://t.me/price_glitch_live"
        )

        # Append to JSON feed
        json_feed["items"].append({
            "id": deal_id,
            "url": url,
            "title": f"[{store}] {title} - {price_str}",
            "content_text": item_desc,
            "date_published": datetime.now(timezone.utc).isoformat()
        })

        # Append to RSS XML
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = f"[{store}] {title} - {price_str}"
        ET.SubElement(item, "link").text = url
        ET.SubElement(item, "guid").text = deal_id
        ET.SubElement(item, "description").text = item_desc
        ET.SubElement(item, "pubDate").text = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

    # Write feed.json
    with open("feed.json", "w", encoding="utf-8") as f:
        json.dump(json_feed, f, indent=2, ensure_ascii=False)

    # Write rss.xml
    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ", level=0)
    tree.write("rss.xml", encoding="utf-8", xml_declaration=True)

    print(f"[✔] Syndication feeds updated: feed.json and rss.xml ({len(all_deals)} items)")

if __name__ == "__main__":
    generate_feeds()
