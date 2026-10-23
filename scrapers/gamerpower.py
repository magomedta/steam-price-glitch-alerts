import requests
import logging

API_URL = "https://www.gamerpower.com/api/giveaways"

def fetch_gamerpower_glitches():
    """
    Scrapes 100% discount promotions, pricing errors, and limited giveaways on Steam/Epic/GOG.
    """
    glitches = []
    try:
        params = {
            "platform": "pc",
            "type": "game",
            "sort-by": "popularity"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        response = requests.get(API_URL, params=params, headers=headers, timeout=12)
        if response.status_code != 200:
            return []

        giveaways = response.json()
        for g in giveaways:
            try:
                g_id = g.get("id")
                title = g.get("title", "Free Game Alert")
                worth_str = g.get("worth", "$19.99").replace("$", "").replace("N/A", "0").strip()
                try:
                    normal_price = float(worth_str) if worth_str else 19.99
                except ValueError:
                    normal_price = 19.99

                # Only include significant items (normally >= $9.99)
                if normal_price < 8.0:
                    continue

                open_giveaway_url = g.get("open_giveaway_url") or g.get("gamerpower_url")
                image = g.get("image", "")

                glitches.append({
                    "id": f"gp_{g_id}",
                    "title": title,
                    "store": "Steam / Epic / GOG",
                    "normal_price": normal_price,
                    "sale_price": 0.00,
                    "savings": 100.0,
                    "url": open_giveaway_url,
                    "thumb": image,
                    "source": "100% Off Alert"
                })
            except Exception:
                continue

    except Exception as e:
        logging.error(f"[GamerPower] Exception: {e}")

    return glitches
