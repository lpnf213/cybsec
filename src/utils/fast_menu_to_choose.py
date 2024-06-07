def display(options):
    print("Choose item:")
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option.items()[0]}")

def get_choice(options):
    while True:
        choice = input("Enter your choice: ")
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(options):
                selected_option = options[index]
                return selected_option.key()
        print("Invalid choice. Please enter a valid number.")
