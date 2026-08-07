import sqlite3
from pathlib import Path

class WIEMemory:
    def __init__(self, db_path):
        self.db_path = Path(db_path).resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _init_db(self):
        self.conn.execute("CREATE TABLE IF NOT EXISTS events (type TEXT, path TEXT, timestamp DATETIME)")
        self.conn.commit()

    def log_event(self, event_type, path):
        self.conn.execute("INSERT INTO events VALUES (?, ?, datetime('now'))", (event_type, str(path)))
        self.conn.commit()
