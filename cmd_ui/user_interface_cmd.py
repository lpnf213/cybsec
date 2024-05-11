import os
class UserInterfaceCmd:

    @staticmethod
    def clear_screen():
        # Clear screen command for Windows
        if os.name == 'nt':
            _ = os.system('cls')
        # Clear screen command for Mac and Linux
        else:
            _ = os.system('clear')
    @staticmethod
    def select_option(**kwargs):
        print("Menu Options:")
        for key, value in kwargs.items():
            print(f"{key}: {value}")

        choice = input("Choose an option: ")

        if choice in kwargs:
            return kwargs[choice]

        print("Invalid option. Please choose from the list.")
        return None
