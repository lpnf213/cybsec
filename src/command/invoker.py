"""
Invoker: This is responsible for invoking the commands. 
It holds a reference to the command and calls its execute() method.
"""
from src.command.command import Command


class Invoker:
    def __init__(self):
        self.command = None

    def add_command(self, command):
        self.command: Command = command

    def execute_command(self):
        self.command.execute()
        self.command.set_configuration()
