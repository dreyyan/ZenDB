# Imports: Menus
from databases_menu import *
from tables_menu import *

# Imports: Utilities
from utilities.console_utils import *
from utilities.input_utils import *
from utilities.settings import *

# Imports: Standard
import time

# load current settings
settings = load_settings()

''' METHODS: User Interface '''
# [ UI ]: Navigate to 'Databases' menu
def go_to_databases():
    while True:
        clear_screen()
        index: int = 1 # to keep track of the current function's index

        database_operations = [
            "Display Databases",
            "Create New Database",
            "Drop Database",
            "Select Database",
            "Show Database Details",
            "Back"
        ]

        # display menu operations
        display_header("ZenDB", "Databases", width=30, symbol="=")

        # display current selected database
        display_selected_database()

        for index, operation in enumerate(database_operations, start=1):
            display_function(index, operation)
        index = 1 # reset index counter
        display_format(32, symbol="=")

        # get user choice
        int_input: int = get_int("user choice", ["required"])

        # do operation based on user choice
        match int_input:
            case 1:
                ()
            case 2:
                create_new_database_menu()
            case 3:
                drop_database_menu()
            case 4:
                select_database_menu()
            case 5:
                show_database_details_menu()
            case 6:
                break

# [ UI ]: Navigate to 'Tables' menu
def go_to_tables():
    while True:
        clear_screen()
        index: int = 1 # to keep track of the current function's index

        tables_operations = [
            "Display Tables",
            "Create New Table",
            "Drop Table",
            "Describe Table Schema",
            "Add/Remove Table Columns",
            "Rename Table",
            "Back"
        ]

        # display menu operations
        display_header("ZenDB", "Tables", width=30, symbol="=")

        # display current selected database
        display_selected_database()

        for index, operation in enumerate(tables_operations, start=1):
            display_function(index, operation)
        index = 1 # reset index counter
        display_format(32, symbol="=")

        # get user choice
        int_input: int = get_int("user choice", ["required"])

        # do operation based on user choice
        match int_input:
            case 1:
                display_tables_menu()
            case 2:
                create_new_table_menu()
            case 3:
                drop_table_menu()
            case 4:
                describe_table_schema_menu()
            case 5:
                add_or_remove_table_columns_menu()
            case 6:
                rename_table_menu()
            case 7:
                break

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
    while True:
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
                print("Exiting ZenDB...", end="")
                time.sleep(2)
                exit(0)