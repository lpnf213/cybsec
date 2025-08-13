from arp_spoof.command_choose_router import ChooseRouter
from arp_spoof.command_mim import Mim
from interface_mac_controller.command_choose_interface import ChooseInterface
from interface_mac_controller.command_mac_changer import MacChanger
from interface_mac_controller.command_report_interface import ReportInterface
from network_scanner.command_network_long_scanner_scapy import NetworkLongScannerScapy
from network_scanner.command_network_short_scanner_scapy import NetworkShortScannerScapy
from option.option_manager import OptionManager
from command.exit_program import ExitProgram
from configuration.configuration import Configuration
from command.hello_world import HelloWorld
from option.option import Option

class OptionManagerBuilder:
    @staticmethod
    def build():
        configuration: Configuration = Configuration()
        option_manager: OptionManager = OptionManager()
        # exit
        exit_option: Option = Option.build(
            identifier='000',
            priority=999999,
            name='Exit command!',
            description='Exit Program!',
            status = 0,
            command=ExitProgram()
        )
        option_manager.add_option(exit_option)

        hello_world_option: Option = Option.build(
            identifier='001',
            priority=1,
            name='hello world command!',
            description='Print string hello world!',
            status = 0,
            command=HelloWorld()
        )
        option_manager.add_option(hello_world_option)
        report_interface_option: Option = Option.build(
            identifier='002',
            priority=2,
            name='report_interface_option',
            description='Show my interfaces!',
            status = 0,
            command=ReportInterface()
        )
        option_manager.add_option(report_interface_option)

        choose_interface_option: Option = Option.build(
            identifier='003',
            priority=3,
            name='choose_interface_option',
            description='Choose my interface!',
            status = 0,
            command=ChooseInterface()
        )
        option_manager.add_option(choose_interface_option)

        mac_changer_option: Option = Option.build(
            identifier='004',
            priority=4,
            name='mac_changer',
            description='Change Mac Address!',
            status = 0,
            command=MacChanger()
        )
        option_manager.add_option(mac_changer_option)

        network_long_scanner_scapy_option: Option = Option.build(
            identifier='005',
            priority=5,
            name='network_long_scanner_scapy',
            description='Network Long Scanner with Scapy!',
            status = 0,
            command=NetworkLongScannerScapy()
        )
        option_manager.add_option(network_long_scanner_scapy_option)

        network_short_scanner_scapy_option: Option = Option.build(
            identifier='006',
            priority=5,
            name='network_short_scanner_scapy',
            description='Network Short Scanner with Scapy!',
            status = 0,
            command=NetworkShortScannerScapy()
        )
        option_manager.add_option(network_short_scanner_scapy_option)

        choose_router_option: Option = Option.build(
            identifier='007',
            priority=6,
            name='choose_router_ip',
            description='Choose Router Ip',
            status = 0,
            command=ChooseRouter()
        )
        option_manager.add_option(choose_router_option)

        mim_option: Option = Option.build(
            identifier='008',
            priority=7,
            name='mim',
            description='Man in the Middle Attack',
            status = 0,
            command=Mim()
        )
        option_manager.add_option(mim_option)


        for option in option_manager.options.values():
            configuration.subscribe(option)
        configuration.notify_observers()
        option_manager.calculate_active_options()
        return option_manager
