import os
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

class HermesAdapter:
    """Multi-agent protocol translator bridging Hermes JSON sessions, Antigravity AGY JSONL logs & Gemini CLI."""

    @classmethod
    def parse_agy_jsonl(cls, jsonl_text: str) -> List[Dict[str, Any]]:
        """Parses raw AGY transcript JSONL string into step objects."""
        steps = []
        for line in jsonl_text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                steps.append(json.loads(line))
            except json.JSONDecodeError:
                pass
        return steps

    @classmethod
    def agy_to_hermes(cls, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Translates AGY transcript steps into Hermes standardized agent session schema."""
        hermes_messages = []
        tools_called = []

        for step in steps:
            step_type = step.get("type", "")
            content = step.get("content", "")
            tool_calls = step.get("tool_calls", [])

            if step_type == "USER_INPUT":
                hermes_messages.append({
                    "role": "user",
                    "content": content,
                    "timestamp": step.get("timestamp", time.time())
                })
            elif step_type == "PLANNER_RESPONSE":
                msg = {
                    "role": "assistant",
                    "content": content,
                    "timestamp": step.get("timestamp", time.time())
                }
                if tool_calls:
                    msg["tool_calls"] = [
                        {
                            "name": tc.get("name", "unknown"),
                            "arguments": tc.get("args", tc.get("parameters", {}))
                        }
                        for tc in tool_calls
                    ]
                    tools_called.extend([tc.get("name") for tc in tool_calls if tc.get("name")])
                hermes_messages.append(msg)
            elif step_type == "SYSTEM":
                hermes_messages.append({
                    "role": "system",
                    "content": content,
                    "timestamp": step.get("timestamp", time.time())
                })

        return {
            "protocol": "hermes-agent-v1",
            "message_count": len(hermes_messages),
            "tool_call_count": len(tools_called),
            "unique_tools": sorted(list(set(tools_called))),
            "messages": hermes_messages
        }

    @classmethod
    def hermes_to_agy(cls, hermes_session: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Translates Hermes agent session schema into AGY JSONL step records."""
        messages = hermes_session.get("messages", [])
        steps = []

        for idx, msg in enumerate(messages):
            role = msg.get("role", "user")
            content = msg.get("content", "")
            tool_calls = msg.get("tool_calls", [])

            if role == "user":
                steps.append({
                    "step_index": idx,
                    "source": "USER_EXPLICIT",
                    "type": "USER_INPUT",
                    "status": "DONE",
                    "content": content
                })
            elif role == "assistant":
                step_obj = {
                    "step_index": idx,
                    "source": "MODEL",
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "content": content
                }
                if tool_calls:
                    step_obj["tool_calls"] = [
                        {"name": tc.get("name"), "args": tc.get("arguments", {})}
                        for tc in tool_calls
                    ]
                steps.append(step_obj)
            elif role == "system":
                steps.append({
                    "step_index": idx,
                    "source": "SYSTEM",
                    "type": "SYSTEM",
                    "status": "DONE",
                    "content": content
                })

        return steps

    @classmethod
    def inspect_session(cls, session_data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Provides analytical telemetry for an agent session."""
        if isinstance(session_data, list):
            steps = session_data
        elif isinstance(session_data, dict) and "messages" in session_data:
            steps = cls.hermes_to_agy(session_data)
        else:
            steps = []

        user_count = sum(1 for s in steps if s.get("type") == "USER_INPUT")
        model_count = sum(1 for s in steps if s.get("type") == "PLANNER_RESPONSE")
        tool_count = sum(len(s.get("tool_calls", [])) for s in steps)

        return {
            "total_steps": len(steps),
            "user_prompts": user_count,
            "agent_responses": model_count,
            "total_tool_calls": tool_count,
            "average_response_length": (sum(len(str(s.get("content", ""))) for s in steps) // max(len(steps), 1))
        }
