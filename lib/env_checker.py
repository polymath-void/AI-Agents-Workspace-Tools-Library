import os
import sys
import shutil
import subprocess
from pathlib import Path

TERMUX_PREFIX = "/data/data/com.termux/files/usr"

def get_system_telemetry():
    """
    Reads hardware, memory, and OS runtime metrics from Linux /proc filesystem.
    """
    telemetry = {
        "is_termux": os.path.exists(TERMUX_PREFIX) or "com.termux" in os.environ.get("PREFIX", ""),
        "prefix": os.environ.get("PREFIX", TERMUX_PREFIX if os.path.exists(TERMUX_PREFIX) else "/usr"),
        "home": os.environ.get("HOME", ""),
        "python_version": sys.version.split()[0],
        "total_ram_mb": 0,
        "free_ram_mb": 0,
        "available_ram_mb": 0,
        "load_avg": []
    }

    # Parse /proc/meminfo
    try:
        if os.path.exists("/proc/meminfo"):
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    parts = line.split(":")
                    if len(parts) == 2:
                        key = parts[0].strip()
                        val = parts[1].strip().split()[0]
                        if key == "MemTotal":
                            telemetry["total_ram_mb"] = round(int(val) / 1024, 1)
                        elif key == "MemFree":
                            telemetry["free_ram_mb"] = round(int(val) / 1024, 1)
                        elif key == "MemAvailable":
                            telemetry["available_ram_mb"] = round(int(val) / 1024, 1)
    except Exception:
        pass

    # Parse /proc/loadavg
    try:
        if os.path.exists("/proc/loadavg"):
            with open("/proc/loadavg", "r") as f:
                telemetry["load_avg"] = f.read().strip().split()[:3]
    except Exception:
        pass

    return telemetry

def get_installed_toolchains():
    """
    Checks availability and version of standard developer toolchains.
    """
    toolchains = {}
    tools_to_check = [
        ("git", ["git", "--version"]),
        ("python3", ["python3", "--version"]),
        ("clang", ["clang", "--version"]),
        ("javac", ["javac", "-version"]),
        ("node", ["node", "--version"]),
        ("npm", ["npm", "--version"]),
        ("cargo", ["cargo", "--version"]),
        ("gh", ["gh", "--version"])
    ]

    for name, cmd in tools_to_check:
        tool_bin = shutil.which(name)
        if tool_bin:
            try:
                res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=3)
                output = res.stdout.strip() or res.stderr.strip()
                first_line = output.splitlines()[0] if output else "Installed"
                toolchains[name] = {"installed": True, "path": tool_bin, "version": first_line}
            except Exception:
                toolchains[name] = {"installed": True, "path": tool_bin, "version": "Available"}
        else:
            toolchains[name] = {"installed": False, "path": None, "version": None}

    return toolchains

def batch_fix_shebangs(directory):
    """
    Scans directory for script files and corrects shebangs for Android Termux environment.
    """
    root = Path(directory).resolve()
    fixed_files = []
    prefix = os.environ.get("PREFIX", TERMUX_PREFIX)
    termux_env_shebang = f"#!{prefix}/bin/env "

    if not root.exists():
        return fixed_files

    for path in root.rglob("*"):
        if any(part.startswith(".") for part in path.parts if part != path.name):
            continue
        if path.is_file() and not path.is_symlink():
            try:
                with open(path, "rb") as f:
                    first_bytes = f.read(128)
                if first_bytes.startswith(b"#!"):
                    line = first_bytes.decode("utf-8", errors="ignore").splitlines()[0]
                    if line.startswith("#!/usr/bin/env ") or line.startswith("#!/bin/bash") or line.startswith("#!/bin/sh"):
                        with open(path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        
                        lines = content.splitlines(keepends=True)
                        if lines:
                            if lines[0].startswith("#!/usr/bin/env "):
                                interp = lines[0][len("#!/usr/bin/env "):]
                                lines[0] = f"#!{prefix}/bin/env {interp}"
                            elif lines[0].startswith("#!/bin/bash"):
                                lines[0] = f"#!{prefix}/bin/bash\n"
                            elif lines[0].startswith("#!/bin/sh"):
                                lines[0] = f"#!{prefix}/bin/sh\n"

                            with open(path, "w", encoding="utf-8") as f:
                                f.writelines(lines)
                            
                            # Ensure executable permission
                            try:
                                path.chmod(path.stat().st_mode | 0o755)
                            except Exception:
                                pass
                            fixed_files.append(str(path))
            except (OSError, PermissionError):
                continue

    return fixed_files
