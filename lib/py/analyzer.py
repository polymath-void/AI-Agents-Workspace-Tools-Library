import ast
import os
from pathlib import Path

IGNORE_DIRS = {'.git', '__pycache__', 'venv', '.venv', 'node_modules', '.gradle', 'build', '.cache'}

class ComplexityAnalyzer:
    """
    Calculates cyclomatic complexity and structural metrics for Python source files.
    """
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.raw_content = ""
        self.tree = None
        self._load()

    def _load(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='replace') as f:
                self.raw_content = f.read()
            self.tree = ast.parse(self.raw_content)
        except Exception:
            self.tree = None

    def calculate_complexity(self):
        if self.tree is None:
            return 1
        complexity = 1
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler, ast.With, ast.BoolOp, ast.IfExp, ast.Match)):
                complexity += 1
        return complexity

    def calculate_metrics(self):
        lines = self.raw_content.splitlines()
        loc = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
        
        functions = 0
        classes = 0
        if self.tree is not None:
            for node in ast.walk(self.tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    functions += 1
                elif isinstance(node, ast.ClassDef):
                    classes += 1

        return {
            "loc": loc,
            "total_lines": len(lines),
            "functions": functions,
            "classes": classes,
            "complexity": self.calculate_complexity()
        }

def analyze_workspace(root_path, mode="complexity"):
    """
    Scans for Python files in workspace and reports metrics.
    """
    results = {}
    root = Path(root_path).resolve()
    if not root.exists():
        return results

    for path in root.rglob('*.py'):
        if any(ignored in path.parts for ignored in IGNORE_DIRS):
            continue
        try:
            analyzer = ComplexityAnalyzer(path)
            if mode == "metrics":
                results[str(path)] = analyzer.calculate_metrics()
            else:
                results[str(path)] = analyzer.calculate_complexity()
        except Exception as e:
            results[str(path)] = f"Error: {e}"
    return results

def workspace_summary(root_path):
    """
    Computes aggregated complexity and LOC statistics for the workspace.
    """
    metrics_map = analyze_workspace(root_path, mode="metrics")
    total_files = len(metrics_map)
    total_loc = 0
    total_functions = 0
    total_classes = 0
    complexities = []
    max_complexity = 0
    max_file = "None"

    for file_path, data in metrics_map.items():
        if isinstance(data, dict):
            total_loc += data.get("loc", 0)
            total_functions += data.get("functions", 0)
            total_classes += data.get("classes", 0)
            c = data.get("complexity", 1)
            complexities.append(c)
            if c > max_complexity:
                max_complexity = c
                max_file = Path(file_path).name

    avg_complexity = (sum(complexities) / len(complexities)) if complexities else 0.0

    return {
        "total_files": total_files,
        "total_loc": total_loc,
        "total_functions": total_functions,
        "total_classes": total_classes,
        "avg_complexity": avg_complexity,
        "max_complexity": max_complexity,
        "max_complexity_file": max_file
    }
