import urllib.parse
from typing import Dict, List

def format_pikabu_post(deal: Dict) -> Dict[str, str]:
    """
    Formats a deal for Pikabu (pikabu.ru/community/steam) - the largest Russian gaming community.
    """
    title = deal.get("title", "Game")
    store = deal.get("store", "Steam")
    savings = int(deal.get("savings", 100))
    url = deal.get("url", "")
    normal_price = deal.get("normal_price", 0.0)

    if savings == 100:
        ru_title = f"[Халява] В {store} временно отдают бесплатно {title} (100% скидка)"
    else:
        ru_title = f"[Скидка] В {store} отдают {title} за ${deal.get('sale_price', 0.99):.2f} (Скидка {savings}%)"

    ru_body = (
        f"**Игра:** {title}\n"
        f"**Магазин:** {store}\n"
        f"**Скидка:** {savings}%\n"
        f"**Ссылка на игру:** {url}\n\n"
        f"---\n"
        f"⚡ *Моментальные оповещения о багах цен и 100% халяве:* https://t.me/price_glitch_live"
    )

    vk_share_url = (
        f"https://vk.com/share.php?"
        f"url={urllib.parse.quote(url)}&"
        f"title={urllib.parse.quote(ru_title + ' | t.me/price_glitch_live')}"
    )

    return {
        "title": ru_title,
        "body": ru_body,
        "url": url,
        "vk_share_url": vk_share_url
    }

if __name__ == "__main__":
    test = {"title": "Space Crew", "store": "Steam", "savings": 100, "url": "https://store.steampowered.com"}
    print(format_pikabu_post(test))
