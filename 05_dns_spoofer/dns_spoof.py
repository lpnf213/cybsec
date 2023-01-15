import netfilterqueue
import scapy.all as scapy
import subprocess
import optparse



def process_packet(packet):
    
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        print(scapy_packet.show())
            
    packet.accept()
    


# use function NetFilterQueue to execute a function in information recive
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
