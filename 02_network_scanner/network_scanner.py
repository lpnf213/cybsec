#!/usr/bin/env python
import scapy.all as scapy


def scan(ip):
    # ARP REQUEST -> who has net ip?
    arp_request = scapy.ARP(pdst=ip)
    # internet object frame
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # ARP REQUEST + INTERNET FRAME
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast,
                              timeout=1, verbose=False)[0]
    print("IP\t\t\tMAC Address\n---------------------------------")
    for element in answered_list:
        print(element[1].psrc + "\t\t" + element[1].hwsrc)


scan("10.0.2.1/24")
