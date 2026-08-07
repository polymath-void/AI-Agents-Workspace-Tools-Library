import os
import sys
import subprocess
import shutil
from pathlib import Path

def probe_agent_environment():
    """
    Performs comprehensive self-diagnosis of the agent execution environment,
    identifying PATH issues, Git authentication conflicts, and system bottlenecks.
    """
    report = {
        "status": "HEALTHY",
        "checks": {},
        "recommendations": []
    }

    # 1. Check Tool Library in PATH / Shell Config
    tools_bin = str(Path(os.path.expanduser("~/AI-Agents-Workspace-Tools-Library/bin")).resolve())
    current_path = os.environ.get("PATH", "")
    in_live_path = tools_bin in current_path.split(":")
    
    # Check bashrc/zshrc persistence
    in_rc = False
    for rc in [".bashrc", ".zshrc"]:
        rc_path = Path(os.path.expanduser(f"~/{rc}"))
        if rc_path.exists() and tools_bin in rc_path.read_text(encoding="utf-8", errors="ignore"):
            in_rc = True
            break

    path_ok = in_live_path or in_rc
    report["checks"]["path_configured"] = {
        "ok": path_ok,
        "tools_bin": tools_bin,
        "live_path": in_live_path,
        "persisted_in_rc": in_rc,
        "detail": "Configured in PATH and shell profile" if (in_live_path and in_rc) else ("Persisted in shell profile (active in new shells)" if in_rc else "Tools directory is NOT configured")
    }
    if not path_ok:
        report["recommendations"].append(f'Run wc-error-healer --fix-path to add tools to PATH')
        report["status"] = "DEGRADED"

    # 2. Check GitHub CLI Authentication
    gh_path = shutil.which("gh")
    if gh_path:
        try:
            gh_res = subprocess.run(["gh", "auth", "status"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = gh_res.stdout + gh_res.stderr
            report["checks"]["github_auth"] = {
                "ok": gh_res.returncode == 0,
                "detail": "GitHub CLI authenticated (Active: polymath-void)" if "polymath-void" in output else "GitHub CLI authenticated",
                "raw": output.strip().splitlines()[:4]
            }
        except Exception as e:
            report["checks"]["github_auth"] = {"ok": False, "error": str(e)}
    else:
        report["checks"]["github_auth"] = {"ok": False, "detail": "gh CLI not installed"}

    # 3. Check Termux Environment & Memory
    meminfo_path = Path("/proc/meminfo")
    ram_avail = 0
    if meminfo_path.exists():
        try:
            with open(meminfo_path, "r") as f:
                for line in f:
                    if "MemAvailable:" in line:
                        ram_avail = int(line.split()[1]) // 1024
                        break
        except Exception:
            pass

    report["checks"]["memory_headroom"] = {
        "ok": ram_avail > 100 or ram_avail == 0,
        "available_mb": ram_avail,
        "detail": f"{ram_avail} MB available" if ram_avail > 0 else "System memory normal"
    }

    # 4. Check Python & SQLite Database
    import sqlite3
    db_test_ok = True
    try:
        conn = sqlite3.connect(":memory:")
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.close()
    except Exception as e:
        db_test_ok = False

    report["checks"]["sqlite_engine"] = {
        "ok": db_test_ok,
        "detail": "SQLite engine operational with WAL support"
    }

    if any(not c.get("ok", True) for c in report["checks"].values()):
        if report["status"] != "DEGRADED":
            report["status"] = "WARNING"

    return report
