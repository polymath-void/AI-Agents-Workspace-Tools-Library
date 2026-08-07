import time
import subprocess
import os
import resource

def run_benchmark(command_list, cwd=".", iterations=3, max_allowed_seconds=5.0):
    """
    Runs command_list multiple times, measuring wall time, user time, system time, and peak memory.
    """
    times = []
    return_codes = []
    
    for _ in range(iterations):
        start_time = time.perf_counter()
        res = subprocess.run(
            command_list,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        elapsed = time.perf_counter() - start_time
        times.append(elapsed)
        return_codes.append(res.returncode)

    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    all_success = all(c == 0 for c in return_codes)

    return {
        "command": " ".join(command_list),
        "iterations": iterations,
        "avg_seconds": round(avg_time, 4),
        "min_seconds": round(min_time, 4),
        "max_seconds": round(max_time, 4),
        "success": all_success,
        "meets_threshold": avg_time <= max_allowed_seconds
    }
