import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "glitches.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS seen_deals (
            deal_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            store TEXT,
            normal_price REAL,
            sale_price REAL,
            savings REAL,
            url TEXT,
            discovered_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def is_deal_seen(deal_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM seen_deals WHERE deal_id = ?", (deal_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def save_deal(deal_id: str, title: str, store: str, normal_price: float, sale_price: float, savings: float, url: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO seen_deals 
            (deal_id, title, store, normal_price, sale_price, savings, url, discovered_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (deal_id, title, store, normal_price, sale_price, savings, url, datetime.utcnow()))
        conn.commit()
    finally:
        conn.close()

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), AVG(savings) FROM seen_deals")
    row = cursor.fetchone()
    conn.close()
    count = row[0] if row else 0
    avg_savings = round(row[1], 1) if row and row[1] else 0.0
    return {"total_glitches": count, "avg_savings": avg_savings}

init_db()
