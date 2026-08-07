import json
import time
from pathlib import Path

class SwarmDispatcher:
    """
    Orchestration and decision engine for Subagent dispatching and swarm management:
    - Analyzes task criteria to decide whether to spawn subagents
    - Formulates optimal dispatch specifications (Role, Prompt, Workspace mode, Model tier)
    - Manages multi-agent synchronization barriers and consensus aggregation
    """

    DECISION_THRESHOLDS = {
        "MAX_LOCAL_SEARCH_FILES": 10,
        "MAX_LOCAL_PROMPT_TOKENS": 4000,
        "DEEP_RESEARCH_THRESHOLD": True,
        "ISOLATED_EXPERIMENTATION": True
    }

    @staticmethod
    def evaluate_subagent_need(task_description, estimated_files=1, is_exploratory=False, requires_isolation=False):
        """
        Determines whether a subagent should be launched or executed directly in the main turn.
        """
        reasons = []
        should_launch = False
        suggested_type = "self"
        suggested_model = "inherit"
        suggested_workspace = "inherit"

        # Condition 1: Broad, token-heavy codebase survey / web research
        if is_exploratory or "research" in task_description.lower() or estimated_files > 15:
            should_launch = True
            suggested_type = "research"
            suggested_model = "flash"
            reasons.append("Broad exploration / file reading would pollute parent context window.")

        # Condition 2: Risky experimental refactoring / destructive changes
        if requires_isolation or "experimental" in task_description.lower() or "branch" in task_description.lower():
            should_launch = True
            suggested_type = "self"
            suggested_workspace = "branch"
            suggested_model = "pro"
            reasons.append("Experimental code modifications require isolated git branch workspace.")

        # Condition 3: Parallel decoupled tasks (e.g. documentation + test generation)
        if "parallel" in task_description.lower() or "concurrent" in task_description.lower():
            should_launch = True
            suggested_type = "self"
            reasons.append("Decoupled task suitable for concurrent execution.")

        if not should_launch:
            reasons.append("Task is small, targeted, and low token-cost; direct execution is faster.")

        return {
            "should_launch_subagent": should_launch,
            "suggested_type": suggested_type,
            "suggested_model": suggested_model,
            "suggested_workspace": suggested_workspace,
            "rationale": reasons
        }

    @staticmethod
    def build_dispatch_spec(role, task_description, context_frames=None, model="inherit", workspace="inherit", subagent_type="self"):
        """
        Constructs a structured, high-clarity subagent dispatch prompt and metadata envelope.
        """
        context_section = ""
        if context_frames:
            context_section = "\n\n### Required Task Context:\n" + json.dumps(context_frames, indent=2)

        prompt = f"""You are the {role} subagent.
Objective: {task_description}{context_section}

Execution Directives:
1. Focus strictly on the objective defined above.
2. Store intermediate progress in SQLite or send event updates via wc-agent-channel.
3. Report back with a structured summary of deliverables once finished.
"""
        return {
            "TypeName": subagent_type,
            "Role": role,
            "Model": model,
            "Workspace": workspace,
            "Prompt": prompt.strip()
        }

    @staticmethod
    def aggregate_subagent_outcomes(outcomes):
        """
        Aggregates results from multiple subagents into a unified verification receipt.
        """
        total = len(outcomes)
        succeeded = sum(1 for o in outcomes if o.get("status") in ["SUCCESS", "DONE", "PASSED"])
        failed = total - succeeded

        return {
            "total_subagents": total,
            "succeeded": succeeded,
            "failed": failed,
            "consensus_passed": failed == 0,
            "outcomes": outcomes,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
