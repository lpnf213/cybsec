# Menu
from src.option.option import Option
from src.option.option_manager import OptionManager


class Menu:
    def __init__(self, option_manager: OptionManager):
        active_options: dict = option_manager.active_options
        self.sorted_options = sorted(active_options.values(), key=lambda option: option.priority)

    def display(self):
        print("Menu:")
        for idx, active_option in enumerate(self.sorted_options, start=1):
            print(f"{idx}. {active_option.name} - {active_option.description}")

    def get_choice(self):
        while True:
            choice = input("Enter your choice: ")
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(self.sorted_options):
                    selected_option: Option = self.sorted_options[index]
                    return selected_option.id
            print("Invalid choice. Please enter a valid number.")

    @staticmethod
    def build(option_manager: OptionManager):
        return Menu(option_manager = option_manager)
