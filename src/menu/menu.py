# Menu
from src.option.option_manager import OptionManager


class Menu:
    def __init__(self, option_manager: OptionManager):
        self.option_manager = option_manager

    def display(self):
        print("Menu:")
        active_options: dict = self.option_manager.active_options
        for idx, active_option in enumerate(active_options.values(), start=1):
            print(f"{idx}. {active_option.name} - {active_option.description}")

    def get_choice(self):
        while True:
            choice = input("Enter your choice: ")
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(self.option_manager.active_options):
                    print(self.option_manager.active_options[index].name)
                    return index
            print("Invalid choice. Please enter a valid number.")

    @staticmethod
    def build(option_manager: OptionManager):
        return Menu(option_manager = option_manager)
