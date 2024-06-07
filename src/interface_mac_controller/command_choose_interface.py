# Command Interface
from src.configuration.configuration import Configuration
from src.interface_mac_controller.interface_mac_controller import InterfaceMacController
from src.command.command import Command


class ChooseInterface(Command):
    def execute(self):
        interface = InterfaceMacController.choose_interface()
        self.set_configuration(interface)

    def set_configuration(self, interface):
        configuration = Configuration()
        configuration.set_configuration(key='my_interface', value=interface)
