# Command Interface
from interface_mac_controller.interface_mac_controller import InterfaceMacController
from command.command import Command


class ReportInterface(Command):
    def execute(self):
        InterfaceMacController.generate_report()

    def set_configuration(self):
        pass
