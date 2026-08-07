import time
import json
from pathlib import Path

class AgentMesh:
    """
    Multi-Agent Swarm Coordinator: manages role handoffs, subagent consensus, and task routing.
    """
    DEFAULT_ROLES = {
        "Architect": "Designs component interfaces, schema models, and system boundaries.",
        "Implementer": "Writes code, modifies files, and scaffolds components.",
        "BuildDoctor": "Repairs build configurations, dependencies, and shebangs.",
        "Verifier": "Executes unit tests, benchmarks latency, and checks contracts.",
        "Auditor": "Audits security, complexity, token density, and workspace health."
    }

    def __init__(self):
        self.active_agents = {}
        self.handoff_log = []

    def register_subagent(self, agent_id, role, capabilities=None):
        self.active_agents[agent_id] = {
            "role": role,
            "role_description": self.DEFAULT_ROLES.get(role, "Custom agent role"),
            "capabilities": capabilities or [],
            "status": "IDLE",
            "registered_at": time.time()
        }

    def assign_task(self, agent_id, task_description):
        if agent_id not in self.active_agents:
            return {"error": f"Agent '{agent_id}' not found in mesh"}

        agent = self.active_agents[agent_id]
        agent["status"] = "BUSY"
        agent["current_task"] = task_description

        record = {
            "agent_id": agent_id,
            "role": agent["role"],
            "task": task_description,
            "assigned_at": time.time()
        }
        self.handoff_log.append(record)
        return record

    def complete_task(self, agent_id, outcome="SUCCESS", details=None):
        if agent_id in self.active_agents:
            agent = self.active_agents[agent_id]
            agent["status"] = "IDLE"
            agent["last_outcome"] = outcome
            agent["last_details"] = details
        return {"agent_id": agent_id, "outcome": outcome}

    def get_mesh_status(self):
        return {
            "total_agents": len(self.active_agents),
            "agents": self.active_agents,
            "recent_handoffs": self.handoff_log[-5:]
        }
