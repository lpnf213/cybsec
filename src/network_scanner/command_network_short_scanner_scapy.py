# Command Interface
from configuration.configuration import Configuration
from command.command import Command
from network_scanner.network_scanner import NetworkScanner


class NetworkShortScannerScapy(Command):
    """
    Command responsible for performing a short (quick) network scan using Scapy.
    """
    def execute(self):
        configuration = Configuration()
        NetworkScanner.scan_with_scapy(
            configuration.get_configuration(key='cidr_2'), timeout = 1)

    def set_configuration(self, interface):
        configuration = Configuration()
