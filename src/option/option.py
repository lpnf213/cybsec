# Builder Pattern
from src.command.command import Command


class Option:
    def __init__(self, identifier:str,
                 priority: int,
                 name:str,
                 description:str,
                 status: bool,
                 command: Command):
        self.id: str = identifier
        self.priority: int = priority
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

    def update_by_rules(self, config_data):
        if self.id in ['000','001','002','003']:
            self.set_status(1)

    @staticmethod
    def build(identifier: str,
              priority: int,
              name: str,
              description: str,
              status: bool,
              command: Command):
        return Option(identifier,priority, name, description, status, command)
