import re
import sys
from pathlib import Path

def clean_ansi(text):
    """Strips terminal ANSI escape color codes."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def compress_log_trace(log_content, max_lines=40):
    """
    Compresses verbose logs by deduplicating repetitive lines and isolating error headers.
    """
    clean_text = clean_ansi(log_content)
    lines = [l.strip() for l in clean_text.splitlines() if l.strip()]
    if not lines:
        return ""

    deduped = []
    prev_line = None
    rep_count = 0

    for line in lines:
        if line == prev_line:
            rep_count += 1
        else:
            if rep_count > 1:
                deduped.append(f"... (repeated {rep_count} times)")
            rep_count = 1
            deduped.append(line)
            prev_line = line

    if rep_count > 1:
        deduped.append(f"... (repeated {rep_count} times)")

    # If still too long, prioritize start and tail
    if len(deduped) > max_lines:
        half = max_lines // 2
        return "\n".join(deduped[:half] + [f"\n... [Truncated {len(deduped) - max_lines} lines for token efficiency] ...\n"] + deduped[-half:])
    
    return "\n".join(deduped)

def pack_agent_context(files_or_logs_dict):
    """
    Packs multiple file contents or task outputs into a dense token-efficient bundle.
    """
    packed = []
    for title, content in files_or_logs_dict.items():
        compressed = compress_log_trace(content, max_lines=25)
        packed.append(f"### 📦 Context Node: `{title}` ({len(compressed)} chars)\n```\n{compressed}\n```")
    return "\n\n".join(packed)
