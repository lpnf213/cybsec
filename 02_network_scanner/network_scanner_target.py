#!/usr/bin/env python
import scapy.all as scapy
import os
import time
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
                              timeout=5, verbose=False)[0]

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


ip = get_arguments()
scan_result = scan(ip)
print_results(scan_result)

print("Turning Wifi off...\n")
os.system("nmcli radio wifi off")
time.sleep(5)
os.system("nmcli radio wifi on")
print("Starting Wifi...\n")
