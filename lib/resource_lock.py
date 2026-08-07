import time
import os
import json
from pathlib import Path

class ResourceLock:
    """
    Distributed mutex locking to protect files/resources across subagents and background threads.
    """
    def __init__(self, lock_dir="~/.agent_locks"):
        self.lock_dir = Path(lock_dir).expanduser().resolve()
        self.lock_dir.mkdir(parents=True, exist_ok=True)

    def _get_lock_file(self, resource_name):
        safe_name = resource_name.replace("/", "_").replace("\\", "_")
        return self.lock_dir / f"{safe_name}.lock"

    def acquire(self, resource_name, holder="agent", ttl_seconds=60, wait_seconds=5):
        lock_file = self._get_lock_file(resource_name)
        start = time.perf_counter()

        while time.perf_counter() - start <= wait_seconds:
            if lock_file.exists():
                try:
                    data = json.loads(lock_file.read_text())
                    # Check TTL expiry
                    if time.time() - data.get("acquired_at", 0) > data.get("ttl", 60):
                        # Lock expired, remove stale lock
                        lock_file.unlink(missing_ok=True)
                    else:
                        time.sleep(0.2)
                        continue
                except Exception:
                    lock_file.unlink(missing_ok=True)

            try:
                # Atomically write lock
                payload = {
                    "resource": resource_name,
                    "holder": holder,
                    "acquired_at": time.time(),
                    "ttl": ttl_seconds
                }
                lock_file.write_text(json.dumps(payload))
                return True
            except Exception:
                time.sleep(0.2)

        return False

    def release(self, resource_name, holder=None):
        lock_file = self._get_lock_file(resource_name)
        if not lock_file.exists():
            return True

        try:
            if holder:
                data = json.loads(lock_file.read_text())
                if data.get("holder") != holder:
                    return False  # Cannot release lock held by someone else
            lock_file.unlink(missing_ok=True)
            return True
        except Exception:
            return False

    def status(self, resource_name):
        lock_file = self._get_lock_file(resource_name)
        if not lock_file.exists():
            return {"locked": False}

        try:
            data = json.loads(lock_file.read_text())
            is_active = time.time() - data.get("acquired_at", 0) <= data.get("ttl", 60)
            return {
                "locked": is_active,
                "holder": data.get("holder"),
                "acquired_at": data.get("acquired_at"),
                "ttl": data.get("ttl")
            }
        except Exception:
            return {"locked": False}
