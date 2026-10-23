# ⚡ Steam & Epic Games Price Glitch Hunter

[![Telegram Channel](https://img.shields.io/badge/Telegram-Join%20Live%20Alerts-blue?style=for-the-badge&logo=telegram)](https://t.me/price_glitch_live)
[![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen?style=for-the-badge&logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

An autonomous, 24/7 background scanner that monitors 35+ digital storefronts (Steam, Epic Games Store, GOG, Humble Store, IndieGala, GreenManGaming) for **85% - 100% price glitches, publisher pricing mistakes, and limited-time giveaways**.

---

> ### 📢 LIVE ALERTS FEED (No Setup Needed!)
> If you don't want to run your own 24/7 server or setup Python, all detected price glitches and 100% free games are broadcast in real-time to our public Telegram channel:
> 
> 👉 **[Click here to Join @price_glitch_live on Telegram](https://t.me/price_glitch_live)**

---

## 🌟 Features

- **Extreme Anomaly Detection:** Flags items where normal price is high ($20 - $70) and sale price drops by 85% to 100%.
- **Zero Duplicates:** SQLite database ensures you only get alerted once per glitch.
- **Multi-Store Coverage:** Steam, Epic Games, GOG, Humble Store, Fanatical, GamersGate.
- **Instant Telegram Dispatch:** Formats eye-catching alerts with direct purchase links.
- **Built-in Auto-Affiliate:** Automatically appends referral tags for monetizing bargain feeds.

---

## 🚀 Quick Start (Run Locally)

### 1. Clone the repository
```bash
git clone https://github.com/magomedta/steam-price-glitch-alerts.git
cd steam-price-glitch-alerts
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure credentials
Copy `.env.example` to `.env`:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
TELEGRAM_CHANNEL_ID=@your_channel_username
```

### 4. Run the scanner
```bash
python main.py
```
Or test deal detection immediately:
```bash
python main.py --test
```

---

## 🔗 Official Community
- **Telegram Feed:** [t.me/price_glitch_live](https://t.me/price_glitch_live)
- **Discussion & Requests:** Open an Issue or join the channel!
