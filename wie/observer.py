import time
import os
from pathlib import Path

IGNORE_DIRS = {'.git', '__pycache__', 'node_modules', '.gradle', '.cache'}

class PollingObserver:
    def __init__(self, watch_path, callback, interval=5):
        self.watch_path = Path(watch_path).resolve()
        self.callback = callback
        self.interval = interval
        self.state = self._scan()  # Properly initialize starting state

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

    def run(self):
        print(f"Observation Layer started on {self.watch_path} (polling every {self.interval}s)")
        while True:
            try:
                time.sleep(self.interval)
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
            except KeyboardInterrupt:
                print("\nObservation Layer stopped.")
                break
            except Exception as e:
                print(f"Observer warning: {e}")
