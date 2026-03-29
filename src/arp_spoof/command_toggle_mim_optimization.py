from command.command import Command
from cmd.command_line import DirectCommandLine
import os
import time

class ToggleMimOptimization(Command):
    """
    Command to toggle TCP MSS clamping to optimize MIM performance.
    Helps victim connectivity for heavy sites (GitHub, Google, etc).
    """
    def execute(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- MIM Performance Optimization (TCP MSS Clamping) ---")
        
        current_status = self._is_optimization_active()
        print(f"Current Status: {'[ENABLED]' if current_status else '[DISABLED]'}")
        
        print("\nThis optimization helps victims maintain connectivity to heavy sites")
        print("by forcing smaller TCP segments during the MIM attack.")
        
        choice = input(f"\nDo you want to {'DISABLE' if current_status else 'ENABLE'} it? (y/n): ").lower()
        
        if choice == 'y':
            if current_status:
                self._disable_optimization()
            else:
                self._enable_optimization()
            
            time.sleep(1.5)

    def _is_optimization_active(self):
        # Check if the rule exists in iptables
        try:
            # We use popen to check stdout
            result = os.popen("sudo iptables -t mangle -L POSTROUTING -v -n").read()
            return "TCPMSS clamp-mss-to-pmtu" in result
        except:
            return False

    def _enable_optimization(self):
        print("[*] Enabling TCP MSS Clamping...")
        cmd = "sudo iptables -t mangle -A POSTROUTING -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu"
        os.system(cmd)
        print("[+] Optimization ENABLED.")

    def _disable_optimization(self):
        print("[*] Disabling TCP MSS Clamping...")
        cmd = "sudo iptables -t mangle -D POSTROUTING -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu"
        os.system(cmd)
        print("[-] Optimization DISABLED.")

    def set_configuration(self, value):
        pass
