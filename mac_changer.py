#!/usr/bin/env python

import subprocess
import optparse
import re
import time


def get_mac_lists():
    config_mac = subprocess.Popen('sudo ifconfig ', shell=True,
                                  stdout=subprocess.PIPE)
    config_mac = config_mac.communicate()[0]
    config_mac = str(config_mac).split('\\n')
    mac_lists = []
    for mac in config_mac:
        r = re.findall(r".*: ", str(mac))
        if len(r) > 0:
            r = r[0].replace(": ", "").replace("b'", "")
            mac_lists.append(r)

    return mac_lists


def get_arguments():
    mac_lists = []
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface",
                      help="Interface to change its MAC address, "
                      "if use '-i all', all mac addresses will change ")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        # code to handle error
        parser.error("Please specify an interface, use --help for more info")
    elif options.interface == 'all':
        return get_mac_lists()
    else:
        mac_lists.append(options.interface)
        return mac_lists


def change_mac(interface):
    subprocess.call('sudo ifconfig ' + str(interface) + ' down', shell=True)
    time.sleep(2)
    subprocess.call('sudo macchanger -r ' + str(interface), shell=True)
    time.sleep(2)
    subprocess.call('sudo ifconfig ' + str(interface) + ' up', shell=True)


options = get_arguments()

for interface in options:
    print(interface)
    change_mac(interface)


# python  mac_changer.py -i wlp3s0
