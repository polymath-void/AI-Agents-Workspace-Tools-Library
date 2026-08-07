class WIEOrchestrator:
    def __init__(self):
        self.agents = {}
        self.event_bus = []

    def register_agent(self, name, agent_function):
        self.agents[name] = agent_function

    def dispatch(self, event_type, path):
        print(f"Event: {event_type} on {path}")
        # Simple dispatch mechanism
        for name, agent in self.agents.items():
            agent(event_type, path)

    def handle_event(self, event_type, path):
        self.dispatch(event_type, path)
