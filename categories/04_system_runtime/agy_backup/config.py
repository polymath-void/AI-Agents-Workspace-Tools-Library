import json
import os
from pathlib import Path

HOME = Path(os.environ.get("HOME", "/data/data/com.termux/files/home"))

GDRIVE_FOLDER_NAME = "AGY_Backups"
MAX_BACKUPS = 10

CREDENTIALS_FILE = HOME / ".gemini" / "antigravity-cli" / "gdrive_credentials.json"
TOKEN_FILE = HOME / ".gemini" / "antigravity-cli" / "gdrive_token.json"
CONFIG_FILE = HOME / ".gemini" / "antigravity-cli" / "backup_config.json"
MANIFEST_FILE = HOME / ".gemini" / "antigravity-cli" / "backup_manifest.json"
TEMP_DIR = HOME / ".gemini" / "antigravity-cli" / "scratch" / "agy_backup_tmp"

# Standard known CLI Agent Clients & system paths
KNOWN_CLIENTS = {
    "agy": {
        "name": "Antigravity AGY CLI",
        "path": HOME / ".gemini" / "antigravity-cli",
        "inclusions": [
            "settings.json", "knowledge", "skills", "memory", "history.jsonl",
            "conversations", "conversation_summaries.db", "brain", "mcp_config.json", "mcp"
        ]
    },
    "gemini": {
        "name": "Gemini CLI",
        "path": HOME / ".gemini",
        "inclusions": [
            "GEMINI.md", "config", "gemini-credentials.json", "google_accounts.json",
            "history", "policies", "projects.json", "rules", "settings.json",
            "skills", "state.json", "trustedFolders.json"
        ]
    },
    "hermes": {
        "name": "Hermes Agent CLI",
        "path": HOME / ".hermes",
        "inclusions": ["hermes-agent", "config.json", "sessions", "memories"]
    },
    "termux": {
        "name": "Termux All User Data",
        "path": HOME,
        "inclusions": ["."]  # Includes all Termux home userdata (excluding store/cache paths)
    }
}

# Explicitly excluded store, cache, and heavy media directories
EXCLUDED_PATTERNS = [
    "storage", "store", "downloads", "shared", "cache", ".cache",
    "node_modules", "cli.log", "crashes", "updater", "*.lock", "*.tmp",
    "scratch/agy_backup_tmp", ".git/objects"
]

def load_user_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "enabled_targets": ["agy", "gemini", "termux"],
        "custom_directories": [],
        "excluded_patterns": EXCLUDED_PATTERNS
    }

def save_user_config(config_data):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=2)

def get_active_targets():
    cfg = load_user_config()
    active = {}
    
    for key in cfg.get("enabled_targets", []):
        if key in KNOWN_CLIENTS:
            active[key] = KNOWN_CLIENTS[key]

    for custom_path in cfg.get("custom_directories", []):
        p = Path(custom_path).expanduser()
        name = f"custom_{p.name}"
        active[name] = {
            "name": f"Custom Dir ({p.name})",
            "path": p,
            "inclusions": ["."]
        }
    return active
