import json
import sqlite3
import time
import re
from pathlib import Path

class WorkflowContextManager:
    """
    Manages and isolates context across multiple concurrent workflows:
    - Independent context namespaces per workflow ID
    - Selective cross-workflow context handoffs
    - Compaction and token pruning to prevent window exhaustion
    - Persistent SQLite WAL backing for crash recovery
    """
    def __init__(self, db_path=None):
        if db_path is None:
            home = Path.home()
            app_dir = home / ".agent_workspace"
            app_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = app_dir / "workflow_context.db"
        else:
            self.db_path = Path(db_path)
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(str(self.db_path), timeout=10.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS workflows (
                    workflow_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    status TEXT DEFAULT 'ACTIVE',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS context_frames (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workflow_id TEXT NOT NULL,
                    frame_key TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    token_estimate INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (workflow_id) REFERENCES workflows(workflow_id) ON DELETE CASCADE
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_wf_frames ON context_frames(workflow_id, frame_key);")

    def register_workflow(self, workflow_id, name="Unnamed Workflow"):
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO workflows (workflow_id, name, status, updated_at)
                VALUES (?, ?, 'ACTIVE', CURRENT_TIMESTAMP);
            """, (workflow_id, name))
        return {"workflow_id": workflow_id, "name": name, "status": "ACTIVE"}

    def set_frame(self, workflow_id, frame_key, payload):
        self.register_workflow(workflow_id)
        payload_str = json.dumps(payload, ensure_ascii=False) if isinstance(payload, (dict, list)) else str(payload)
        tokens = max(1, len(payload_str) // 4)

        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO context_frames (workflow_id, frame_key, payload, token_estimate)
                VALUES (?, ?, ?, ?);
            """, (workflow_id, frame_key, payload_str, tokens))
            conn.execute("UPDATE workflows SET updated_at = CURRENT_TIMESTAMP WHERE workflow_id = ?;", (workflow_id,))

        return {"workflow_id": workflow_id, "frame_key": frame_key, "token_estimate": tokens}

    def get_context(self, workflow_id, latest_only=True):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if latest_only:
                cursor.execute("""
                    SELECT frame_key, payload, token_estimate, created_at
                    FROM context_frames
                    WHERE workflow_id = ?
                    ORDER BY id DESC;
                """, (workflow_id,))
            else:
                cursor.execute("""
                    SELECT frame_key, payload, token_estimate, created_at
                    FROM context_frames
                    WHERE workflow_id = ?
                    ORDER BY id ASC;
                """, (workflow_id,))

            rows = cursor.fetchall()
            
        context_map = {}
        total_tokens = 0
        for key, payload_str, tok, ts in rows:
            if key not in context_map:
                try:
                    val = json.loads(payload_str)
                except Exception:
                    val = payload_str
                context_map[key] = {
                    "value": val,
                    "tokens": tok,
                    "timestamp": ts
                }
                total_tokens += tok

        return {
            "workflow_id": workflow_id,
            "total_tokens": total_tokens,
            "frames": context_map
        }

    def handoff_context(self, source_wf_id, target_wf_id, keys=None):
        """
        Selectively transfers context keys from one workflow to another.
        """
        source_ctx = self.get_context(source_wf_id)
        transferred = []
        
        frames = source_ctx.get("frames", {})
        for k, data in frames.items():
            if keys is None or k in keys:
                self.set_frame(target_wf_id, k, data["value"])
                transferred.append(k)

        return {
            "source_workflow": source_wf_id,
            "target_workflow": target_wf_id,
            "transferred_keys": transferred
        }

    def prune_workflow_context(self, workflow_id, max_frames=10):
        """
        Prunes older historical frames, retaining only the most recent frames.
        """
        with self._get_connection() as conn:
            conn.execute("""
                DELETE FROM context_frames
                WHERE workflow_id = ? AND id NOT IN (
                    SELECT id FROM context_frames
                    WHERE workflow_id = ?
                    ORDER BY id DESC
                    LIMIT ?
                );
            """, (workflow_id, workflow_id, max_frames))
        return {"workflow_id": workflow_id, "pruned_to_max_frames": max_frames}
