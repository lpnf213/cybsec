from src.interface_mac_controller.command_choose_interface import ChooseInterface
from src.interface_mac_controller.command_report_interface import ReportInterface
from src.option.option_manager import OptionManager
from src.command.exit_program import ExitProgram
from src.configuration.configuration import Configuration
from src.command.hello_world import HelloWorld
from src.option.option import Option

class OptionManagerBuilder:
    @staticmethod
    def build():
        configuration: Configuration = Configuration()
        option_manager: OptionManager = OptionManager()
        # exit
        exit_option: Option = Option.build(
            identifier='000',
            priority=999999,
            name='Exit command!',
            description='Exit Program!',
            status = 0,
            command=ExitProgram()
        )
        option_manager.add_option(exit_option)
        #hello world option
        hello_world_option: Option = Option.build(
            identifier='001',
            priority=0,
            name='hello world command!',
            description='Print string hello world!',
            status = 0,
            command=HelloWorld()
        )
        option_manager.add_option(hello_world_option)
        #hello world option
        report_interface_option: Option = Option.build(
            identifier='002',
            priority=1,
            name='report_interface_option',
            description='Show my interfaces!',
            status = 0,
            command=ReportInterface()
        )
        option_manager.add_option(report_interface_option)

        #hello world option
        report_interface_option: Option = Option.build(
            identifier='003',
            priority=2,
            name='choose_interface_option',
            description='Choose my interface!',
            status = 0,
            command=ChooseInterface()
        )
        option_manager.add_option(report_interface_option)

        for option in option_manager.options.values():
            configuration.subscribe(option)
        configuration.notify_observers()
        option_manager.calculate_active_options()
        return option_manager
