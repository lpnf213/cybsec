# Command Interface
from configuration.configuration import Configuration
from interface_mac_controller.interface_mac_controller import InterfaceMacController
from command.command import Command


class MacChanger(Command):
    """
    Command that facilitates changing the MAC address of a selected network interface.
    """
    def execute(self):
        configuration = Configuration()
        interface: str = configuration.get_configuration(key="my_interface_name")
        InterfaceMacController.mac_changer_interface(interface=interface)
        self.set_configuration(interface)

    def set_configuration(self, interface):
        interface_data = InterfaceMacController.get_interface_resume(interface_input = interface)
        configuration = Configuration()
        configuration.set_configuration(key='mac_address_changed',
                                        value=interface_data[2])
