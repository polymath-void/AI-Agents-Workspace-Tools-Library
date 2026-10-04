#!/usr/bin/env bash
# Push Antigravity Agent & Bridge to Termux

echo "=== Pushing Antigravity Bridge Client to Termux ==="

mkdir -p ~/.local/bin

cat << 'EOF' > ~/.local/bin/agy-remote
#!/usr/bin/env bash
# Antigravity Remote Agent Client for Termux
PC_IP="192.168.0.124"
BRIDGE_PORT="8090"

if [ -z "$1" ]; then
    echo "Usage: agy-remote \"<command or prompt>\""
    exit 1
fi

COMMAND="$*"

curl -s -X POST "http://${PC_IP}:${BRIDGE_PORT}/exec" \
  -H "Content-Type: application/json" \
  -d "{\"command\": $(jq -R -s . <<< "$COMMAND")}" | jq -r '.stdout // .error'
EOF

chmod +x ~/.local/bin/agy-remote

if ! grep -q ".local/bin" ~/.bashrc 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
fi

echo -e "\033[38;2;129;201;149m✨ Antigravity Agent Pushed to Termux Successfully!\033[0m"
echo -e "\033[38;2;138;180;248mUsage in Termux: agy-remote \"ls -la\"\033[0m"
