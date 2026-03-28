from command.command import Command
from arp_spoof.arp_spoof import ArpSpoof
import os
import time

class ToggleIpForwarding(Command):
    """
    Command to manually check and toggle the system's IP forwarding status (Linux).
    """
    def execute(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            status = ArpSpoof.get_ip_forwarding_status()
            
            print("--- IP Forwarding Management ---")
            print(f"Current Status: {status}")
            print("\nOptions: [1] Enable, [2] Disable, [q] Return")
            
            choice = input(">> ").lower()
            
            if choice == '1':
                success, msg = ArpSpoof.set_ip_forwarding_status(True)
                print(f"{'[+]' if success else '[-]'} {msg}")
                time.sleep(1.5)
                if success: break
            elif choice == '2':
                success, msg = ArpSpoof.set_ip_forwarding_status(False)
                print(f"{'[+]' if success else '[-]'} {msg}")
                time.sleep(1.5)
                if success: break
            elif choice == 'q':
                break
            else:
                print("[-] Invalid option.")
                time.sleep(1)
