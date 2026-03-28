# Command Interface
from interface_mac_controller.interface_mac_controller import InterfaceMacController
from command.command import Command


class ReportInterface(Command):
    """
    Command that lists and reports available network interfaces to the user.
    """
    def execute(self):
        InterfaceMacController.generate_report()

    def set_configuration(self):
        pass
