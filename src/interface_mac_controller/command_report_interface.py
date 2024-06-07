# Command Interface
from src.interface_mac_controller.interface_mac_controller import InterfaceMacController
from src.command.command import Command


class ReportInterface(Command):
    def execute(self):
        InterfaceMacController.generate_report()

    def set_configuration(self):
        pass
