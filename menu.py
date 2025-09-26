from utilities.console_utils import *
from utilities.input_utils import *
import time

''' METHODS: User Interface '''
# [ UI ]: Navigate to 'Databases' menu
def go_to_databases():
    pass

# [ UI ]: Navigate to 'Tables' menu
def go_to_tables():
    pass

# [ UI ]: Navigate to 'Data Operations' menu
def go_to_data_operations():
    pass

# [ UI ]: Navigate to 'Schema Tools' menu
def go_to_schema_tools():
    pass

# [ UI ]: Navigate to 'Utilities' menu
def go_to_utilities():
    pass

# [ UI ]: Navigate to 'Settings' menu
def go_to_settings():
    pass

# [ UI ]: Display main menu
def display_main_menu() -> None:
    clear_screen()
    index: int = 1 # to keep track of the current function's index

    menu_operations = [
        "Databases",
        "Tables",
        "Data Operations",
        "Schema Tools",
        "Utilities",
        "Settings",
        "Exit"
    ]

    # display menu operations
    display_header("ZenDB", "Main Menu", width=30, symbol="=")
    for index, operation in enumerate(menu_operations, start=1):
        display_function(index, operation)
    index = 1 # reset index counter
    display_format(32, symbol="=")

    # get user choice
    int_input: int = get_int("user choice", ["required"])

    # do operation based on user choice
    match int_input:
        case 1:
            go_to_databases()
        case 2:
            go_to_tables()
        case 3:
            go_to_data_operations()
        case 4:
            go_to_schema_tools()
        case 5:
            go_to_utilities()
        case 6:
            go_to_settings()
        case 7: # Exit system
            print("Exiting ZenDB...")
            time.sleep(2)