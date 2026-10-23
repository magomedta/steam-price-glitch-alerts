import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
# Get token from @BotFather on Telegram, or leave empty for console simulation mode
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")

# Detection Criteria for Price Glitches
MIN_DISCOUNT_PERCENT = int(os.getenv("MIN_DISCOUNT_PERCENT", "85")) # Only alert 85%+ discounts
MAX_GLITCH_PRICE = float(os.getenv("MAX_GLITCH_PRICE", "10.00"))    # Maximum price to be considered a budget glitch
SCAN_INTERVAL_SECONDS = int(os.getenv("SCAN_INTERVAL_SECONDS", "30")) # Loop scan frequency

# Affiliate Monetization Tags (Store pays commission on every purchase)
AMAZON_AFFILIATE_TAG = os.getenv("AMAZON_AFFILIATE_TAG", "priceglitch-20")
CHEAPSHARK_AFFILIATE_ID = os.getenv("CHEAPSHARK_AFFILIATE_ID", "priceglitch")

# Target Stores Mapping
STORES_MAP = {
    "1": "Steam",
    "2": "GamersGate",
    "3": "GreenManGaming",
    "4": "Amazon",
    "5": "GameStop",
    "6": "Direct2Drive",
    "7": "GOG",
    "8": "Origin",
    "11": "Humble Store",
    "13": "Uplay",
    "15": "Fanatical",
    "25": "Epic Games Store"
}
