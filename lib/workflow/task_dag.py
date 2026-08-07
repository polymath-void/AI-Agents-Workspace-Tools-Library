import time
import subprocess
import concurrent.futures
import json
from pathlib import Path

class TaskDAG:
    """
    Dependency-aware multi-task DAG executor for parallel and sequential agent workflows.
    """
    def __init__(self):
        self.tasks = {}       # task_id -> { "name": ..., "cmd": ..., "deps": [...], "status": "PENDING" }
        self.results = {}     # task_id -> { "success": bool, "output": str, "duration": float }

    def add_task(self, task_id, name, command, dependencies=None):
        self.tasks[task_id] = {
            "name": name,
            "cmd": command,
            "deps": dependencies or [],
            "status": "PENDING"
        }

    def _execute_single_task(self, task_id, cwd="."):
        task = self.tasks[task_id]
        task["status"] = "RUNNING"
        start = time.perf_counter()

        cmd = task["cmd"]
        if isinstance(cmd, str):
            cmd_list = cmd.split()
        else:
            cmd_list = cmd

        try:
            res = subprocess.run(
                cmd_list,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=300
            )
            duration = round(time.perf_counter() - start, 3)
            success = res.returncode == 0
            output = res.stdout if success else (res.stderr or res.stdout)
            
            task["status"] = "COMPLETED" if success else "FAILED"
            self.results[task_id] = {
                "success": success,
                "output": output.strip(),
                "duration": duration,
                "exit_code": res.returncode
            }
            return success
        except Exception as e:
            duration = round(time.perf_counter() - start, 3)
            task["status"] = "ERROR"
            self.results[task_id] = {
                "success": False,
                "output": str(e),
                "duration": duration,
                "exit_code": -1
            }
            return False

    def run_all(self, max_workers=4, cwd="."):
        """
        Executes all tasks respecting DAG dependencies using a thread/process worker pool.
        """
        completed = set()
        failed = set()
        start_time = time.perf_counter()

        while len(completed) + len(failed) < len(self.tasks):
            # Find tasks ready to run (all deps completed successfully)
            ready_tasks = [
                t_id for t_id, t_info in self.tasks.items()
                if t_info["status"] == "PENDING" and all(d in completed for d in t_info["deps"])
            ]

            # If no tasks ready but unfinished tasks exist, check if blocked by failures
            if not ready_tasks:
                for t_id, t_info in self.tasks.items():
                    if t_info["status"] == "PENDING" and any(d in failed for d in t_info["deps"]):
                        t_info["status"] = "BLOCKED"
                        failed.add(t_id)
                        self.results[t_id] = {
                            "success": False,
                            "output": f"Blocked by failed dependencies: {[d for d in t_info['deps'] if d in failed]}",
                            "duration": 0.0,
                            "exit_code": -1
                        }
                if len(completed) + len(failed) >= len(self.tasks):
                    break
                if not ready_tasks:
                    # Circular dependency or deadlock
                    break

            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_task = {
                    executor.submit(self._execute_single_task, t_id, cwd): t_id
                    for t_id in ready_tasks
                }
                for future in concurrent.futures.as_completed(future_to_task):
                    t_id = future_to_task[future]
                    success = future.result()
                    if success:
                        completed.add(t_id)
                    else:
                        failed.add(t_id)

        total_duration = round(time.perf_counter() - start_time, 3)
        return {
            "total_tasks": len(self.tasks),
            "completed": len(completed),
            "failed": len(failed),
            "total_duration": total_duration,
            "results": self.results
        }
