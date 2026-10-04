#!/data/data/com.termux/files/usr/bin/env bash

# gemini_safe.sh - Stability wrapper for gemini-cli in Termux

# 1. Cleanup stale processes before starting
pkill -f "node.*gemini" 2>/dev/null

# 2. Reset terminal state just in case
stty sane

# 3. Define optimized Node.js execution
# Limiting memory usage to 2GB to prevent Android OOM kills
# Use --trace-warnings to see if there are internal JS issues
NODE_OPTIONS="--max-old-space-size=2048 --trace-warnings"

echo "[gemini_safe] Launching gemini..."
gemini "$@"

# 4. Cleanup/Reset after execution (if it exited cleanly or crashed)
exit_code=$?
stty sane
if [ $exit_code -ne 0 ]; then
    echo "[gemini_safe] Gemini exited with code $exit_code. Terminal state restored."
fi
exit $exit_code
