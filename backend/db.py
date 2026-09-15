# db.py
import sqlite3
from decimal import Decimal
from contextlib import contextmanager

DB_PATH = "banking.db"

# --- Teach sqlite3 to round-trip Decimal ---
# SQLite has no DECIMAL type; we store balances/amounts as TEXT and
# convert at the boundary so all Python code still sees real Decimals.
sqlite3.register_adapter(Decimal, str)                       # Decimal -> DB
sqlite3.register_converter("DECIMAL", lambda b: Decimal(b.decode()))  # DB -> Decimal

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    balance DECIMAL DEFAULT '0.00',
    account_type TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS transactions (
    txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    txn_type TEXT,
    amount DECIMAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);
"""


def _connect():
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row          # rows support row["column"] access
    conn.execute("PRAGMA foreign_keys = ON")  # off by default in SQLite!
    return conn


def init_db():
    conn = _connect()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


@contextmanager
def get_cursor(commit=False):
    conn = _connect()
    cursor = conn.cursor()
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    init_db()
    with get_cursor() as cur:
        cur.execute("SELECT 1")
        print("Connection OK:", tuple(cur.fetchone()))
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        print("Tables:", [r["name"] for r in cur.fetchall()])