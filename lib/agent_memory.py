import os
import json
import sqlite3
import shutil
import time
from pathlib import Path

DEFAULT_DB_PATH = os.path.expanduser("~/.agent_memory.db")

class AgentMemoryStore:
    """
    Persistent SQLite storage for agent knowledge, decisions, and workspace snapshots.
    """
    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = Path(db_path).resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS memory_kv (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    category TEXT,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS snapshots (
                    snapshot_id TEXT PRIMARY KEY,
                    tag TEXT,
                    target_dir TEXT,
                    backup_path TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def set(self, key, value, category="general"):
        val_str = json.dumps(value) if not isinstance(value, str) else value
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO memory_kv (key, value, category, updated_at) VALUES (?, ?, ?, datetime('now'))",
                (key, val_str, category)
            )

    def get(self, key):
        cur = self.conn.cursor()
        cur.execute("SELECT value FROM memory_kv WHERE key = ?", (key,))
        row = cur.fetchone()
        if not row:
            return None
        try:
            return json.loads(row[0])
        except Exception:
            return row[0]

    def list_keys(self, category=None):
        cur = self.conn.cursor()
        if category:
            cur.execute("SELECT key, category, updated_at FROM memory_kv WHERE category = ? ORDER BY updated_at DESC", (category,))
        else:
            cur.execute("SELECT key, category, updated_at FROM memory_kv ORDER BY updated_at DESC")
        return [{"key": r[0], "category": r[1], "updated_at": r[2]} for r in cur.fetchall()]

    def delete(self, key):
        with self.conn:
            self.conn.execute("DELETE FROM memory_kv WHERE key = ?", (key,))

    def create_snapshot(self, target_dir, tag="manual"):
        src = Path(target_dir).resolve()
        if not src.exists():
            raise FileNotFoundError(f"Target directory not found: {target_dir}")

        snap_id = f"snap_{int(time.time())}"
        backup_dir = Path(os.path.expanduser("~/.agent_snapshots")) / snap_id
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Copy non-ignored files
        ignore_names = shutil.ignore_patterns('.git', 'node_modules', 'build', '.gradle', '__pycache__', '.cache')
        shutil.copytree(src, backup_dir / src.name, ignore=ignore_names, dirs_exist_ok=True)

        with self.conn:
            self.conn.execute(
                "INSERT INTO snapshots (snapshot_id, tag, target_dir, backup_path) VALUES (?, ?, ?, ?)",
                (snap_id, tag, str(src), str(backup_dir / src.name))
            )
        return {"snapshot_id": snap_id, "tag": tag, "backup_path": str(backup_dir / src.name)}

    def list_snapshots(self):
        cur = self.conn.cursor()
        cur.execute("SELECT snapshot_id, tag, target_dir, backup_path, created_at FROM snapshots ORDER BY created_at DESC")
        return [{
            "snapshot_id": r[0], "tag": r[1], "target_dir": r[2], "backup_path": r[3], "created_at": r[4]
        } for r in cur.fetchall()]
