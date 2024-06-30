def get_choice_info(choice, options_dict):
    # Get the list of keys from the dictionary
    keys = list(options_dict.keys())

    # Check if the choice is a valid index
    if 1 <= choice <= len(keys):
        # Get the key based on user choice
        key = keys[choice - 1]
        # Return the value associated with the key
        return options_dict[key]

    return f"Invalid choice. Please choose a number between 1 and {len(keys)}."

def choose_options_in_dict(options_dict):
    # Display options to the user
    print("Choose an option:")
    for i, key in enumerate(options_dict.keys(), 1):
        print(f"{i}. {key}")

    # Prompt the user to choose an option
    user_input = int(input("Enter the number of your choice: "))

    # Get the value for the chosen key and print it
    result = get_choice_info(choice = user_input,
                             options_dict = options_dict)
    print(result)
    return result
