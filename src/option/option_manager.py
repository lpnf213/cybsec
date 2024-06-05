# Option Manager


from src.configuration.configuration import Configuration
from src.command.hello_world import HelloWorld
from src.command.invoker import Invoker
from src.option.option import Option


class OptionManager:
    def __init__(self):
        self.options = {}
        self.active_options = {}

    def add_option(self, option: Option):
        self.options[option.name] = option

    def calculate_active_options(self):
        self.active_options = {}
        for option in self.options.values():
            if option.status == 1:
                self.active_options[option.name] = option

    def execute_option(self, name):
        if name in self.options and self.options[name].status==1:
            invoke_command: Invoker = Invoker()
            invoke_command.add_command(self.options[name])
            invoke_command.execute_command()
            configuration: Configuration = Configuration()
            configuration.notify_observers()
            self.calculate_active_options()
        else:
            print("Invalid option")

    @staticmethod
    def build():
        configuration: Configuration = Configuration()
        option_manager: OptionManager = OptionManager()
        #hello world option
        hello_world_option: Option = Option.build(
            name='hello world command!',
            description='Print string hello world!',
            status = 1,
            command=HelloWorld()
        )
        option_manager.add_option(hello_world_option)
        for option in option_manager.options.values():
            configuration.subscribe(option)
        option_manager.calculate_active_options()
        return option_manager
