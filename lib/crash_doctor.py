import os
import re
from pathlib import Path

def parse_stacktrace(trace_text):
    """
    Parses Java/Kotlin and POSIX C crash logs, extracting the root cause and line numbers.
    """
    results = {
        "exception_type": "Unknown",
        "message": "",
        "root_cause_file": None,
        "root_cause_line": None,
        "stack_frames": []
    }

    lines = trace_text.splitlines()
    for line in lines:
        # Match Java/Kotlin Exception: java.lang.NullPointerException: ...
        exc_match = re.search(r'([a-zA-Z0-9_.]+(?:Exception|Error)):?\s*(.*)', line)
        if exc_match and results["exception_type"] == "Unknown":
            results["exception_type"] = exc_match.group(1)
            results["message"] = exc_match.group(2).strip()

        # Match stack frame: at com.piuu.launcher.MainActivity.onCreate(MainActivity.kt:123)
        frame_match = re.search(r'at\s+([a-zA-Z0-9_.$]+)\(([a-zA-Z0-9_.]+):(\d+)\)', line)
        if frame_match:
            frame = {
                "method": frame_match.group(1),
                "file": frame_match.group(2),
                "line": int(frame_match.group(3))
            }
            results["stack_frames"].append(frame)
            if not results["root_cause_file"]:
                results["root_cause_file"] = frame["file"]
                results["root_cause_line"] = frame["line"]

        # Match native crash: signal 11 (SIGSEGV), code 1 (SEGV_MAPERR)
        sig_match = re.search(r'signal\s+(\d+)\s*\((SIG\w+)\)', line)
        if sig_match:
            results["exception_type"] = f"Native Signal {sig_match.group(1)} ({sig_match.group(2)})"
            results["message"] = line.strip()

    return results

def analyze_crash_log(file_path):
    """
    Reads a crash log or build output file and diagnoses the failure.
    """
    path = Path(file_path).resolve()
    if not path.exists():
        return {"error": f"File not found: {file_path}"}

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        return parse_stacktrace(content)
    except Exception as e:
        return {"error": str(e)}
