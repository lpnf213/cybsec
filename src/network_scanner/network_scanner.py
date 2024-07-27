from cmd.command_line import DirectCommandLine
import scapy.all as scapy
import socket
import nmap
import requests
from tabulate import tabulate
from colorama import init, Fore, Style
# TODO: Create a Scapy Layer
class NetworkScanner:

    @staticmethod
    def scan_with_scapy(ip, timeout):
        # ARP REQUEST -> who has net ip?
        arp_request = scapy.ARP(pdst=ip)
        print('arp_request: ' + str(arp_request))
        # internet object frame
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        print('broadcast: ' + str(broadcast))
        # ARP REQUEST + INTERNET FRAME
        arp_request_broadcast = broadcast/arp_request
        print('arp_request_broadcast: ' + str(arp_request_broadcast))

        answered_list, unanswered = scapy.srp(arp_request_broadcast,
                                timeout=5, verbose=True)
        print(answered_list)
        print(unanswered)

        # list of dictionaries
        clients_list = []
        for element in answered_list:
            ip_address = element[1].psrc
            mac_address = element[1].hwsrc
            hostname = NetworkScanner.get_hostname(ip_address)
            device_info = NetworkScanner.get_device_info(ip_address, timeout)
            manufacturer = NetworkScanner.get_mac_manufacturer(mac_address)
            vulnerabilities = NetworkScanner.scan_vulnerabilities(ip_address, timeout)

            client_dict = {
                "ip": ip_address,
                "mac": mac_address,
                "name": hostname,
                "info": device_info, 
                "manufacturer": manufacturer,
                "vulnerabilities": vulnerabilities
            }
            clients_list.append(client_dict)
        if clients_list is not None:
            init(autoreset=True)  # Initialize colorama
            NetworkScanner.print_results(clients_list)

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
