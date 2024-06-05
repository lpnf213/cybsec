# Command Interface
from src.command.command import Command


class HelloWorld(Command):
    def execute(self):
        print('Hello World!')

    def set_configuration(self):
        pass