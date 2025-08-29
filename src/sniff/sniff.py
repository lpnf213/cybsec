import scapy.all as scapy

from scapy.packet import Raw

class Sniff():

    @staticmethod
    def sniff(interface):
        scapy.sniff(
            iface=interface,
            store=False,
            prn=Sniff.process_sniffed_packet)
    @staticmethod
    def process_sniffed_packet(packet):
        print(packet)
        print(packet.summary())


Sniff.sniff("wlan0")