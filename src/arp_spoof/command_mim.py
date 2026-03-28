from arp_spoof.arp_spoof import ArpSpoof
from command.command import Command
from configuration.configuration import Configuration
from tabulate import tabulate
import os
import time

class Mim(Command):
    """
    Command to initiate a Man-In-The-Middle (ARP Spoofing) attack on a target.
    Allows interactive selection from the last network scan results.
    """
    def execute(self):
        configuration = Configuration()
        router: str = configuration.get_configuration(key='router_ip')
        
        if not router:
            print("[-] Router IP not set. Please select a router first.")
            time.sleep(1)
            return

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            results_file = configuration.get_configuration("last_scan_results_file")
            results = []
            
            if results_file and os.path.exists(results_file):
                import json
                try:
                    with open(results_file, 'r') as f:
                        results = json.load(f)
                except Exception:
                    results = []
            
            print(f"--- ARP Spoofing --- Router: {router} ---")
            
            if not results:
                print("[!] No scan results found.")
                target = input("Enter Target IP manually (or 'q' to cancel): ")
                if target.lower() == 'q': break
                self._start_mim(router, target)
                break

            print("\nSelect Target for MIM Attack:")
            table_data = []
            headers = ["#", "IP", "MAC Address", "Device Name", "Manufacturer"]
            
            for idx, client in enumerate(results, 1):
                # Don't show the router in the target list if we can help it
                if client['ip'] == router: continue
                table_data.append([idx, client['ip'], client['mac'], client['name'], client['manufacturer']])
            
            print(tabulate(table_data, headers, tablefmt="fancy_grid"))
            print("\nOptions: [Number] to select, [m] to enter manually, [q] to cancel")
            
            choice = input(">> ").lower()
            
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(results):
                    target = results[idx]['ip']
                    self._start_mim(router, target)
                    break
                else:
                    print("[-] Invalid index.")
                    time.sleep(1)
            elif choice == 'm':
                target = input("Enter Target IP: ")
                self._start_mim(router, target)
                break
            elif choice == 'q':
                break
            else:
                print("[-] Invalid option.")
                time.sleep(1)

    def _start_mim(self, router, target):
        configuration = Configuration()
        interface = configuration.get_configuration(key="my_interface_name")
        print(f"[+] Starting MIM attack: {router} <-> {target} on {interface}")
        ArpSpoof.main_mim(router_ip=router, target_ip=target, interface=interface)
        self.set_configuration(target)
        time.sleep(1)

    def set_configuration(self, target):
        configuration = Configuration()
        mim_targets: set = configuration.get_configuration(key='mim_targets')
        if not mim_targets:
             mim_targets = set()
        mim_targets.add(target)
        configuration.set_configuration(key='mim_targets', value=mim_targets)
