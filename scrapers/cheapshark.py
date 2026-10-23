import requests
import logging
from config import MIN_DISCOUNT_PERCENT, MAX_GLITCH_PRICE, STORES_MAP, CHEAPSHARK_AFFILIATE_ID

API_URL = "https://www.cheapshark.com/api/1.0/deals"

def fetch_cheapshark_glitches():
    """
    Scrapes high-discount anomalies from CheapShark's live aggregation feed.
    Filters for >= MIN_DISCOUNT_PERCENT (default 85%+) or high-value price errors.
    """
    glitches = []
    try:
        # Request top savings sorted descending (desc=0 in CheapShark = highest savings first)
        params = {
            "sortBy": "Savings",
            "pageSize": 60,
            "output": "json"
        }
        headers = {
            "User-Agent": "PriceGlitchMonitor/2.0 (alerts@priceglitch.live)"
        }

        response = requests.get(API_URL, params=params, headers=headers, timeout=12)
        if response.status_code != 200:
            logging.error(f"[CheapShark] API returned status {response.status_code}: {response.text[:100]}")
            return []

        deals = response.json()
        for deal in deals:
            try:
                savings = float(deal.get("savings", 0))
                sale_price = float(deal.get("salePrice", 0))
                normal_price = float(deal.get("normalPrice", 0))
                title = deal.get("title", "Unknown Title")
                deal_id = deal.get("dealID", "")
                store_id = str(deal.get("storeID", "1"))
                store_name = STORES_MAP.get(store_id, f"Store #{store_id}")
                thumb = deal.get("thumb", "")

                # Criteria for Price Glitch / Anomaly:
                # 1. Savings >= MIN_DISCOUNT_PERCENT (e.g. 85% to 100%)
                # 2. Or high value item (> $20 normal price) selling for under $5 with >= 75% off
                is_high_discount = savings >= MIN_DISCOUNT_PERCENT
                is_severe_price_drop = (normal_price >= 19.99 and sale_price <= MAX_GLITCH_PRICE and savings >= 75)

                if is_high_discount or is_severe_price_drop:
                    # Construct affiliate URL
                    raw_url = f"https://www.cheapshark.com/redirect?dealID={deal_id}"
                    if CHEAPSHARK_AFFILIATE_ID:
                        raw_url += f"&aff={CHEAPSHARK_AFFILIATE_ID}"

                    glitches.append({
                        "id": f"cs_{deal_id}",
                        "title": title,
                        "store": store_name,
                        "normal_price": normal_price,
                        "sale_price": sale_price,
                        "savings": round(savings, 1),
                        "url": raw_url,
                        "thumb": thumb,
                        "source": "CheapShark Feed"
                    })
            except (ValueError, KeyError) as e:
                continue

    except Exception as e:
        logging.error(f"[CheapShark] Exception during fetch: {e}")

    return glitches
