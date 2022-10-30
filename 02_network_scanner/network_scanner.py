#!/usr/bin/env python
import scapy.all as scapy
import os
import time
import subprocess
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target",
                      help="Target Ip")
    (options, arguments) = parser.parse_args()
    return options.target


def scan(ip):
    # ARP REQUEST -> who has net ip?
    arp_request = scapy.ARP(pdst=ip)
    # internet object frame
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # ARP REQUEST + INTERNET FRAME
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast,
                              timeout=2, verbose=True)[0]

    # list of dictionaries
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
        return clients_list


def print_results(results_list):
    print("IP\t\t\tMAC Address\n-----------------------------------")
    for client in results_list:
        print(client['ip']+"\t\t"+client['mac'])


def turn_off_on():
    print("Turning Wifi off...\n")
    os.system("nmcli radio wifi off")
    time.sleep(2)
    os.system("nmcli radio wifi on")
    print("Starting Wifi...\n")
    time.sleep(10)


def all_network(ip):
    c = 0
    list_targets = []
    ip_router = ip.split('.')
    for i in range(255):
        c += 1
        if c == 50:
            # turn off on
            turn_off_on()
            c = 0
        ip_router[-1] = str(255-i)
        target_ip = ''
        for part_ip in ip_router:
            target_ip += '.' + str(part_ip)
        scan_ = scan(target_ip[1:])
        subprocess.call('clear')
        print(target_ip[1:])
        if scan_ is not None:
            list_targets.append(scan_[0])
        print_results(list_targets)
        print("to see OS: 'nmap --osscan-guess {ip}'")
    return list_targets


ip = get_arguments()
# scan all network
scan_result = all_network(ip)
subprocess.call('clear')
print_results(scan_result)
print("to see OS: 'nmap --osscan-guess {ip}'")


# nmap --osscan-guess {ip}
