import scapy.all as scapy
from scapy.layers import http
from collections import Counter
import os
import time
import requests
import re

class PcapInvestigator:
    @staticmethod
    def analyze(pcap_path):
        if not os.path.exists(pcap_path):
            return f"Error: {pcap_path} not found."

        print(f"[*] Loading and analyzing {os.path.basename(pcap_path)}... (This may take a moment)")
        try:
            packets = scapy.rdpcap(pcap_path)
        except Exception as e:
            return f"Error reading PCAP: {e}"

        total_packets = len(packets)
        protocols = Counter()
        destinations = Counter()
        domains = set()
        user_agents = set()
        credentials = []
        
        # Keyword search for credentials
        cred_keywords = ["user", "pass", "login", "password", "username", "cookie", "token"]

        for pkt in packets:
            if pkt.haslayer(scapy.IP):
                dst = pkt[scapy.IP].dst
                destinations[dst] += 1
                
                # Protocol counting
                if pkt.haslayer(scapy.TCP): protocols["TCP"] += 1
                elif pkt.haslayer(scapy.UDP): protocols["UDP"] += 1
                elif pkt.haslayer(scapy.ICMP): protocols["ICMP"] += 1
                elif pkt.haslayer(scapy.ARP): protocols["ARP"] += 1

                # Domain Extraction (DNS)
                if pkt.haslayer(scapy.DNSQR):
                    qname = pkt[scapy.DNSQR].qname.decode('utf-8', errors='ignore')
                    domains.add(qname)

                # Domain Extraction (SNI) & User-Agent (HTTP)
                if pkt.haslayer(scapy.Raw):
                    load = pkt[scapy.Raw].load
                    load_str = load.decode('utf-8', errors='ignore')

                    # SNI Detection (Simple Regex for typical TLS ClientHello domains)
                    if b'\x16\x03' in load and b'\x01\x00' in load:
                        matches = re.findall(r'[a-z0-9.-]+\.[a-z]{2,}', load_str)
                        for m in matches:
                            if len(m) > 4 and '.' in m:
                                domains.add(m)

                    # User-Agent Detection
                    if "User-Agent:" in load_str:
                        ua = load_str.split("User-Agent:")[1].split("\r\n")[0].strip()
                        user_agents.add(ua)

                    # Credential Search
                    for kw in cred_keywords:
                        if kw in load_str.lower():
                            context = f"Port {pkt[scapy.TCP].dport if pkt.haslayer(scapy.TCP) else 'UDP'}"
                            credentials.append(f"[{context}] {load_str.strip()[:100]}...")
                            break

        # Geolocation for top destinations
        geo_info = {}
        print("[*] Performing Geolocation for top destinations...")
        top_ips = [ip for ip, count in destinations.most_common(5)]
        for ip in top_ips:
            if not ip.startswith(("192.168.", "10.", "172.", "127.", "224.")):
                try:
                    response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
                    if response.status_code == 200:
                        data = response.json()
                        geo_info[ip] = f"{data.get('city', 'Unknown')}, {data.get('country', 'Unknown')} ({data.get('isp', 'Unknown')})"
                except:
                    geo_info[ip] = "GeoIP Lookup Failed"

        # Generate Report Content
        report_lines = []
        report_lines.append("="*50)
        report_lines.append(f"    CYBSEC PCAP INVESTIGATION REPORT")
        report_lines.append(f"    File: {os.path.basename(pcap_path)}")
        report_lines.append(f"    Analyzed at: {time.ctime()}")
        report_lines.append("="*50 + "\n")

        report_lines.append(f"Total Packets: {total_packets}\n")

        report_lines.append("--- Protocol Statistics ---")
        for proto, count in protocols.items():
            report_lines.append(f"  {proto}: {count}")
        report_lines.append("")

        report_lines.append("--- Top Destinations & Geolocation ---")
        for ip, count in destinations.most_common(10):
            geo = geo_info.get(ip, "Local / Private Network")
            report_lines.append(f"  {ip:15} | {count:5} pkts | {geo}")
        report_lines.append("")

        report_lines.append("--- Detected Domains (DNS/SNI) ---")
        for d in sorted(list(domains)):
            report_lines.append(f"  - {d}")
        if not domains: report_lines.append("  None detected.")
        report_lines.append("")

        if user_agents:
            report_lines.append("--- Device Information (User-Agents) ---")
            for ua in user_agents:
                report_lines.append(f"  - {ua}")
            report_lines.append("")

        if credentials:
            report_lines.append("--- Potential Clear-Text Data/Credentials ---")
            for cred in credentials[:20]: # Show first 20
                report_lines.append(f"  {cred}")
            report_lines.append("")

        # Save to file
        report_path = pcap_path.replace(".pcap", "_report.txt")
        try:
            with open(report_path, "w", encoding='utf-8') as f:
                f.write("\n".join(report_lines))
        except Exception as e:
            return f"Error saving report: {e}"

        return "\n".join(report_lines[:20]) + f"\n\n[...] FULL REPORT SAVED TO: {report_path}"
