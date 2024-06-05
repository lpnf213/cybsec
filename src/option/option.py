# Builder Pattern
from src.command.command import Command


class Option:
    def __init__(self, name, description, status: bool, command: Command):
        self.name: str = name
        self.description: str = description
        self.status: bool = status
        self.command: Command = command

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_status(self, status):
        self.status = status

    def set_command(self, command: Command):
        self.command: Command = command

    def update_by_rules(self, config_data: dict):
        # Update behavior based on new configurations
        print("Options updated based on new configurations")

    @staticmethod
    def build(name: str, description: str, status: bool, command: Command):
        return Option(name, description, status, command)
