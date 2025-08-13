# TODO: Format Readme
# WINDOWS
wifi passwords saved 
netsh wlan show profile
netsh wlan show profile Nome_da_rede key=clear

# KALI LINUX DEBIAN VM
## shared folder with Main Machine
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

# network discover
## netdiscover
sudo netdiscover -r 192.168.1.1/24
## nmap
sudo nmap --osscan-guess "192.168.1.1/24" 

# ARP SPOOF
## arpsoof
arpspoof -i wlan0 -t 192.168.1.226 192.168.1.1
arpspoof -i wlan0 -t 192.168.1.1 192.168.1.226

# IP Forwarding

The command `echo 1 > /proc/sys/net/ipv4/ip_forward` is used in Linux to enable IP forwarding. Here's a breakdown of what each part of the command does:

- `echo 1`: This outputs the number `1`.
- `>`: This is a redirection operator that takes the output from the command on its left and writes it to the file on its right.
- `/proc/sys/net/ipv4/ip_forward`: This is a special file in the Linux filesystem that controls the IP forwarding feature.

When you write `1` to this file, you enable IP forwarding, which allows the system to forward packets from one network interface to another. This is essential for setting up a Linux machine as a router or gateway.

Here's a more detailed explanation of each component:

- `echo`: A command that prints its arguments to the standard output.
- `1`: The value to be written, where `1` enables IP forwarding.
- `>`: Redirection operator to direct the output to a file.
- `/proc/sys/net/ipv4/ip_forward`: A pseudo-file that controls IP forwarding settings. Writing `1` to this file turns on IP forwarding, while writing `0` turns it off.

By enabling IP forwarding, your Linux system can route traffic between different network interfaces, which is a key feature for network gateways, routers, or when setting up network address translation (NAT).


# ARP
## ARP REQUEST
Broadcast MacAddress 
Who are mac Address x
## ARP RECEIVE
My Mac Address is x
## see MY ARP TABLE
arp -a 
## ARP RESPONSE

