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
Broadcast MaxAddress 
Who are mac Address x
## ARP RECEIVE
My Mac Address is x
## see MY ARP TABLE
arp -a 
## ARP RESPONSE

## Class Diagram

```mermaid
classDiagram
    class Core {
        <<EntryPoint>>
        +main()
    }

    class Command {
        <<interface>>
        +execute()
        +set_configuration()
    }
    
    class Invoker {
        -commands: dict
        +register(command_name, command)
        +execute(command_name)
    }
    
    class Configuration {
        <<Subject>>
        +get_configuration(key)
        +subscribe(observer)
        +notify_observers()
    }

    class Option {
        <<Observer>>
        +id: str
        +status: bool
        -command: Command
        +update_by_rules(configurations)
    }
    
    class OptionManager {
        -options: dict
        -active_options: dict
        +add_option(option)
        +execute_option(identifier)
    }
    
    class OptionManagerBuilder {
        <<Builder>>
        +build() OptionManager
    }

    class Menu {
        -sorted_options: list
        +build(option_manager)
        +display()
        +get_choice()
    }

    %% Core Entry Point Logic
    Core --> OptionManagerBuilder : initiates
    Core --> OptionManager : uses
    Core --> Configuration : initializes
    Core --> Menu : creates
    
    %% Menu Logic
    Menu --> OptionManager : reads active_options
    Menu --> Option : interacts with

    %% Option and Patterns
    OptionManagerBuilder --> OptionManager : builds
    OptionManager "1" o-- "many" Option : contains
    Option o-- Command : wraps
    Configuration <-- Option : observes (updates status based on configs)
    
    %% Commands and Dependencies
    Command <|-- NetworkShortScannerScapy
    Command <|-- NetworkLongScannerScapy
    Command <|-- ReportInterface
    Command <|-- ChooseInterface
    Command <|-- MacChanger
    Command <|-- ExitProgram
    Command <|-- HelloWorld
    Command <|-- MimRemove
    Command <|-- Mim
    Command <|-- ChooseRouter
    Command <|-- SniffStart
    Command <|-- SniffStop
    Command <|-- NetworkScannerShowResults

    %% State dependencies (represented as dashed arrows)
    NetworkShortScannerScapy ..> NetworkScannerShowResults : provides scan_results
    NetworkLongScannerScapy ..> NetworkScannerShowResults : provides scan_results
    NetworkShortScannerScapy ..> ChooseRouter : provides IPs
    NetworkLongScannerScapy ..> ChooseRouter : provides IPs
    ChooseRouter ..> Mim : provides router_ip
    Mim ..> SniffStart : provides mim_targets

    Invoker o-- Command : executes
    
    %% Core Modules Dependencies
    class NetworkScanner
    class InterfaceMacController
    class ArpSpoof
    class Sniff
    class RegexParser

    NetworkShortScannerScapy --> NetworkScanner : uses
    NetworkLongScannerScapy --> NetworkScanner : uses
    NetworkScannerShowResults --> NetworkScanner : uses
    
    ReportInterface --> InterfaceMacController : uses
    ChooseInterface --> InterfaceMacController : uses
    MacChanger --> InterfaceMacController : uses

    Mim --> ArpSpoof : uses
    MimRemove --> ArpSpoof : uses

    SniffStart --> Sniff : uses
    SniffStop --> Sniff : uses

    InterfaceMacController --> RegexParser : uses
```

## Available Commands (Command Pattern)

The following classes inherit from the base `Command` interface to provide specific functionalities:

- **NetworkShortScannerScapy**: Performs a short (quick) network scan using Scapy.
- **NetworkLongScannerScapy**: Performs a comprehensive (long) network scan using Scapy.
- **NetworkScannerShowResults**: Displays the results of the most recent network scan from its JSON file.
- **ReportInterface**: Lists and reports available network interfaces to the user.
- **ChooseInterface**: Allows the user to select an active network interface for operations.
- **MacChanger**: Facilitates changing the MAC address of a selected network interface.
- **ExitProgram**: Cleanly terminates and exits the application.
- **HelloWorld**: A simple command used for testing purposes that prints 'Hello World'.
- **MimRemove**: Stops and removes an active Man-In-The-Middle (ARP Spoofing) attack.
- **Mim**: Initiates a Man-In-The-Middle (ARP Spoofing) attack on a target.
- **ChooseRouter**: Selects the router/gateway IP address for network attacks.
- **SniffStart**: Starts the packet sniffer on a target (requires active MIM).
- **SniffStop**: Stops a background packet sniffer session.
