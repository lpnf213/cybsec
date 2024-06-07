# Option Manager
from src.configuration.configuration import Configuration
from src.command.invoker import Invoker
from src.option.option import Option


class OptionManager:
    def __init__(self):
        self.options = {}
        self.active_options = {}

    def add_option(self, option: Option):
        self.options[option.id] = option

    def calculate_active_options(self):
        self.active_options = {}
        for option in self.options.values():
            if option.status == 1:
                self.active_options[option.id] = option

    def execute_option(self, identifier):
        if identifier in self.options and self.options[identifier].status==1:
            invoke_command: Invoker = Invoker()
            invoke_command.add_command(self.options[identifier].command)
            invoke_command.execute_command()
            configuration: Configuration = Configuration()
            configuration.notify_observers()
            self.calculate_active_options()
        else:
            print("Invalid option")
