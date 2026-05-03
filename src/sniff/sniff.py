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
        # 1. Save RAW packet to PCAP
        try:
            if pcap_writer:
                pcap_writer.write(packet)
                pcap_writer.flush()
        except Exception:
            pass

        # 2. Extract basic info
        timestamp = time.strftime('%H:%M:%S')
        is_http = packet.haslayer(http.HTTPRequest)
        
        # 3. Enhanced Detection: DNS, TLS/SNI, and generic TCP/UDP
        log_entry = ""
        
        if is_http:
            url_str = Sniff.get_url(packet)
            login_info = Sniff.get_login_info(packet)
            log_entry = f"[{timestamp}] HTTP Request >> {url_str}\n"
            if login_info:
                log_entry += f"    [**] Possible Credentials >> {login_info}\n"
        
        elif packet.haslayer(scapy.DNSQR):
            qname = packet[scapy.DNSQR].qname.decode('utf-8', errors='ignore')
            log_entry = f"[{timestamp}] DNS Query >> {qname}\n"
            
        elif packet.haslayer(scapy.TCP):
            dst_ip = packet[scapy.IP].dst
            dport = packet[scapy.TCP].dport
            
            # Simple TLS SNI extraction for HTTPS
            if dport == 443 and packet.haslayer(scapy.Raw):
                load = packet[scapy.Raw].load
                # Look for the SNI pattern in TLS Handshake (Client Hello)
                # This is a simplified check for common domain patterns
                if b"\x00\x00" in load:
                    try:
                        # Extract domain-like strings from raw payload (simple forensic heuristic)
                        import re
                        domains = re.findall(b"[a-z0-9.-]+\\.[a-z]{2,}", load.lower())
                        if domains:
                            domain = domains[0].decode('utf-8', errors='ignore')
                            log_entry = f"[{timestamp}] HTTPS Session (SNI) >> {domain}\n"
                    except: pass
            
            if not log_entry:
                # Generic TCP traffic alert for visual feedback
                log_entry = f"[{timestamp}] TCP Connection >> {dst_ip}:{dport}\n"

        elif packet.haslayer(scapy.UDP):
            dst_ip = packet[scapy.IP].dst
            dport = packet[scapy.UDP].dport
            log_entry = f"[{timestamp}] UDP Traffic >> {dst_ip}:{dport}\n"

        # 4. Write to log
        if log_entry:
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