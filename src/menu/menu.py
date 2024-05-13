# Menu
class Menu:
    def __init__(self):
        self.menu_items = []

    def add_item(self, item):
        self.menu_items.append(item)

    def display(self):
        print("Menu:")
        for idx, item in enumerate(self.menu_items, start=1):
            print(f"{idx}. {item.name} - {item.description}")

    def get_choice(self):
        while True:
            choice = input("Enter your choice: ")
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(self.menu_items):
                    return index
            print("Invalid choice. Please enter a valid number.")
