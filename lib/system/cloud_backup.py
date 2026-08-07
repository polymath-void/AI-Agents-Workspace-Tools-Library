import os
import sys
import re
import json
import time
import shutil
import tarfile
import hashlib
import sqlite3

from pathlib import Path
from typing import Dict, Any, List, Optional

DEFAULT_EXCLUDES = [
    ".git", "node_modules", ".cache", "__pycache__", "build",
    "dist", ".gradle", ".idea", "*.pyc", "*.tmp", "*.log",
    "storage/shared", "storage/downloads", "storage/dcim"
]

TARGET_MAP = {
    "agy": [Path.home() / ".gemini" / "antigravity-cli"],
    "gemini": [Path.home() / ".gemini"],
    "termux": [
        Path.home() / ".termux",
        Path.home() / ".bashrc",
        Path.home() / ".zshrc",
        Path.home() / ".gitconfig",
        Path.home() / ".ssh",
        Path.home() / "skills-workspace",
        Path.home() / "AI-Agents-Workspace-Tools-Library"
    ],
    "all": [Path.home()]
}

class CloudBackupEngine:
    """Zero-overhead incremental tarball creator, manifest hasher & cloud sync manager."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or (Path.home() / ".gemini" / "antigravity-cli" / "backup_ledger.sqlite")
        self._init_db()

    def _init_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS backup_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target TEXT NOT NULL,
                    archive_path TEXT NOT NULL,
                    sha256 TEXT NOT NULL,
                    file_count INTEGER NOT NULL,
                    size_bytes INTEGER NOT NULL,
                    timestamp REAL NOT NULL
                )
            """)
            conn.commit()

    @staticmethod
    def calculate_file_hash(path: Path) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()

    def should_exclude(self, path: Path, extra_excludes: Optional[List[str]] = None) -> bool:
        excludes = DEFAULT_EXCLUDES + (extra_excludes or [])
        path_str = str(path)
        for excl in excludes:
            if excl.startswith("*"):
                if path.name.endswith(excl[1:]):
                    return True
            elif excl in path.parts or excl == path.name:
                return True
        return False

    def scan_target(self, target_paths: List[Path], extra_excludes: Optional[List[str]] = None) -> Dict[str, Any]:
        manifest = {}
        total_size = 0
        file_count = 0

        for root_target in target_paths:
            if not root_target.exists():
                continue
            if root_target.is_file():
                if not self.should_exclude(root_target, extra_excludes):
                    size = root_target.stat().st_size
                    manifest[str(root_target)] = {
                        "size": size,
                        "mtime": root_target.stat().st_mtime,
                        "sha256": self.calculate_file_hash(root_target)
                    }
                    total_size += size
                    file_count += 1
            elif root_target.is_dir():
                for p in root_target.rglob("*"):
                    if p.is_file() and not p.is_symlink():
                        if not self.should_exclude(p, extra_excludes):
                            try:
                                size = p.stat().st_size
                                manifest[str(p)] = {
                                    "size": size,
                                    "mtime": p.stat().st_mtime
                                }
                                total_size += size
                                file_count += 1
                            except (PermissionError, FileNotFoundError):
                                pass

        return {
            "file_count": file_count,
            "total_size": total_size,
            "manifest": manifest
        }

    def create_backup(self, target: str = "agy", dest_dir: Optional[Path] = None, dry_run: bool = False, force: bool = False) -> Dict[str, Any]:
        target_paths = TARGET_MAP.get(target, [Path(target) if Path(target).exists() else Path.home()])
        dest_dir = dest_dir or (Path.home() / "backups" / "cloud_staging")
        dest_dir.mkdir(parents=True, exist_ok=True)

        scan_result = self.scan_target(target_paths)
        if scan_result["file_count"] == 0:
            return {"status": "SKIPPED", "reason": "No files matched target criteria", "target": target}

        ts = int(time.time())
        target_slug = re.sub(r"[^a-zA-Z0-9_-]", "_", target).strip("_") or "all"
        archive_name = f"backup_{target_slug}_{ts}.tar.gz"
        archive_path = dest_dir / archive_name

        if dry_run:
            return {
                "status": "DRY_RUN",
                "target": target,
                "file_count": scan_result["file_count"],
                "total_size_bytes": scan_result["total_size"],
                "archive_target": str(archive_path)
            }

        # Check last snapshot to see if incremental update is required
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT sha256, file_count, size_bytes FROM backup_snapshots WHERE target = ? ORDER BY timestamp DESC LIMIT 1", (target,))
            last_snap = cur.fetchone()

        # Create compressed tarball
        with tarfile.open(archive_path, "w:gz") as tar:
            for filepath in scan_result["manifest"].keys():
                p = Path(filepath)
                if p.exists():
                    try:
                        arcname = str(p.relative_to(Path.home())) if str(p).startswith(str(Path.home())) else p.name
                        tar.add(p, arcname=arcname)
                    except Exception:
                        pass

        archive_sha = self.calculate_file_hash(archive_path)
        archive_size = archive_path.stat().st_size

        if not force and last_snap and last_snap[0] == archive_sha:
            archive_path.unlink()
            return {
                "status": "UP_TO_DATE",
                "message": "No changes detected since last snapshot.",
                "target": target
            }

        # Record snapshot in SQLite
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO backup_snapshots (target, archive_path, sha256, file_count, size_bytes, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                (target, str(archive_path), archive_sha, scan_result["file_count"], archive_size, time.time())
            )
            conn.commit()

        # Write manifest file alongside
        manifest_path = dest_dir / f"backup_{target_slug}_{ts}_manifest.json"
        manifest_path.write_text(json.dumps({
            "target": target,
            "timestamp": ts,
            "archive": archive_name,
            "sha256": archive_sha,
            "file_count": scan_result["file_count"],
            "archive_size": archive_size,
            "files": scan_result["manifest"]
        }, indent=2))

        return {
            "status": "SUCCESS",
            "target": target,
            "archive": str(archive_path),
            "manifest": str(manifest_path),
            "file_count": scan_result["file_count"],
            "size_bytes": archive_size,
            "sha256": archive_sha,
            "timestamp": ts
        }

    def list_backups(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM backup_snapshots ORDER BY timestamp DESC").fetchall()
            return [dict(r) for r in rows]

    def status(self) -> Dict[str, Any]:
        backups = self.list_backups()
        return {
            "db_path": str(self.db_path),
            "total_snapshots": len(backups),
            "latest_snapshots": backups[:5]
        }
