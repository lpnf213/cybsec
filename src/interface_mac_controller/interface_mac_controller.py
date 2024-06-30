from cmd.command_line import DirectCommandLine
from regex_parser.regex_parser import RegexParser
import time
import ipaddress

from utils.utils import choose_options_in_dict

class InterfaceMacController:


    @staticmethod
    def detect_cidr(ip_address: str):
        # List of common subnet masks
        common_subnet_masks = ['255.255.255.0', '255.255.0.0', '255.0.0.0']

        for mask in common_subnet_masks:
            network = ipaddress.IPv4Network((ip_address, mask), strict=False)
            cidr_notation = str(network)
            print(f"CIDR notation for IP {ip_address} with subnet mask {mask} is {cidr_notation}")

    @staticmethod
    def choose_interface():
        all_items = InterfaceMacController.generate_report(show_report=False)
        return choose_options_in_dict(all_items)

    @staticmethod
    def generate_report(show_report: bool = True):
        interfaces_list, ip_list, mac_list = InterfaceMacController.get_interface_resume()
        # Header for the report
        header = "NAME\tIP\tMAC ADDRESS"
        if show_report:
            print(header)
            print("=" * len(header.expandtabs()))
        all_items: dict = {}
        # Iterate through each sublist and print the information
        for position, interface in enumerate(interfaces_list):
            items = [interface, ip_list[position], mac_list[position]]
            if show_report:
                print("\t".join(map(str, items)))
            all_items[interface] = items
        return all_items

    @staticmethod
    def get_interface_resume():
        result_ifconfig: bytes = DirectCommandLine.popen(sudo='sudo',
                                             ifconfig='ifconfig')

        result_ifconfig_rows: list = str(result_ifconfig).replace(
            "\\n\\n"," ").split(
                'collisions 0')[:-1]
        interfaces_list = []
        ip_list = []
        mac_list = []
        for interface in result_ifconfig_rows:
            interfaces_list.append(InterfaceMacController.get_interface(interface))
            ip_list.append(InterfaceMacController.get_ip(interface))
            mac_list.append(InterfaceMacController.get_mac(interface))

        return interfaces_list, ip_list, mac_list

    @staticmethod
    def get_interface(interface):
        interface: list = str(interface).split('\\n')

        mac_lists = []
        for elem in interface:
            mac_lists.append(RegexParser.findall(r".*: ", str(elem),
                                                replace_expression=[[": ", ""]]))
        for mac in mac_lists:
            if len(mac) > 0:
                return mac[0].replace("b'", "").replace(" ", "")
        return None

    @staticmethod
    def get_ip(interface):
        interface: list = str(interface).split('\\n')
        ip_lists = []
        for elem in interface:
            ip_lists.append(
                RegexParser.findall(r'inet\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
                                    str(elem)))
        for ip in ip_lists:
            if len(ip) > 0:
                return ip[0]
        return None

    @staticmethod
    def get_mac(interface):
        interface: list = str(interface).split('\\n')
        mac_lists = []
        for elem in interface:
            mac_lists.append(
                RegexParser.findall(r'ether\s+([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})',
                                    str(elem)))
        for mac in mac_lists:
            if len(mac) > 0:
                return mac[0]
        return None

    @staticmethod
    def mac_changer_interface(interface):
        DirectCommandLine.call(
            command_ifconfig_down = 'sudo ifconfig ' + str(interface) + ' down', shell=True)
        time.sleep(2)
        DirectCommandLine.call(
            command_ifconfig_macchanger = 'sudo macchanger -r ' + str(interface), shell=True)
        time.sleep(2)
        DirectCommandLine.call(
            command_ifconfig_up = 'sudo ifconfig ' + str(interface) + ' up', shell=True)

    @staticmethod
    def mac_changer_all_interfaces():
        interfaces_list = InterfaceMacController.get_interface_resume()[0]
        for interface in interfaces_list:
            InterfaceMacController.mac_changer_interface(interface)
