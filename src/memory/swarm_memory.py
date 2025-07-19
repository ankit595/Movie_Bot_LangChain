# src/memory/swarm_memory.py
class SwarmMemory:
    def __init__(self):
        self.entries = []  # List of (question, route, answer)

    def log_route(self, question, route):
        self.entries.append({"question": question, "route": route})

    def log_answer(self, question, answer):
        for entry in self.entries:
            if entry["question"] == question:
                entry["answer"] = answer
                break

    def get_history(self):
        return self.entries