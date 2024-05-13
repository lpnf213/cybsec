# Invoker
from command.command import Command


class Invoker:
    def __init__(self):
        self.command = None

    def add_command(self, command):
        self.command: Command = command

    def execute_commands(self):
        self.command.execute()
