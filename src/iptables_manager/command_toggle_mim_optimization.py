from command.command import Command
from iptables_manager.iptables_controller import IptablesController
import os
import time

class ToggleMimOptimization(Command):
    """
    Command to manage TCP MSS Clamping for better MIM performance.
    Now leverages the centralized IptablesController.
    """
    def execute(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- MIM Performance Optimization (TCP MSS Clamping) ---")
        
        # Check current status through our controller
        is_active = IptablesController.is_mss_clamping_active()
        print(f"Current Status: {'[ENABLED]' if is_active else '[DISABLED]'}")
        
        print("\nThis optimization forces smaller TCP segments, preventing")
        print("connectivity issues on heavy sites (GitHub, Google, etc).")
        
        choice = input(f"\nDo you want to {'DISABLE' if is_active else 'ENABLE'} it? (y/n): ").lower()
        
        if choice == 'y':
            success = IptablesController.set_mss_clamping(not is_active)
            if success:
                print(f"[+] Optimization status updated.")
            else:
                print(f"[-] FAILED to update optimization. Checked permissions?")
            
            time.sleep(1.5)

    def set_configuration(self, value):
        pass
