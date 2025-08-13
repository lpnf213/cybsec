from command.command import Command
from configuration.configuration import Configuration


class ChooseRouter(Command):
    def execute(self):
        router: str = input("Ip Router: ")
        self.set_configuration(router)

    def set_configuration(self, router):
        configuration = Configuration()
        configuration.set_configuration(key='router_ip', value=router)
