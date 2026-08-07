import os
import shutil
from pathlib import Path

FORBIDDEN_ROOTS = {'/', '/root', '/home', os.path.expanduser('~')}

def sanitize_workspace(root_path, patterns_to_remove, dry_run=False):
    """
    Identifies and safely removes build artifacts, unused temporary files, 
    or orphan dependencies based on defined patterns.
    """
    root = Path(root_path).resolve()
    if not root.exists() or not root.is_dir():
        return []

    # Safeguard against accidental deletion of root or home directory
    if str(root) in FORBIDDEN_ROOTS:
        raise ValueError(f"Safety Error: Cannot run sanitize on system root or home directory: {root}")

    removed_items = []
    matched_paths = set()

    for pattern in patterns_to_remove:
        # Prevent dangerous wildcards that would wipe the entire repo
        if pattern in ('*', '.', '..', '/', '**'):
            continue
        try:
            for item in root.rglob(pattern):
                # Don't delete .git directory or the root directory itself
                if '.git' in item.parts or item == root:
                    continue
                matched_paths.add(item)
        except (OSError, PermissionError):
            continue

    # Process files first, then directories sorted by deepest path first
    sorted_items = sorted(matched_paths, key=lambda p: (p.is_dir() if p.exists() else False, -len(p.parts)))

    for item in sorted_items:
        try:
            if not item.exists():
                continue
            if dry_run:
                removed_items.append(str(item))
            elif item.is_file() or item.is_symlink():
                item.unlink(missing_ok=True)
                removed_items.append(str(item))
            elif item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
                removed_items.append(str(item))
        except (OSError, PermissionError):
            continue

    return removed_items
