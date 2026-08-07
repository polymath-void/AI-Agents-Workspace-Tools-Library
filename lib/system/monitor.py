import json
import os
from pathlib import Path

try:
    from lib.py.analyzer import analyze_workspace
except ImportError:
    try:
        from py.analyzer import analyze_workspace
    except ImportError:
        from analyzer import analyze_workspace

class WorkspaceMonitor:
    def __init__(self, config=None):
        self.config = config or {
            "max_file_lines": 500,
            "max_cyclomatic_complexity": 15,
            "forbidden_patterns": ["TODO_REPAIR", "FIXME_URGENT", "HACK_BYPASS"]
        }

    def check_health(self, target_dir):
        target = Path(target_dir).resolve()
        anomalies = []
        
        file_metrics = analyze_workspace(target, mode="metrics")
        for file_path, m in file_metrics.items():
            if not isinstance(m, dict):
                continue
            if m.get("total_lines", 0) > self.config["max_file_lines"]:
                anomalies.append({
                    "file": file_path,
                    "type": "FILE_TOO_LARGE",
                    "value": m.get("total_lines", 0),
                    "threshold": self.config["max_file_lines"]
                })
            if m.get("complexity", 1) > self.config["max_cyclomatic_complexity"]:
                anomalies.append({
                    "file": file_path,
                    "type": "HIGH_COMPLEXITY",
                    "value": m.get("complexity", 1),
                    "threshold": self.config["max_cyclomatic_complexity"]
                })

        forbidden = self.config["forbidden_patterns"]
        for p in target.rglob("*"):
            if p.is_file() and p.suffix in [".py", ".kt", ".java", ".js", ".ts"]:
                if any(x in p.parts for x in [".git", "build", "dist", "node_modules"]):
                    continue
                try:
                    content = p.read_text(encoding="utf-8", errors="ignore")
                    for pattern in forbidden:
                        if pattern in content:
                            anomalies.append({
                                "file": str(p.relative_to(target)),
                                "type": "FORBIDDEN_PATTERN",
                                "pattern": pattern
                            })
                except Exception:
                    pass

        return anomalies
