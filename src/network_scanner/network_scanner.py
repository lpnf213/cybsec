from cmd.command_line import DirectCommandLine
import scapy.all as scapy
import socket
import nmap
import requests
from tabulate import tabulate
import threading
import json
import os
import time
from colorama import init, Fore, Style
# TODO: Create a Scapy Layer
class NetworkScanner:

    @staticmethod
    def scan_with_scapy(ip, timeout):
        from configuration.configuration import Configuration
        configuration = Configuration()
        interface = configuration.get_configuration(key="my_interface_name")
        
        # ARP REQUEST -> who has net ip?
        arp_request = scapy.ARP(pdst=ip)
        # internet object frame
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        # ARP REQUEST + INTERNET FRAME
        arp_request_broadcast = broadcast/arp_request

        print(f"[!] Sending ARP Broadcast to {ip} on {interface}...")
        answered_list, _ = scapy.srp(arp_request_broadcast,
                                timeout=2, iface=interface, verbose=False)

        # Initial list of found devices
        clients_list = []
        for element in answered_list:
            client_dict = {
                "ip": element[1].psrc,
                "mac": element[1].hwsrc,
                "name": "Scanning...",
                "info": {"os": "Scanning...", "os_gen": "Scanning...", "os_vendor": "Scanning...", "open_ports": []},
                "manufacturer": "Scanning...",
                "vulnerabilities": []
            }
            clients_list.append(client_dict)
        
        # Save results to file with timestamp
        os.makedirs('threads', exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        results_file = f"threads/scan_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(clients_list, f, indent=4)
            
        # Store file path in Configuration
        configuration.set_configuration("last_scan_results_file", results_file)
        
        # Lock for thread-safe file updates
        file_lock = threading.Lock()

        # Start enrichment in background threads
        def enrich_client(client_ip):
            # Slow lookups
            hostname = NetworkScanner.get_hostname(client_ip)
            
            # Find the client index to update MAC first for manufacturer
            with file_lock:
                try:
                    with open(results_file, 'r') as f:
                        current_results = json.load(f)
                except Exception: return
                
                target_client = next((c for c in current_results if c["ip"] == client_ip), None)
                if not target_client: return
                
                mac_address = target_client["mac"]
            
            manufacturer = NetworkScanner.get_mac_manufacturer(mac_address)
            device_info = NetworkScanner.get_device_info(client_ip, timeout)
            
            # Update file safely
            with file_lock:
                try:
                    with open(results_file, 'r') as f:
                        current_results = json.load(f)
                    
                    for c in current_results:
                        if c["ip"] == client_ip:
                            c["name"] = hostname
                            c["manufacturer"] = manufacturer
                            c["info"] = device_info
                            break
                    
                    with open(results_file, 'w') as f:
                        json.dump(current_results, f, indent=4)
                except Exception: pass
            
            configuration.notify_observers()

        print(f"[!] Found {len(clients_list)} devices. Enriching data in background...")
        for client in clients_list:
            t = threading.Thread(target=enrich_client, args=(client["ip"],), daemon=True)
            t.start()
        
        return results_file

    @staticmethod
    def show_last_results():
        from configuration.configuration import Configuration
        configuration = Configuration()
        results_file = configuration.get_configuration("last_scan_results_file")
        
        if not results_file or not os.path.exists(results_file):
            print("[-] No recent scan results found.")
            return

        try:
            with open(results_file, 'r') as f:
                results = json.load(f)
            NetworkScanner.print_results(results)
        except Exception as e:
            print(f"[-] Error reading results: {e}")

    @staticmethod
    def get_hostname(ip):
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            hostname = "Unknown"
        return hostname

    @staticmethod
    def get_device_info(ip, timeout):
        device_info = {}
        try:
            nm = nmap.PortScanner()
            nm.scan(ip, arguments='-O', timeout=timeout)  # OS detection

            if ip in nm.all_hosts():
                if 'osclass' in nm[ip]:
                    device_info['os'] = nm[ip]['osclass'][0]['osfamily']
                    device_info['os_gen'] = nm[ip]['osclass'][0].get('osgen', 'Unknown')
                    device_info['os_vendor'] = nm[ip]['osclass'][0].get('vendor', 'Unknown')
                else:
                    device_info['os'] = 'Unknown'
                    device_info['os_gen'] = 'Unknown'
                    device_info['os_vendor'] = 'Unknown'

                device_info['open_ports'] = [port for port in nm[ip]['tcp']]
            else:
                device_info['os'] = 'Unknown'
                device_info['os_gen'] = 'Unknown'
                device_info['os_vendor'] = 'Unknown'
                device_info['open_ports'] = []
        except Exception as e:
            print(e)
            device_info['os'] = 'Unknown'
            device_info['os_gen'] = 'Unknown'
            device_info['os_vendor'] = 'Unknown'
            device_info['open_ports'] = []

        return device_info
    @staticmethod
    def get_mac_manufacturer(mac):
        url = f"https://api.macvendors.com/{mac}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                return "Unknown"
        except requests.RequestException:
            return "Unknown"

    @staticmethod
    def scan_vulnerabilities(ip, timeout):
        vulnerabilities = []
        try:
            nm = nmap.PortScanner()
            nm.scan(ip, arguments='--script vuln', timeout=timeout)
            if ip in nm.all_hosts():
                for script in nm[ip].get('hostscript', []):
                    vulnerabilities.append(script['id'])
            return vulnerabilities
        except Exception as e:
            print(e)
            return []
        
    @staticmethod     
    def print_results(results_list):
        table_data = []
        headers = ["IP",
                   "MAC Address", 
                   "Device Name", 
                   "OS", 
                   "OS Gen", 
                   "OS Vendor", 
                   "Open Ports", 
                   "Manufacturer", 
                   "Vulnerabilities"]

        for client in results_list:
            vulnerabilities = ", ".join(client['vulnerabilities'])
            if vulnerabilities:
                vulnerabilities = Fore.RED + vulnerabilities + Style.RESET_ALL

            row = [
                client['ip'],
                client['mac'],
                client['name'],
                client['info']['os'],
                client['info']['os_gen'],
                client['info']['os_vendor'],
                ", ".join(map(str, client['info']['open_ports'])),
                client['manufacturer'],
                vulnerabilities
            ]
            table_data.append(row)

        print(tabulate(table_data, headers, tablefmt="fancy_grid"))

    @staticmethod
    def scan_with_nmap(ip):
        result_nmap: bytes = DirectCommandLine.popen(sudo='sudo',
                                        nmap='nmap',
                                        osscan_guess='--osscan-guess',
                                        ip=ip)
        print(result_nmap)
        print(str(result_nmap))

    @staticmethod
    def scan_with_netdiscover(ip):
        result_netdiscover: bytes = DirectCommandLine.popen(sudo='sudo',
                                        nmap='netdiscover',
                                        r='-r',
                                        ip=ip)
        print(result_netdiscover)
        print(str(result_netdiscover))
