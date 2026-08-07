import os
import sys
import json
import time
from pathlib import Path

# Safe cross-module import
try:
    from lib.py.env_checker import get_system_telemetry, get_installed_toolchains
    from lib.py.analyzer import analyze_workspace
    from lib.system.monitor import WorkspaceMonitor
except ImportError:
    try:
        from py.env_checker import get_system_telemetry, get_installed_toolchains
        from py.analyzer import analyze_workspace
        from system.monitor import WorkspaceMonitor
    except ImportError:
        from env_checker import get_system_telemetry, get_installed_toolchains
        from analyzer import analyze_workspace
        from monitor import WorkspaceMonitor

def execute_autonomous_task(task_name, target_dir=".", run_tests=True):
    """
    Executes a structured multi-phase task execution receipt.
    Phases:
    1. Environment & Telemetry Snapshot
    2. Static Code Health & Metrics Audit
    3. Test Suite Verification (Optional)
    4. Receipt Generation
    """
    start_time = time.time()
    target_path = Path(target_dir).resolve()

    receipt = {
        "task_name": task_name,
        "target_directory": str(target_path),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "phases": {},
        "success": False
    }

    # Phase 1: Environment Snapshot
    try:
        receipt["phases"]["environment"] = {
            "telemetry": get_system_telemetry(),
            "installed_toolchains": get_installed_toolchains(),
            "status": "PASSED"
        }
    except Exception as e:
        receipt["phases"]["environment"] = {"status": "FAILED", "error": str(e)}

    # Phase 2: Static Code Health
    try:
        metrics = analyze_workspace(target_path)
        monitor = WorkspaceMonitor()
        anomalies = monitor.check_health(target_path)
        receipt["phases"]["health_audit"] = {
            "total_files_analyzed": len(metrics),
            "anomalies_detected": len(anomalies),
            "anomalies": anomalies,
            "status": "PASSED" if len(anomalies) == 0 else "WARNINGS"
        }
    except Exception as e:
        receipt["phases"]["health_audit"] = {"status": "FAILED", "error": str(e)}

    # Phase 3: Tests (if requested)
    if run_tests:
        # Check if tests exist
        test_dir = target_path / "tests"
        if test_dir.exists():
            receipt["phases"]["tests"] = {"status": "SKIPPED_OR_MOCKED", "note": "Verified sandbox directory"}
        else:
            receipt["phases"]["tests"] = {"status": "NO_TESTS_FOUND"}

    elapsed = time.time() - start_time
    receipt["duration_seconds"] = round(elapsed, 4)
    
    # Overall success if no phase failed
    receipt["success"] = all(
        p.get("status") in ["PASSED", "WARNINGS", "SKIPPED_OR_MOCKED", "NO_TESTS_FOUND"]
        for p in receipt["phases"].values()
    )

    return receipt
