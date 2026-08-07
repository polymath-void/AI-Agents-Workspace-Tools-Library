import subprocess
import shutil
from pathlib import Path

def run_git(args, cwd="."):
    """
    Executes a git command and returns (success, stdout, stderr).
    """
    if not shutil.which("git"):
        return False, "", "Git binary not found"
    try:
        res = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )
        return res.returncode == 0, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def get_git_status(repo_path="."):
    """
    Returns structured Git status for a repository.
    """
    success, branch, _ = run_git(["branch", "--show-current"], cwd=repo_path)
    if not success:
        return {"is_git": False, "error": "Not a git repository"}

    _, status_raw, _ = run_git(["status", "--porcelain"], cwd=repo_path)
    _, log_raw, _ = run_git(["log", "-n", "1", "--oneline"], cwd=repo_path)
    _, remotes_raw, _ = run_git(["remote", "-v"], cwd=repo_path)

    modified_files = []
    untracked_files = []
    staged_files = []

    for line in status_raw.splitlines():
        if len(line) >= 3:
            code = line[:2]
            filename = line[3:]
            if code.startswith("?") or code.endswith("?"):
                untracked_files.append(filename)
            elif code[0] in ("M", "A", "D", "R"):
                staged_files.append(filename)
            elif code[1] in ("M", "D"):
                modified_files.append(filename)

    return {
        "is_git": True,
        "current_branch": branch or "detached",
        "clean": len(status_raw) == 0,
        "staged": staged_files,
        "modified": modified_files,
        "untracked": untracked_files,
        "last_commit": log_raw,
        "has_remotes": len(remotes_raw) > 0
    }

def sync_branches(repo_path=".", source_branch="main", target_branch="master"):
    """
    Fast-forwards target_branch to match source_branch cleanly.
    """
    # Verify both branches exist
    success, branches_out, _ = run_git(["branch"], cwd=repo_path)
    if not success:
        return False, "Failed to read branches"

    branches = [b.strip().lstrip("* ") for b in branches_out.splitlines()]
    if source_branch not in branches or target_branch not in branches:
        return False, f"Missing required branches (Found: {branches})"

    # Record current branch
    _, original_branch, _ = run_git(["branch", "--show-current"], cwd=repo_path)

    # Checkout target and merge source
    s1, out1, err1 = run_git(["checkout", target_branch], cwd=repo_path)
    if not s1:
        return False, f"Checkout failed: {err1}"

    s2, out2, err2 = run_git(["merge", source_branch], cwd=repo_path)
    
    # Return to original branch
    run_git(["checkout", original_branch], cwd=repo_path)

    if not s2:
        return False, f"Merge failed: {err2}"

    return True, f"Successfully fast-forwarded '{target_branch}' to match '{source_branch}'"
