import os
import sys
import subprocess
import re
from pathlib import Path

def auto_heal_error(error_message):
    """
    Analyzes error messages and automatically applies self-healing remediation routines.
    """
    fixes_applied = []

    # 1. Detect Git 403 Forbidden / Permission Denied
    if "Permission to" in error_message and ("denied" in error_message or "403" in error_message):
        # Extract target user from repo if possible
        user_match = re.search(r'Permission to ([^/]+)/', error_message)
        target_user = user_match.group(1) if user_match else "polymath-void"
        
        # Switch gh user
        res = subprocess.run(["gh", "auth", "switch", "--user", target_user], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            fixes_applied.append(f"Switched active GitHub CLI account to '{target_user}'")

    # 2. Detect Shebang missing in Termux (/usr/bin/env: No such file)
    if "No such file or directory" in error_message and ("env" in error_message or "python" in error_message):
        from env_checker import batch_fix_shebangs
        fixed = batch_fix_shebangs(os.path.expanduser("~/AI-Agents-Workspace-Tools-Library/bin"))
        if fixed:
            fixes_applied.append(f"Repaired Termux shebangs on {len(fixed)} binary files")

    # 3. Detect SQLite database locked
    if "database is locked" in error_message or "busy" in error_message:
        # Check ~/.wie_memory.db-wal
        for p in Path(os.path.expanduser("~")).glob("*.db-wal"):
            try:
                p.unlink()
                fixes_applied.append(f"Cleared stale SQLite WAL lock: {p.name}")
            except Exception:
                pass

    return fixes_applied

def ensure_path_configured():
    """
    Ensures ~/AI-Agents-Workspace-Tools-Library/bin is added to ~/.bashrc and ~/.zshrc.
    """
    tools_bin = os.path.expanduser("~/AI-Agents-Workspace-Tools-Library/bin")
    export_line = f'export PATH="{tools_bin}:$PATH"'
    modified_rcs = []

    for rc_name in [".bashrc", ".zshrc"]:
        rc_path = Path(os.path.expanduser(f"~/{rc_name}"))
        content = rc_path.read_text(encoding="utf-8", errors="ignore") if rc_path.exists() else ""
        if export_line not in content and tools_bin not in content:
            with open(rc_path, "a", encoding="utf-8") as f:
                f.write(f"\n# AI Agents Workspace Tools Library\n{export_line}\n")
            modified_rcs.append(rc_name)

    return modified_rcs
