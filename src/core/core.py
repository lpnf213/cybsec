from src.menu.menu import Menu
from src.configuration.configuration import Configuration
from src.option.option_manager import OptionManager


def main():
    option_manager: OptionManager = OptionManager.build()
    while 1==1:
        menu: Menu = Menu.build(option_manager)
        menu.display()
        menu.get_choice()
