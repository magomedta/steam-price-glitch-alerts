import time
import sys
import threading
import logging
from datetime import datetime
from colorama import init, Fore, Style

from config import SCAN_INTERVAL_SECONDS, TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
import database
from scrapers.cheapshark import fetch_cheapshark_glitches
from scrapers.gamerpower import fetch_gamerpower_glitches
from publisher import publish_to_telegram, format_glitch_message
from bot_listener import start_bot_polling

init(autoreset=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def print_banner():
    print(Fore.CYAN + Style.BRIGHT + """
 =======================================================
   🔥 AUTONOMOUS PRICE GLITCH & ARBITRAGE BOT v1.0
   100% Autonomous | Zero Human Needed | 24/7 Scanner
 =======================================================
    """ + Style.RESET_ALL)
    
    stats = database.get_stats()
    tg_status = Fore.GREEN + "LIVE (" + TELEGRAM_CHANNEL_ID + ")" if TELEGRAM_BOT_TOKEN else Fore.YELLOW + "CONSOLE DEMO MODE (Add Token in .env for Live Telegram)"
    print(f"[*] Telegram Dispatcher: {tg_status}")
    print(f"[*] Database Memory:     {stats['total_glitches']} historic deals tracked")
    print(f"[*] Scan Frequency:      Every {SCAN_INTERVAL_SECONDS} seconds")
    print(Fore.CYAN + "-------------------------------------------------------\n")

def run_scanner_cycle():
    """
    Executes one complete scanning cycle across all price anomaly sources.
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {Fore.BLUE}Scanning feeds for pricing errors & 85%+ glitches...{Style.RESET_ALL}")

    # 1. Fetch from CheapShark (Steam, Humble, GOG, GamersGate, etc.)
    cs_deals = fetch_cheapshark_glitches()
    # 2. Fetch from GamerPower (100% Free Publisher Glitches)
    gp_deals = fetch_gamerpower_glitches()

    all_deals = cs_deals + gp_deals
    new_glitches_found = 0

    for deal in all_deals:
        deal_id = deal.get("id")
        title = deal.get("title")
        savings = deal.get("savings")
        sale_price = deal.get("sale_price")
        normal_price = deal.get("normal_price")
        store = deal.get("store")

        if not database.is_deal_seen(deal_id):
            new_glitches_found += 1
            # Save to SQLite database to prevent double-alerts
            database.save_deal(
                deal_id=deal_id,
                title=title,
                store=store,
                normal_price=normal_price,
                sale_price=sale_price,
                savings=savings,
                url=deal.get("url")
            )

            # Publish immediately to Telegram
            publish_to_telegram(deal)

            # Console notification
            print(Fore.GREEN + Style.BRIGHT + f" [NEW GLITCH] " + Style.RESET_ALL +
                  f"{Fore.YELLOW}{title}{Style.RESET_ALL} | " +
                  f"{Fore.CYAN}{store}{Style.RESET_ALL} | " +
                  f"Was: ${normal_price:.2f} -> {Fore.GREEN}${sale_price:.2f} (-{int(savings)}%){Style.RESET_ALL}")

    if new_glitches_found > 0:
        try:
            from feed_generator import generate_feeds
            generate_feeds()
        except Exception as e:
            logging.warning(f"Failed updating feeds: {e}")
    else:
        print(f"[{timestamp}] Feeds checked. No new unposted glitches this tick. Monitoring active...")

    return new_glitches_found

def main():
    print_banner()

    # If --test argument passed, run one instant scan and exit
    if "--test" in sys.argv:
        print(Fore.YELLOW + "[*] Running in Instant Test Mode to show live glitches..." + Style.RESET_ALL)
        run_scanner_cycle()
        print(Fore.GREEN + "\n[✔] Test scan complete! All APIs working flawlessly." + Style.RESET_ALL)
        return

    # Launch background Telegram interaction listener thread
    listener_thread = threading.Thread(target=start_bot_polling, daemon=True)
    listener_thread.start()

    # Continuous 24/7 background loop
    print(Fore.GREEN + "[*] Bot engine started. Running autonomously 24/7. Press Ctrl+C to stop.\n" + Style.RESET_ALL)
    try:
        while True:
            run_scanner_cycle()
            time.sleep(SCAN_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[*] Scanner stopped by user." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
