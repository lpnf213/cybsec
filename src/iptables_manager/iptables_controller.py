import os
import subprocess

class IptablesController:
    """
    Centralized controller to manage Linux kernel networking and iptables rules.
    This class abstracts the complexity of system calls into high-level methods.
    """

    # --- IP FORWARDING (Kernel Level) ---

    @staticmethod
    def is_forwarding_enabled():
        """
        Checks if the IPv4 forwarding is enabled in the Linux kernel.
        Reading from /proc/sys/net/ipv4/ip_forward.
        """
        try:
            with open("/proc/sys/net/ipv4/ip_forward", "r") as f:
                return f.read().strip() == "1"
        except Exception:
            return False

    @staticmethod
    def set_forwarding(enable=True):
        """
        Enables or disables IP forwarding using sysctl.
        """
        value = "1" if enable else "0"
        print(f"[*] {'Enabling' if enable else 'Disabling'} IP Forwarding...")
        return os.system(f"sudo sysctl -w net.ipv4.ip_forward={value} > /dev/null") == 0

    # --- TCP MSS CLAMPING (Mangle Table) ---

    @staticmethod
    def is_mss_clamping_active():
        """
        Checks if the MSS Clamping rule exists in the mangle table.
        Uses the -C (Check) flag of iptables.
        """
        cmd = "sudo iptables -t mangle -C POSTROUTING -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu"
        # 2>/dev/null hides the error message if the rule doesn't exist
        return os.system(cmd + " 2>/dev/null") == 0

    @staticmethod
    def set_mss_clamping(enable=True):
        """
        Adds or removes the MSS Clamping rule to optimize MIM performance.
        """
        is_active = IptablesController.is_mss_clamping_active()
        
        if enable:
            if is_active:
                return True # Already enabled
            print("[*] Enabling TCP MSS Clamping (Optimization)...")
            cmd = "sudo iptables -t mangle -A POSTROUTING -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu"
            return os.system(cmd) == 0
        else:
            # We use a loop to ensure ALL duplicate rules are removed
            removed = 0
            while IptablesController.is_mss_clamping_active():
                cmd = "sudo iptables -t mangle -D POSTROUTING -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu"
                os.system(cmd)
                removed += 1
            if removed > 0:
                print(f"[-] Disabled TCP MSS Clamping ({removed} rules removed).")
            return True

    # --- DNS SPOOFING (NFQUEUE) ---

    @staticmethod
    def is_dns_spoof_active():
        """
        Checks if the NFQUEUE rule for DNS spoofing is active in the FORWARD chain.
        """
        cmd = "sudo iptables -C FORWARD -j NFQUEUE --queue-num 0"
        return os.system(cmd + " 2>/dev/null") == 0

    @staticmethod
    def set_dns_spoof_rules(enable=True):
        """
        Enables or disables the NFQUEUE rule to intercept forwarded traffic.
        Essential for DNS Spoofing, SSL Stripping, etc.
        """
        is_active = IptablesController.is_dns_spoof_active()

        if enable:
            if is_active:
                return True
            print("[*] Enabling NFQUEUE (Queue 0) for packet redirection...")
            cmd = "sudo iptables -I FORWARD -j NFQUEUE --queue-num 0"
            return os.system(cmd) == 0
        else:
            removed = 0
            while IptablesController.is_dns_spoof_active():
                cmd = "sudo iptables -D FORWARD -j NFQUEUE --queue-num 0"
                os.system(cmd)
                removed += 1
            if removed > 0:
                print(f"[-] Disabled NFQUEUE ({removed} rules removed).")
            return True

    # --- GENERAL MAINTENANCE ---

    @staticmethod
    def flush_all():
        """
        Performs a full reset of all iptables tables (filter, nat, mangle).
        Sets default policies to ACCEPT.
        """
        print("[!] Performing FULL iptables reset to defaults...")
        commands = [
            "sudo iptables -P INPUT ACCEPT",
            "sudo iptables -P FORWARD ACCEPT",
            "sudo iptables -P OUTPUT ACCEPT",
            "sudo iptables -t filter -F",
            "sudo iptables -t nat -F",
            "sudo iptables -t mangle -F",
            "sudo iptables -t filter -X",
            "sudo iptables -t nat -X",
            "sudo iptables -t mangle -X"
        ]
        
        success = True
        for cmd in commands:
            if os.system(cmd + " 2>/dev/null") != 0:
                success = False
        
        return success
