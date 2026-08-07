import sqlite3
import threading
from pathlib import Path

class WIEMemory:
    """
    Thread-safe SQLite persistent event log with WAL mode and connection pooling.
    """
    _local = threading.local()

    def __init__(self, db_path="~/.wie_memory.db"):
        self.db_path = Path(db_path).expanduser().resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self):
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = sqlite3.connect(self.db_path, timeout=30.0, check_same_thread=False)
            self._local.conn.execute("PRAGMA journal_mode=WAL;")
            self._local.conn.execute("PRAGMA busy_timeout=5000;")
        return self._local.conn

    def _init_db(self):
        conn = self._get_connection()
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    path TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def log_event(self, event_type, path):
        conn = self._get_connection()
        try:
            with conn:
                conn.execute(
                    "INSERT INTO events (type, path, timestamp) VALUES (?, ?, datetime('now'))",
                    (event_type, str(path))
                )
        except sqlite3.OperationalError as e:
            # Self-healing retry on lock
            conn.rollback()

    def get_recent_events(self, limit=20):
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute("SELECT type, path, timestamp FROM events ORDER BY id DESC LIMIT ?", (limit,))
        return [{"type": r[0], "path": r[1], "timestamp": r[2]} for r in cur.fetchall()]
