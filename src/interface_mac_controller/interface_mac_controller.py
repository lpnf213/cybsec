from src.cmd.command_line import DirectCommandLine
from src.regex_parser.regex_parser import RegexParser
import time

from src.utils.fast_menu_to_choose import display, get_choice

class InterfaceMacController:

    @staticmethod
    def generate_report():
        interfaces_list, ip_list, mac_list = InterfaceMacController.get_interface_resume()
        # Header for the report
        header = "NAME\tIP\tMAC ADDRESS"
        print(header)
        print("=" * len(header.expandtabs()))

        # Iterate through each sublist and print the information
        for position, interface in enumerate(interfaces_list):
            items = [interface, ip_list[position], mac_list[position]]
            print("\t".join(map(str, items)))

    @staticmethod
    def choose_interface():
        interfaces_list, ip_list, mac_list = InterfaceMacController.get_interface_resume()
        options: list = []
        for position, interface in enumerate(interfaces_list):
            option = {interface: f'{interface} - {ip_list[position]} - {mac_list[position]}'}
            options.append(option)
        display(options)
        return get_choice(options)

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
