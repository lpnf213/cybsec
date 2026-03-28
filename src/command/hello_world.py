# Command Interface
from configuration.configuration import Configuration
from command.command import Command


class HelloWorld(Command):
    """
    A simple command used for testing purposes that prints 'Hello World'.
    """
    def execute(self):
        print('Hello World!')

    def set_configuration(self):
        configuration: Configuration = Configuration()
        configuration.set_configuration(key='exit',
                                        value=1)
