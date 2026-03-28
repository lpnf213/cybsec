from command.command import Command
from configuration.configuration import Configuration
from sniff.sniff import Sniff

class SniffStart(Command):
    """
    Command to start the packet sniffer on a specific Man-In-The-Middle target.
    Extracts HTTP URLs and Credentials, saving them to a specific file.
    """
    def execute(self):
        configuration = Configuration()
        interface = configuration.get_configuration(key="my_interface_name")
        
        if not interface:
            print("Please select an interface first.")
            return
            
        mim_targets: set = configuration.get_configuration(key='mim_targets')
        
        if not mim_targets:
            print("No active MIM targets. Please start an ARP Spoofing attack first.")
            return
            
        print(f"Active MIM targets: {', '.join(mim_targets)}")
        target = input("Target IP to sniff: ")
        
        if target not in mim_targets:
            print("Warning: Target is not in the active MIM list. Sniffing may not capture relevant data.")
            
        Sniff.start_sniff(interface=interface, target_ip=target)
        print(f"Sniffer started! Logs will be saved to threads/{target}_sniff_log.txt")


class SniffStop(Command):
    """
    Command to stop the background packet sniffer for a specific target.
    """
    def execute(self):
        target = input("Target IP to stop sniffing: ")
        Sniff.stop_sniff(target_ip=target)
        print(f"Sniffer stopped for {target}.")
