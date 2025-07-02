class MCPAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.history = []

    def think(self, prompt, model_fn):
        self.history.append(("user", prompt))
        full_prompt = f"{self.role}\n\n{prompt}"
        response = model_fn(full_prompt)
        self.history.append(("agent", response))
        return response
