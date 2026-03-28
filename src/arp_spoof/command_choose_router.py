from command.command import Command
from configuration.configuration import Configuration
from network_scanner.network_scanner import NetworkScanner
from utils.utils import press_enter_and_clear_screen
from tabulate import tabulate
import os
import time

class ChooseRouter(Command):
    """
    Command to select the router/gateway IP address for network attacks.
    Provides an interactive list from the last network scan.
    """
    def execute(self):
        configuration = Configuration()
        
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
            
            if not results:
                print("[!] No scan results found.")
                choice = input("Do you want to run a quick scan now? (y/n): ").lower()
                if choice == 'y':
                    cidr = configuration.get_configuration(key='cidr_2')
                    if not cidr:
                        cidr = input("Enter network CIDR (e.g. 192.168.1.0/24): ")
                        configuration.set_configuration('cidr_2', cidr)
                    NetworkScanner.scan_with_scapy(cidr, timeout=1)
                    input("Scan started. Press Enter to see results...")
                    continue
                else:
                    router = input("Enter Router IP manually: ")
                    self.set_configuration(router)
                    break

            print("\n--- Select Router from Discovered Devices ---")
            table_data = []
            headers = ["#", "IP", "MAC Address", "Device Name", "Manufacturer"]
            
            for idx, client in enumerate(results, 1):
                table_data.append([
                    idx,
                    client['ip'],
                    client['mac'],
                    client['name'],
                    client['manufacturer']
                ])
            
            print(tabulate(table_data, headers, tablefmt="fancy_grid"))
            print("\nOptions: [Number] to select, [Enter] to refresh data, [m] to enter manually, [q] to cancel")
            
            choice = input(">> ").lower()
            
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(results):
                    selected_ip = results[idx]['ip']
                    self.set_configuration(selected_ip)
                    print(f"[+] Router IP set to: {selected_ip}")
                    time.sleep(1)
                    break
                else:
                    print("[-] Invalid index.")
                    time.sleep(1)
            elif choice == 'm':
                router = input("Enter Router IP: ")
                self.set_configuration(router)
                break
            elif choice == 'q':
                break
            elif choice == '':
                continue # Refresh
            else:
                print("[-] Invalid option.")
                time.sleep(1)

    def set_configuration(self, router):
        configuration = Configuration()
        configuration.set_configuration(key='router_ip', value=router)
