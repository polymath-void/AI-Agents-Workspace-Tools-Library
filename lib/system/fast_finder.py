import os
import re
from pathlib import Path

DEFAULT_SKIP_DIRS = {
    '.git', 'node_modules', 'build', 'build_artifacts', '.gradle', 
    '__pycache__', '.cache', 'bin', 'obj', '.idea', '.vscode'
}

def fast_search(root_path, query, is_regex=False, case_insensitive=True, extensions=None, context_lines=0, max_results=100):
    """
    Scans files in root_path for query string or regex pattern, skipping build and binary noise.
    """
    root = Path(root_path).resolve()
    results = []
    
    if not root.exists():
        return results

    flags = re.IGNORECASE if case_insensitive else 0
    pattern = re.compile(query if is_regex else re.escape(query), flags)

    ext_set = set(e.lower().lstrip(".") for e in extensions) if extensions else None

    for path in root.rglob("*"):
        if any(ignored in path.parts for ignored in DEFAULT_SKIP_DIRS):
            continue

        if not path.is_file() or path.is_symlink():
            continue

        if ext_set and path.suffix.lower().lstrip(".") not in ext_set:
            continue

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except (OSError, PermissionError):
            continue

        for i, line in enumerate(lines):
            if pattern.search(line):
                match_entry = {
                    "file": str(path),
                    "line_number": i + 1,
                    "line_content": line.rstrip(),
                    "context_before": [lines[j].rstrip() for j in range(max(0, i - context_lines), i)],
                    "context_after": [lines[j].rstrip() for j in range(i + 1, min(len(lines), i + 1 + context_lines))]
                }
                results.append(match_entry)
                if len(results) >= max_results:
                    return results

    return results
