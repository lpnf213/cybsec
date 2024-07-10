from configuration.configuration import Configuration
from option.option_manager_builder import OptionManagerBuilder
from menu.menu import Menu
from option.option_manager import OptionManager
import os

from utils.utils import press_enter_and_clear_screen


def main():
    option_manager: OptionManager = OptionManagerBuilder.build()
    press_enter_and_clear_screen()
    while True:
        configuration: Configuration = Configuration()
        configuration.show_configurations()
        menu: Menu = Menu.build(option_manager)
        menu.display()
        option_id:str = menu.get_choice()
        option_manager.execute_option(identifier=option_id)
        press_enter_and_clear_screen()

