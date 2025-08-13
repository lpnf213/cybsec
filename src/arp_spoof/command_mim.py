from arp_spoof.arp_spoof import ArpSpoof
from command.command import Command
from configuration.configuration import Configuration


class Mim(Command):
    def execute(self):
        configuration = Configuration()
        router: str = configuration.get_configuration(key='router_ip')
        target: str = input("Ip Target: ")
        ArpSpoof.main_mim(router_ip=router,target_ip=target)
        self.set_configuration(target)

    def set_configuration(self, target):
        configuration = Configuration()
        mim_targets: list = configuration.get_configuration(key='mim_targets')
        if not mim_targets:
             mim_targets = []
        mim_targets.append(target)
        configuration.set_configuration(key='mim_targets', value=mim_targets)
