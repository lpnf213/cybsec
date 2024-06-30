from option.option_manager_builder import OptionManagerBuilder
from menu.menu import Menu
from option.option_manager import OptionManager


def main():
    option_manager: OptionManager = OptionManagerBuilder.build()
    while True:
        menu: Menu = Menu.build(option_manager)
        menu.display()
        option_id:str = menu.get_choice()
        option_manager.execute_option(identifier=option_id)
