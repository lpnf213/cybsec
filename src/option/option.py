# Option
class Option:
    def __init__(self, name, description, type, default):
        self.name = name
        self.description = description
        self.type = type
        self.default = default

    def execute(self):
        # Placeholder for option execution logic
        print(f"Executing option: {self.name}")
