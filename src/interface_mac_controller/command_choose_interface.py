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
        configuration.set_configuration(key='mac_address', value=interface[2])
        configuration.set_configuration(key='mac_address_changed', value="")
        cidr_list: list = InterfaceMacController.detect_cidr(ip_address=interface[1])
        configuration.set_configuration(key='cidr_1', value=cidr_list[0])
        configuration.set_configuration(key='cidr_2', value=cidr_list[1])
        configuration.set_configuration(key='cidr_3', value=cidr_list[2])
        configuration.set_configuration(key='cidr_4', value=cidr_list[3])
