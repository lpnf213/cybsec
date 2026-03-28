from command.command import Command
from network_scanner.network_scanner import NetworkScanner

class NetworkScannerShowResults(Command):
    """
    Command that displays the results of the most recent network scan.
    """
    def execute(self):
        NetworkScanner.show_last_results()
