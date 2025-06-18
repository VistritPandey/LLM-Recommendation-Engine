from typing import Dict, Any, List
import sqlite3
import json
from pathlib import Path
from .base import BaseStorage


class SQLiteStorage(BaseStorage):
    def __init__(self, db_path: str | Path = "recommender.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS items(
                id TEXT PRIMARY KEY,
                payload TEXT
            )"""
        )
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS users(
                id TEXT PRIMARY KEY,
                vector TEXT
            )"""
        )
        self.conn.commit()

    def save_item(self, item_id: str, payload: Dict[str, Any]):
        self.conn.execute(
            "REPLACE INTO items(id, payload) VALUES (?, ?)",
            (item_id, json.dumps(payload)),
        )
        self.conn.commit()

    def get_all_items(self) -> List[Dict[str, Any]]:
        cur = self.conn.execute("SELECT payload FROM items")
        return [json.loads(row[0]) for row in cur.fetchall()]

    def save_user_vector(self, user_id: str, vector):
        self.conn.execute(
            "REPLACE INTO users(id, vector) VALUES (?, ?)",
            (user_id, json.dumps(vector)),
        )
        self.conn.commit()

    def get_user_vector(self, user_id: str):
        cur = self.conn.execute("SELECT vector FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()
        return json.loads(row[0]) if row else None 