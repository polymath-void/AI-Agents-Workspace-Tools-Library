import sys
import traceback

class WIEOrchestrator:
    """
    Fault-tolerant agent event orchestrator with exception isolation.
    """
    def __init__(self):
        self.agents = {}

    def register_agent(self, name, agent_function):
        self.agents[name] = agent_function

    def unregister_agent(self, name):
        if name in self.agents:
            del self.agents[name]

    def dispatch(self, event_type, path):
        for name, agent in list(self.agents.items()):
            try:
                agent(event_type, path)
            except Exception as e:
                # Isolate agent errors so other agents and the observer loop continue running smoothly
                print(f"[Orchestrator Warning] Agent '{name}' failed on {event_type}: {e}", file=sys.stderr)

    def handle_event(self, event_type, path):
        self.dispatch(event_type, path)
