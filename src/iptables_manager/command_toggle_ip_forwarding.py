from command.command import Command
from iptables_manager.iptables_controller import IptablesController
from utils.utils import press_enter_and_clear_screen
import os
import time

class ToggleIpForwarding(Command):
    """
    Command to manage the Linux kernel IP Forwarding status.
    Now leverages the centralized IptablesController.
    """
    def execute(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- IP Forwarding Management ---")
        
        # Check current status through our controller
        is_enabled = IptablesController.is_forwarding_enabled()
        print(f"Current Status: {'[ENABLED]' if is_enabled else '[DISABLED]'}")
        
        print("\nNote: IP Forwarding must be ENABLED for MIM attacks to work")
        print("so that the victim doesn't lose internet connectivity.")
        
        choice = input(f"\nDo you want to {'DISABLE' if is_enabled else 'ENABLE'} it? (y/n): ").lower()
        
        if choice == 'y':
            success = IptablesController.set_forwarding(not is_enabled)
            if success:
                print(f"[+] Status successfully changed.")
            else:
                print(f"[-] FAILED to change status. Checked permissions?")
            
            time.sleep(1.5)

    def set_configuration(self, value):
        pass
