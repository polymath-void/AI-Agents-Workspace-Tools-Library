import subprocess
import time
import urllib.request
import json

class NativeAIEngine:
    """Manages the lifecycle and execution of the Native AI Engine (phi-3-mini-q4.gguf)."""
    
    def __init__(self, port: int = 57160):
        self.port = port
        self.url = f"http://127.0.0.1:{port}"

    def is_running(self) -> bool:
        """Check if the native_ai_engine process is active."""
        try:
            res = subprocess.run(
                ["su", "-c", "pgrep -f native_ai_engine"],
                capture_output=True,
                text=True
            )
            return res.returncode == 0
        except Exception:
            return False

    def wake(self) -> bool:
        """Wake up the native engine daemon via Magisk init."""
        if self.is_running():
            return True
        try:
            subprocess.run(["su", "-c", "start native_ai_engine"], check=True)
            # Wait for HTTP server to bind
            for _ in range(5):
                time.sleep(1)
                try:
                    req = urllib.request.Request(f"{self.url}/health", method="GET")
                    with urllib.request.urlopen(req, timeout=1) as resp:
                        if resp.status == 200:
                            return True
                except Exception:
                    pass
            return False
        except Exception:
            return False

    def sleep(self) -> bool:
        """Gracefully shut down and stop the native engine."""
        try:
            req = urllib.request.Request(
                f"{self.url}/shutdown",
                data=b"shutdown",
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=2):
                pass
        except Exception:
            pass
        try:
            subprocess.run(["su", "-c", "stop native_ai_engine"], check=True)
            return True
        except Exception:
            return False

    def query(self, prompt: str) -> str:
        """Query the native engine with a prompt using the Wake -> Execute -> Sleep lifecycle."""
        if not self.wake():
            return "[Error] Failed to wake up Native AI Engine."
        try:
            req = urllib.request.Request(
                self.url,
                data=prompt.encode("utf-8"),
                method="POST",
                headers={"Content-Type": "text/plain"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8")
        except Exception as e:
            return f"[Error] Query failed: {e}"
        finally:
            self.sleep()
