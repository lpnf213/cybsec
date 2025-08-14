from arp_spoof.arp_spoof import ArpSpoof
from command.command import Command
from configuration.configuration import Configuration


class MimRemove(Command):
    def execute(self):
        target: str = input("Ip Target: ")
        ArpSpoof.stop_mim(target_ip=target)
        self.set_configuration(target)

    def set_configuration(self, target):
        configuration = Configuration()
        mim_targets: set = configuration.get_configuration(key='mim_targets')
        if not mim_targets:
             mim_targets = set()
        mim_targets.discard(target)
        configuration.set_configuration(key='mim_targets', value=mim_targets)
