# Builder Pattern
from command.command import Command


class Option:
    def __init__(self, identifier:str,
                 priority: int,
                 name:str,
                 description:str,
                 status: bool,
                 command: Command):
        self.id: str = identifier
        self.priority: int = priority
        self.name: str = name
        self.description: str = description
        self.status: bool = status
        self.command: Command = command

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_status(self, status):
        self.status = status

    def set_command(self, command: Command):
        self.command: Command = command

    def update_by_rules(self, configurations):
        if self.id in ['000','001','002','003', '013', '014', '015', '016']:
            self.set_status(1)

        if configurations.get_configuration(key="my_interface") and self.id in ['004',
                                                                                '005',
                                                                                '006',
                                                                                '007',
                                                                                '008']:
            self.set_status(1)

        if configurations.get_configuration(key="router_ip") and self.id in ['009','010']:
            self.set_status(1)

        mim_targets = configurations.get_configuration(key="mim_targets")
        if mim_targets and len(mim_targets) > 0 and self.id in ['011','012','017','018']:
            self.set_status(1)



    @staticmethod
    def build(identifier: str,
              priority: int,
              name: str,
              description: str,
              status: bool,
              command: Command):
        return Option(identifier,priority, name, description, status, command)
