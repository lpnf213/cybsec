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
    print(arp_request)
    # internet object frame
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    print(broadcast)
    # ARP REQUEST + INTERNET FRAME
    arp_request_broadcast = broadcast/arp_request
    print(arp_request_broadcast)
    
    answered_list, unanswered = scapy.srp(arp_request_broadcast,
                              timeout=5, verbose=True)
    print(answered_list)
    print(unanswered)

    # list of dictionaries
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append([client_dict])
    print(clients_list)
    return clients_list


def print_results(results_list):
    print("IP\t\t\tMAC Address\n-----------------------------------")
    for client in results_list:
        print(client[0]['ip']+"\t\t"+client[0]['mac'])


def turn_off_on():
    True
    #print("Turning Wifi off...\n")
    #os.system("nmcli radio wifi off")
    #time.sleep(2)
    #os.system("nmcli radio wifi on")
    #print("Starting Wifi...\n")
    #time.sleep(10)


def all_network(ip):
    c = 0
    list_targets = []
    scan_ = scan(ip)
    subprocess.call('clear')
    if scan_ is not None:
        list_targets.append(scan_)
    #print(list_targets[0])
    print_results(list_targets[0])
    print("to see OS: 'nmap --osscan-guess {ip}'")
    return list_targets


ip = get_arguments()
# scan all network
scan_result = all_network(ip)
subprocess.call('clear')
print_results(scan_result[0])
print("to see OS: 'nmap --osscan-guess {ip}'")


# nmap --osscan-guess {ip}
