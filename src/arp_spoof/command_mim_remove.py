from arp_spoof.arp_spoof import ArpSpoof
from command.command import Command
from configuration.configuration import Configuration
import os
import time

class MimRemove(Command):
    """
    Command to stop and remove an active Man-In-The-Middle (ARP Spoofing) attack.
    Allows selecting from currently active targets.
    """
    def execute(self):
        configuration = Configuration()
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            mim_targets: set = configuration.get_configuration(key='mim_targets')
            
            if not mim_targets or len(mim_targets) == 0:
                print("[-] No active MIM attacks to remove.")
                time.sleep(1.5)
                break
                
            sorted_targets = sorted(list(mim_targets))
            
            print("--- Active MIM Attacks ---")
            for idx, target in enumerate(sorted_targets, 1):
                print(f"{idx}. {target}")
            
            print("\nOptions: [Number] to stop attack, [q] to cancel, [m] for manual IP")
            choice = input(">> ").lower()
            
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(sorted_targets):
                    target = sorted_targets[idx]
                    self._stop_mim(target)
                    break
                else:
                    print("[-] Invalid index.")
                    time.sleep(1)
            elif choice == 'm':
                target = input("Enter IP to stop: ")
                self._stop_mim(target)
                break
            elif choice == 'q':
                break
            else:
                print("[-] Invalid option.")
                time.sleep(1)

    def _stop_mim(self, target):
        print(f"[*] Stopping MIM attack on {target}...")
        ArpSpoof.stop_mim(target_ip=target)
        self.set_configuration(target)
        time.sleep(1)

    def set_configuration(self, target):
        configuration = Configuration()
        mim_targets: set = configuration.get_configuration(key='mim_targets')
        if not mim_targets:
             mim_targets = set()
        mim_targets.discard(target)
        configuration.set_configuration(key='mim_targets', value=mim_targets)
