import time
import os
import signal
import sys
from pathlib import Path

IGNORE_DIRS = {'.git', '__pycache__', 'node_modules', '.gradle', '.cache', '.wc_backups', '.agent_snapshots'}

class PollingObserver:
    def __init__(self, watch_path, callback, interval=3):
        self.watch_path = Path(watch_path).resolve()
        self.callback = callback
        self.interval = interval
        self._running = True
        self.state = self._scan()

    def _scan(self):
        new_state = {}
        if not self.watch_path.exists():
            return new_state

        try:
            for p in self.watch_path.rglob('*'):
                if any(ignored in p.parts for ignored in IGNORE_DIRS):
                    continue
                try:
                    if p.is_file(follow_symlinks=False):
                        new_state[str(p)] = p.stat().st_mtime
                except (OSError, PermissionError):
                    continue
        except (OSError, PermissionError):
            pass
        return new_state

    def stop(self):
        self._running = False

    def run(self):
        print(f"👁️  Workspace Observer active on: {self.watch_path} (interval={self.interval}s)")
        
        # Setup signal handler for graceful shutdown
        def _sig_handler(sig, frame):
            print("\n🛑 Shutting down Workspace Observer cleanly...")
            self.stop()

        signal.signal(signal.SIGINT, _sig_handler)
        signal.signal(signal.SIGTERM, _sig_handler)

        while self._running:
            try:
                time.sleep(self.interval)
                if not self._running:
                    break

                current_state = self._scan()

                # Detect Created / Modified Files
                for path, mtime in current_state.items():
                    if path not in self.state:
                        self.callback("CREATED", path)
                    elif mtime > self.state[path]:
                        self.callback("MODIFIED", path)

                # Detect Deleted Files
                for path in self.state:
                    if path not in current_state:
                        self.callback("DELETED", path)

                self.state = current_state
            except Exception as e:
                print(f"[Observer Warning] {e}", file=sys.stderr)
