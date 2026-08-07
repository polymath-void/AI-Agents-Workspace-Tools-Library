import os
import json
from pathlib import Path

DEFAULT_IGNORES = {'.git', '.cache', '__pycache__', 'node_modules', '.gradle', '.idea', '.vscode'}

def scan_directory(root_path, ignore_patterns=None, max_depth=10, current_depth=0):
    """
    Recursively scans a directory and builds a resilient tree structure of the workspace.
    """
    root = Path(root_path).resolve()
    if not root.exists() or not root.is_dir():
        return None

    ignores = set(DEFAULT_IGNORES)
    if ignore_patterns:
        ignores.update(ignore_patterns)

    tree = {
        "name": root.name if root.name else str(root),
        "type": "directory",
        "path": str(root),
        "children": [],
        "total_files": 0,
        "total_dirs": 0,
        "total_size_bytes": 0
    }

    if current_depth >= max_depth:
        return tree

    try:
        entries = sorted(root.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
    except (PermissionError, OSError):
        return tree

    for item in entries:
        if item.name.startswith('.') and item.name not in {'.env.example', '.gitignore'}:
            continue
        if item.name in ignores:
            continue

        try:
            if item.is_dir(follow_symlinks=False):
                child = scan_directory(item, ignore_patterns=ignores, max_depth=max_depth, current_depth=current_depth + 1)
                if child:
                    tree["children"].append(child)
                    tree["total_dirs"] += 1 + child.get("total_dirs", 0)
                    tree["total_files"] += child.get("total_files", 0)
                    tree["total_size_bytes"] += child.get("total_size_bytes", 0)
            elif item.is_file(follow_symlinks=False):
                try:
                    file_size = item.stat().st_size
                except (OSError, PermissionError):
                    file_size = 0
                tree["children"].append({
                    "name": item.name,
                    "type": "file",
                    "path": str(item),
                    "size": file_size
                })
                tree["total_files"] += 1
                tree["total_size_bytes"] += file_size
        except (PermissionError, OSError):
            continue

    return tree

def save_metadata(tree, output_path):
    """
    Saves the directory tree as a JSON file, creating parent directories if needed.
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(tree, f, indent=2)
