import os
import re
import shutil
import time
from pathlib import Path

IGNORE_DIRS = {'.git', 'node_modules', 'build', '.gradle', '__pycache__', '.cache', 'bin'}

def batch_code_replace(root_path, target_pattern, replacement, extensions=None, is_regex=False, dry_run=False, create_backup=True):
    """
    Safely modifies code across multiple files with regex/literal matching,
    creating atomic backups for rollback capability.
    """
    root = Path(root_path).resolve()
    results = {
        "modified_files": [],
        "total_occurrences": 0,
        "backup_dir": None,
        "dry_run": dry_run
    }

    if not root.exists():
        return results

    flags = re.MULTILINE
    pattern = re.compile(target_pattern if is_regex else re.escape(target_pattern), flags)

    ext_set = set(e.lower().lstrip(".") for e in extensions) if extensions else None

    # Prepare backup directory if needed
    if not dry_run and create_backup:
        backup_base = root / ".wc_backups" / f"backup_{int(time.time())}"
        backup_base.mkdir(parents=True, exist_ok=True)
        results["backup_dir"] = str(backup_base)

    for path in root.rglob("*"):
        if any(ignored in path.parts for ignored in IGNORE_DIRS):
            continue
        if ".wc_backups" in path.parts:
            continue
        if not path.is_file() or path.is_symlink():
            continue
        if ext_set and path.suffix.lower().lstrip(".") not in ext_set:
            continue

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except (OSError, PermissionError):
            continue

        matches = pattern.findall(content)
        if matches:
            count = len(matches)
            results["total_occurrences"] += count
            results["modified_files"].append({"file": str(path), "occurrences": count})

            if not dry_run:
                # Create backup
                if create_backup:
                    rel = path.relative_to(root)
                    bak_file = Path(results["backup_dir"]) / rel
                    bak_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(path, bak_file)

                # Apply replacement
                new_content = pattern.sub(replacement, content)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)

    return results

def inject_import(root_path, import_statement, extension="kt", dry_run=False):
    """
    Injects an import statement at the top of code files if not already present.
    """
    root = Path(root_path).resolve()
    injected_files = []
    ext = extension.lstrip(".")

    for path in root.rglob(f"*.{ext}"):
        if any(ignored in path.parts for ignored in IGNORE_DIRS):
            continue
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            continue

        content = "".join(lines)
        if import_statement.strip() in content:
            continue

        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("package "):
                insert_idx = i + 1
            elif line.startswith("import "):
                insert_idx = i + 1

        if not dry_run:
            lines.insert(insert_idx, f"{import_statement.strip()}\n")
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(lines)

        injected_files.append(str(path))

    return injected_files
