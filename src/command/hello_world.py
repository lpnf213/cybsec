# Command Interface
from src.configuration.configuration import Configuration
from src.command.command import Command


class HelloWorld(Command):
    def execute(self):
        print('Hello World!')

    def set_configuration(self):
        configuration: Configuration = Configuration()
        configuration.set_configuration(key='exit',
                                        value=1)
