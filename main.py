from interface_mac_controller.interface_mac_controller import InterfaceMacController
from cmd_ui.user_interface_cmd import UserInterfaceCmd

UserInterfaceCmd.clear_screen()
UserInterfaceCmd.select_option(show_interfaces=1, choose_interfaces=2)

# report interface
# change one macaddress
# change all macaddress
InterfaceMacController.generate_report()
#MacController.mac_changer_all_interfaces()
#MacController.generate_report()