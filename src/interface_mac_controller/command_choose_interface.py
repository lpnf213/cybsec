# Command Interface
from configuration.configuration import Configuration
from interface_mac_controller.interface_mac_controller import InterfaceMacController
from command.command import Command


class ChooseInterface(Command):
    def execute(self):
        interface: list = InterfaceMacController.choose_interface()
        self.set_configuration(interface)

    def set_configuration(self, interface):
        configuration = Configuration()
        configuration.set_configuration(key='my_interface_name', value=interface[0])
        configuration.set_configuration(key='my_interface', value=interface[1])
        InterfaceMacController.detect_cidr(ip_address=interface[1])
