

import sqlite3
from contextlib import closing
from typing import List

DB_PATH = "signals.db"

def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS signals (
                    pair TEXT,
                    signal TEXT,
                    confidence INTEGER,
                    entry_price REAL,
                    stop_loss REAL,
                    take_profit REAL,
                    timestamp TEXT PRIMARY KEY,
                    reasons TEXT
                )
            """)

def insert_signal(data: dict):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute("""
                INSERT OR REPLACE INTO signals (
                    pair, signal, confidence, entry_price, stop_loss, take_profit, timestamp, reasons
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["pair"],
                data["signal"],
                data["confidence"],
                data["entry_price"],
                data["stop_loss"],
                data["take_profit"],
                data["timestamp"],
                data["reasons"]
            ))
def get_signals(page: int = 1, page_size: int = 10) -> List[dict]:
    offset = (page - 1) * page_size
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM signals
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        """, (page_size, offset))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]