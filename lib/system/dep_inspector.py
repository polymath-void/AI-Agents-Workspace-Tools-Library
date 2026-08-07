import os
import re
import json
from pathlib import Path

IGNORE_DIRS = {'.git', 'node_modules', 'build', '.gradle', '__pycache__', '.cache'}

def inspect_dependencies(root_path):
    """
    Scans the workspace for Gradle, NPM, Python, and Rust dependency manifests.
    """
    root = Path(root_path).resolve()
    manifests = {
        "gradle": [],
        "npm": [],
        "python": [],
        "rust": []
    }

    if not root.exists():
        return manifests

    for path in root.rglob("*"):
        if any(ignored in path.parts for ignored in IGNORE_DIRS):
            continue

        filename = path.name

        # Gradle / Android
        if filename in ("build.gradle", "build.gradle.kts", "libs.versions.toml"):
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                deps = re.findall(r'(?:implementation|api|kapt|annotationProcessor)\s+[\'"]([^\'"]+)[\'"]', content)
                plugins = re.findall(r'(?:id|plugin)\s+[\'"]([^\'"]+)[\'"]', content)
                manifests["gradle"].append({
                    "file": str(path),
                    "dependencies": sorted(set(deps)),
                    "plugins": sorted(set(plugins))
                })
            except Exception:
                pass

        # NPM / Web / Node
        elif filename == "package.json":
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    pkg = json.load(f)
                manifests["npm"].append({
                    "file": str(path),
                    "name": pkg.get("name", "unnamed"),
                    "version": pkg.get("version", "0.0.0"),
                    "dependencies": pkg.get("dependencies", {}),
                    "devDependencies": pkg.get("devDependencies", {})
                })
            except Exception:
                pass

        # Python
        elif filename in ("requirements.txt", "pyproject.toml"):
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
                manifests["python"].append({
                    "file": str(path),
                    "entries": lines
                })
            except Exception:
                pass

        # Rust
        elif filename == "Cargo.toml":
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                deps = re.findall(r'\[dependencies(?:\.[^\]]+)?\]\s*([^\[]+)', content)
                manifests["rust"].append({
                    "file": str(path),
                    "raw_deps": deps[0].strip().splitlines() if deps else []
                })
            except Exception:
                pass

    return manifests
