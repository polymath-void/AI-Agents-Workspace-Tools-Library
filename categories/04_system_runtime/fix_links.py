#!/usr/bin/env python3
import os

HOME = "/data/data/com.termux/files/home"

# Define the exact mapping of what was moved where
MAPPING = {
    f"{HOME}/agent": f"{HOME}/Projects/local/agent",
    f"{HOME}/unified-agent": f"{HOME}/Projects/local/unified-agent",
    f"{HOME}/hybrid-engine": f"{HOME}/Projects/polymath-void/hybrid-engine",
    
    f"{HOME}/agents-playground": f"{HOME}/Projects/Planned/agents-playground",
    f"{HOME}/mission-agent-reborn": f"{HOME}/Projects/Planned/mission-agent-reborn",
    f"{HOME}/saas-agent-v2": f"{HOME}/Projects/Planned/saas-agent-v2",
    f"{HOME}/teamwork_projects": f"{HOME}/Projects/Planned/teamwork_projects",
    f"{HOME}/test-sandbox": f"{HOME}/Projects/Planned/test-sandbox",
    f"{HOME}/sentinel_dashboard": f"{HOME}/Projects/Planned/sentinel_dashboard",
    
    f"{HOME}/AI-Agents-Workspace-Tools-Library": f"{HOME}/Workspace/Tools/AI-Agents-Workspace-Tools-Library",
    f"{HOME}/skills-workspace": f"{HOME}/Workspace/Tools/skills-workspace",
    f"{HOME}/tools": f"{HOME}/Workspace/Tools/tools",
    f"{HOME}/scripts": f"{HOME}/Workspace/Scripts",
    f"{HOME}/AGY": f"{HOME}/Workspace/Tools/AGY",
    f"{HOME}/termux-antigravity-cli-agy": f"{HOME}/Workspace/Tools/termux-antigravity-cli-agy"
}

# Directories to scan
SCAN_DIRS = [
    f"{HOME}/Projects",
    f"{HOME}/Workspace",
    f"{HOME}/.gemini"
]

# Extensions that are safe to modify (text files)
SAFE_EXTS = {
    ".sh", ".py", ".js", ".ts", ".json", ".md", ".txt", ".yml", ".yaml", 
    ".toml", ".ini", ".conf", ".bash", ".zsh", ".env", ".rs", ".go"
}

def is_text_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    return ext in SAFE_EXTS or os.path.basename(filepath) in ["Makefile", "Dockerfile"]

def fix_links():
    total_files_fixed = 0
    total_replacements = 0

    for scan_dir in SCAN_DIRS:
        if not os.path.exists(scan_dir):
            continue
            
        for root, dirs, files in os.walk(scan_dir):
            # Skip hidden directories like .git
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                filepath = os.path.join(root, file)
                if not is_text_file(filepath):
                    continue
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                except (UnicodeDecodeError, PermissionError, FileNotFoundError):
                    continue
                
                new_content = content
                for old_path, new_path in MAPPING.items():
                    # Replace absolute paths
                    if old_path in new_content:
                        new_content = new_content.replace(old_path, new_path)
                    
                    # Replace relative paths (like ~/Projects/local/agent)
                    old_rel = old_path.replace(HOME, "~")
                    new_rel = new_path.replace(HOME, "~")
                    if old_rel in new_content:
                        new_content = new_content.replace(old_rel, new_rel)

                if new_content != content:
                    try:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"[+] Fixed paths in: {filepath}")
                        total_files_fixed += 1
                        total_replacements += 1
                    except PermissionError:
                        print(f"[-] Permission denied writing to: {filepath}")

    print(f"\nDone! Fixed {total_files_fixed} files.")

if __name__ == "__main__":
    fix_links()
