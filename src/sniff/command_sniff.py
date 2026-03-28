from command.command import Command
from configuration.configuration import Configuration
from sniff.sniff import Sniff
import os
import time

class SniffStart(Command):
    """
    Command to start the packet sniffer on a specific Man-In-The-Middle target.
    Allows interactive selection from active MIM targets.
    """
    def execute(self):
        configuration = Configuration()
        interface = configuration.get_configuration(key="my_interface_name")
        
        if not interface:
            print("[-] Please select an interface first.")
            time.sleep(1)
            return
            
        mim_targets: set = configuration.get_configuration(key='mim_targets')
        
        if not mim_targets or len(mim_targets) == 0:
            print("[-] No active MIM targets. Please start an ARP Spoofing attack first.")
            time.sleep(1.5)
            return

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            sorted_targets = sorted(list(mim_targets))
            
            print(f"--- Start Sniffing --- Interface: {interface} ---")
            print("\nSelect Target to Sniff:")
            for idx, target in enumerate(sorted_targets, 1):
                # Check if already sniffing
                control_file = f"threads/{target}_sniff_control"
                status = "(Sniffing...)" if os.path.exists(control_file) else ""
                print(f"{idx}. {target} {status}")
            
            print("\nOptions: [Number] to start, [q] to cancel, [m] for manual IP")
            choice = input(">> ").lower()
            
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(sorted_targets):
                    self._start_sniff(interface, sorted_targets[idx])
                    break
                else:
                    print("[-] Invalid index.")
                    time.sleep(1)
            elif choice == 'm':
                target = input("Enter Target IP: ")
                self._start_sniff(interface, target)
                break
            elif choice == 'q':
                break
            else:
                print("[-] Invalid option.")
                time.sleep(1)

    def _start_sniff(self, interface, target):
        print(f"[+] Starting sniffer for {target} on {interface}...")
        Sniff.start_sniff(interface=interface, target_ip=target)
        print(f"[!] Log: threads/{target}_sniff_log.txt")
        print(f"[!] Raw Capture (PCAP): threads/{target}_capture.pcap")
        time.sleep(1.5)


class SniffStop(Command):
    """
    Command to stop the background packet sniffer for a specific target.
    Lists only targets currently being sniffed.
    """
    def execute(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Find all active sniffers by looking for control files
            sniffing_targets = []
            if os.path.exists('threads'):
                for f in os.listdir('threads'):
                    if f.endswith('_sniff_control'):
                        target = f.replace('_sniff_control', '')
                        sniffing_targets.append(target)
            
            if not sniffing_targets:
                print("[-] No active sniffing sessions found.")
                time.sleep(1.5)
                break
            
            sniffing_targets.sort()
            
            print("--- Active Sniffing Sessions ---")
            for idx, target in enumerate(sniffing_targets, 1):
                print(f"{idx}. {target}")
            
            print("\nOptions: [Number] to stop, [q] to cancel, [m] for manual IP")
            choice = input(">> ").lower()
            
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(sniffing_targets):
                    self._stop_sniff(sniffing_targets[idx])
                    break
                else:
                    print("[-] Invalid index.")
                    time.sleep(1)
            elif choice == 'm':
                target = input("Enter IP to stop: ")
                self._stop_sniff(target)
                break
            elif choice == 'q':
                break
            else:
                print("[-] Invalid option.")
                time.sleep(1)

    def _stop_sniff(self, target):
        print(f"[*] Stopping sniffer for {target}...")
        Sniff.stop_sniff(target_ip=target)
        time.sleep(1)
