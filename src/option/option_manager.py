# Option Manager
from configuration.configuration import Configuration


class OptionManager:
    def __init__(self):
        self.options = {}

    def add_option(self, name, option):
        self.options[name] = option

    def display_options(self):
        print("Available Options:")
        for name, option in self.options.items():
            print(f"{name}: {option.description}")

    def execute_option(self, name):
        if name in self.options:
            self.options[name].execute()
        else:
            print("Invalid option")

    def update(self):
        # Update behavior based on new configurations
        configuration: Configuration = Configuration()
        print(f"Options updated based on new configurations: {configuration}")
