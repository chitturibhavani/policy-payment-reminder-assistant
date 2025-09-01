import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "assistant.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Store conversations + customer lookups
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  customer_id TEXT,
                  user_message TEXT,
                  bot_reply TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def log_message(customer_id, user_message, bot_reply):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO chat_history (customer_id, user_message, bot_reply) VALUES (?, ?, ?)",
              (customer_id, user_message, bot_reply))
    conn.commit()
    conn.close()

def fetch_history(customer_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_message, bot_reply, timestamp FROM chat_history WHERE customer_id=? ORDER BY id DESC LIMIT 5", (customer_id,))
    rows = c.fetchall()
    conn.close()
    return rows
