import sqlite3
import os
import json
import time
from pathlib import Path

class AgentChannel:
    """
    High-speed, persistent inter-agent pub/sub messaging bus.
    """
    def __init__(self, db_path="~/.agent_channel.db"):
        self.db_path = Path(db_path).expanduser().resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=5000;")
        return conn

    def _init_db(self):
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    sender TEXT NOT NULL,
                    recipient TEXT DEFAULT 'ALL',
                    payload TEXT NOT NULL,
                    status TEXT DEFAULT 'UNREAD',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def publish(self, topic, payload, sender="main_agent", recipient="ALL"):
        payload_str = json.dumps(payload) if isinstance(payload, (dict, list)) else str(payload)
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO messages (topic, sender, recipient, payload) VALUES (?, ?, ?, ?)",
                (topic, sender, recipient, payload_str)
            )
            return cur.lastrowid

    def read_topic(self, topic=None, recipient=None, limit=20, mark_read=False):
        with self._get_conn() as conn:
            cur = conn.cursor()
            query = "SELECT id, topic, sender, recipient, payload, status, created_at FROM messages WHERE 1=1"
            params = []
            if topic:
                query += " AND topic = ?"
                params.append(topic)
            if recipient:
                query += " AND (recipient = ? OR recipient = 'ALL')"
                params.append(recipient)
            
            query += " ORDER BY id DESC LIMIT ?"
            params.append(limit)

            cur.execute(query, tuple(params))
            rows = cur.fetchall()

            messages = []
            ids_to_mark = []
            for r in rows:
                try:
                    data = json.loads(r[4])
                except Exception:
                    data = r[4]
                messages.append({
                    "id": r[0],
                    "topic": r[1],
                    "sender": r[2],
                    "recipient": r[3],
                    "payload": data,
                    "status": r[5],
                    "created_at": r[6]
                })
                ids_to_mark.append(r[0])

            if mark_read and ids_to_mark:
                conn.execute(
                    f"UPDATE messages SET status = 'READ' WHERE id IN ({','.join(['?']*len(ids_to_mark))})",
                    ids_to_mark
                )

            return messages

    def clear(self):
        with self._get_conn() as conn:
            conn.execute("DELETE FROM messages")
