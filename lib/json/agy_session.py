import os
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

class AGYSessionInspector:
    """Antigravity AGY session transcript analyzer, token density counter and tool call profiler."""

    @classmethod
    def load_transcript(cls, path: Path) -> List[Dict[str, Any]]:
        """Loads JSONL transcript records from file."""
        if not path.exists():
            return []
        records = []
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        return records

    @classmethod
    def analyze_session(cls, transcript_path: Path) -> Dict[str, Any]:
        """Deep analytics on conversation length, message types, subagents and tool calls."""
        records = cls.load_transcript(transcript_path)
        if not records:
            return {"status": "ERROR", "message": f"Empty or missing transcript: {transcript_path}"}

        step_types = {}
        tool_counts = {}
        subagents_spawned = []
        total_chars = 0
        total_tokens_est = 0
        user_inputs = []

        for r in records:
            st = r.get("type", "UNKNOWN")
            step_types[st] = step_types.get(st, 0) + 1
            
            content = str(r.get("content", ""))
            total_chars += len(content)
            total_tokens_est += len(content) // 4  # ~4 chars per token approximation

            if st == "USER_INPUT":
                user_inputs.append(content[:120])

            # Check tool calls
            for tc in r.get("tool_calls", []):
                tname = tc.get("name", "unknown")
                tool_counts[tname] = tool_counts.get(tname, 0) + 1
                if tname == "invoke_subagent":
                    args = tc.get("args", tc.get("parameters", {}))
                    subs = args.get("Subagents", [])
                    for s in subs:
                        subagents_spawned.append({
                            "type": s.get("TypeName"),
                            "role": s.get("Role"),
                            "model": s.get("Model", "inherit")
                        })

        return {
            "status": "SUCCESS",
            "file": str(transcript_path),
            "total_steps": len(records),
            "approx_tokens": total_tokens_est,
            "total_characters": total_chars,
            "step_distribution": step_types,
            "total_tool_calls": sum(tool_counts.values()),
            "tool_call_breakdown": tool_counts,
            "subagents_spawned": subagents_spawned,
            "recent_user_prompts": user_inputs[-5:]
        }

    @classmethod
    def export_markdown_timeline(cls, transcript_path: Path, output_file: Path) -> Dict[str, Any]:
        """Generates a clean human-readable Markdown summary of the session history."""
        records = cls.load_transcript(transcript_path)
        if not records:
            return {"status": "ERROR", "message": "No transcript records found"}

        md_lines = [
            f"# 📜 Antigravity Session Timeline Report",
            f"**Source File**: `{transcript_path.name}`  ",
            f"**Total Steps**: {len(records)}  ",
            "\n---\n"
        ]

        for r in records:
            idx = r.get("step_index", "?")
            stype = r.get("type", "UNKNOWN")
            src = r.get("source", "AGENT")
            content = str(r.get("content", "")).strip()

            md_lines.append(f"### Step {idx} — [{src}] `{stype}`")
            if content:
                # Truncate large steps for readable timeline
                preview = content if len(content) < 400 else content[:400] + " ... *(truncated)*"
                md_lines.append(f"```text\n{preview}\n```")

            tool_calls = r.get("tool_calls", [])
            if tool_calls:
                md_lines.append("**Tool Calls:**")
                for tc in tool_calls:
                    md_lines.append(f"- 🔧 `{tc.get('name')}`")
            md_lines.append("\n---\n")

        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text("\n".join(md_lines), encoding="utf-8")

        return {
            "status": "SUCCESS",
            "report_file": str(output_file),
            "size_bytes": output_file.stat().st_size
        }
