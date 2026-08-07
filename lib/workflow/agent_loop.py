import time
import subprocess
import os
import sys
from pathlib import Path

# Local imports
try:
    from .agent_probe import probe_agent_environment
    from .agent_memory import AgentMemoryStore
    from .error_healer import auto_heal_error
except (ImportError, ValueError):
    from agent_probe import probe_agent_environment
    from agent_memory import AgentMemoryStore
    from error_healer import auto_heal_error

def run_agent_loop(command_list, target_dir=".", tag="agent_task", max_retries=1):
    """
    Executes an agent task inside a self-healing loop with pre-flight diagnostics,
    automatic rollback snapshots, and error self-repair.
    """
    start_time = time.perf_counter()
    loop_result = {
        "task": " ".join(command_list),
        "target_dir": str(Path(target_dir).resolve()),
        "status": "RUNNING",
        "probe": None,
        "snapshot_id": None,
        "healing_attempts": [],
        "success": False,
        "elapsed_seconds": 0.0
    }

    # Step 1: Pre-flight probe
    probe = probe_agent_environment()
    loop_result["probe"] = probe["status"]

    # Step 2: Create pre-execution snapshot
    try:
        store = AgentMemoryStore()
        snap = store.create_snapshot(target_dir, tag=tag)
        loop_result["snapshot_id"] = snap["snapshot_id"]
    except Exception as e:
        loop_result["snapshot_id"] = f"Snapshot skipped: {e}"

    # Step 3: Execute Command with Retry Loop
    attempt = 0
    while attempt <= max_retries:
        attempt += 1
        res = subprocess.run(
            command_list,
            cwd=target_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if res.returncode == 0:
            loop_result["success"] = True
            loop_result["status"] = "COMPLETED"
            break
        else:
            err_output = res.stderr or res.stdout
            fixes = auto_heal_error(err_output)
            loop_result["healing_attempts"].append({
                "attempt": attempt,
                "error": err_output.strip().splitlines()[-3:],
                "fixes": fixes
            })
            if not fixes:
                # No self-healing routine available
                break

    if not loop_result["success"]:
        loop_result["status"] = "FAILED"

    loop_result["elapsed_seconds"] = round(time.perf_counter() - start_time, 3)
    return loop_result
