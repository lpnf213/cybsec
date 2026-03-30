from command.command import Command
from iptables_manager.iptables_controller import IptablesController
from utils.utils import press_enter_and_clear_screen
import os
import time

class IptablesFlush(Command):
    """
    Command to completely reset all iptables rules to default states.
    Cleans filter, nat, and mangle tables.
    """
    def execute(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- [!] DANGER: Iptables Full Reset ---")
        print("This will delete ALL existing firewall and routing rules.")
        
        confirm = input("\nAre you SURE you want to reset everything? (type 'yes'): ").lower()
        
        if confirm == 'yes':
            success = IptablesController.flush_all()
            if success:
                print("\n[+] Success! Iptables is back to default state.")
            else:
                print("\n[-] Something went wrong during flush. Check sudo permissions.")
            
            press_enter_and_clear_screen()

    def set_configuration(self, value):
        pass
