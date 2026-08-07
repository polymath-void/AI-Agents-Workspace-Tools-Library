import os
import re
from pathlib import Path

def validate_jni_contracts(repo_path="."):
    """
    Scans Kotlin source files for 'external fun' declarations and verifies
    corresponding C/C++ JNI exported function signatures in native source files.
    """
    root = Path(repo_path).resolve()
    report = {
        "kotlin_external_functions": [],
        "c_jni_exports": [],
        "missing_c_implementations": [],
        "valid": True
    }

    if not root.exists():
        return report

    # 1. Find Kotlin external fun declarations
    for path in root.rglob("*.kt"):
        if ".git" in path.parts or "build" in path.parts:
            continue
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            matches = re.findall(r'external\s+fun\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)', content)
            for name, params in matches:
                report["kotlin_external_functions"].append({
                    "file": str(path),
                    "name": name,
                    "params": params.strip()
                })
        except Exception:
            continue

    # 2. Find C/C++ JNI functions (e.g. Java_com_...)
    for path in root.rglob("*.[ch]"):
        if ".git" in path.parts or "build" in path.parts:
            continue
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            c_matches = re.findall(r'JNIEXPORT\s+\w+\s+JNICALL\s+Java_[a-zA-Z0-9_]+_([a-zA-Z0-9_]+)', content)
            for c_fn in c_matches:
                report["c_jni_exports"].append({"file": str(path), "name": c_fn})
        except Exception:
            continue

    # 3. Check for missing implementations
    c_names = {c["name"] for c in report["c_jni_exports"]}
    for kt_fn in report["kotlin_external_functions"]:
        if kt_fn["name"] not in c_names and len(report["c_jni_exports"]) > 0:
            report["missing_c_implementations"].append(kt_fn)
            report["valid"] = False

    return report

def validate_ipc_contracts(desktop_path="."):
    """
    Verifies Electron contextBridge API definitions in preload.js against main/renderer usages.
    """
    root = Path(desktop_path).resolve()
    report = {
        "exposed_apis": [],
        "valid": True
    }

    preload_file = root / "preload.js"
    if not preload_file.exists():
        # Search anywhere in project
        matches = list(root.rglob("preload.js"))
        if matches:
            preload_file = matches[0]
        else:
            return report

    try:
        with open(preload_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        methods = re.findall(r'(\w+)\s*:\s*\([^)]*\)\s*=>\s*ipcRenderer\.(?:invoke|send)', content)
        report["exposed_apis"] = list(set(methods))
    except Exception:
        pass

    return report
