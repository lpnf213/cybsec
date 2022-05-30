#!/usr/bin/env python
import scapy.all as scapy


def scan(ip):
    # ARP REQUEST -> who has net ip?
    arp_request = scapy.ARP(pdst=ip)
    print(arp_request.summary())
    arp_request.show()
    # internet object frame
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    print(broadcast.summary())
    broadcast.show()
    # ARP REQUEST + INTERNET FRAME
    arp_request_broadcast = broadcast/arp_request
    print(arp_request_broadcast.summary())
    arp_request_broadcast.show()


scan("192.168.1.1/24")
