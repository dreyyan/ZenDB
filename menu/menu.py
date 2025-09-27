# Here's the modified code for menu.py. No changes needed here, but including for completeness.

# Imports: Database
from db_utils.database_manager import connect_database

# Imports: Menus
from .databases_menu import *
from .tables_menu import *
from .data_operations_menu import *

# Imports: Utilities
from utils.console_utils import *
from utils.input_utils import *
from utils.settings import *

# Imports: Standard
import time

''' METHODS: User Interface '''
# [ UI ]: Navigate to 'Databases' menu
def go_to_databases():
    global settings, current_database, current_engine

    while True:
        clear_screen()

        database_operations = [
            "Back",
            "Display Databases",
            "Create New Database",
            "Drop Database",
            "Connect Database",
            "Show Database Details"
        ]

        # display 'Databases' header
        display_header("ZenDB", "Databases", width=30, symbol="=")
        display_selected_database() # display current selected database
        display_function(0, "Exit")
        print("=" * 32)

        # display 'Databases' operations
        for index, operation in enumerate(database_operations[1:], start=1):
            display_function(index, operation)
        display_format(32, symbol="=")

        # get user choice
        int_input: int = get_int("user choice", ["required"])

        clear_screen() # clear console screen before navigating

        # do operation based on user choice
        match int_input:
            case 0:
                break
            case 1:
                display_databases_menu()
            case 2:
                create_new_database_menu()
            case 3:
                drop_database_menu()
            case 4:
                connect_database_menu()
            case 5:
                show_database_details_menu()

# [ UI ]: Navigate to 'Tables' menu
def go_to_tables():
    while True:
        clear_screen()

        tables_operations = [
            "Back",
            "Display Tables",
            "Create New Table",
            "Drop Table",
            "Select Table",
            "Describe Table Schema",
            "Add/Remove Table Columns",
            "Rename Table"
        ]

        # display 'Databases' header
        display_header("ZenDB", "Tables", width=30, symbol="=")
        display_selected_table() # display current selected database
        display_function(0, "Exit")
        print("=" * 32)

        # display 'Databases' operations
        for index, operation in enumerate(tables_operations[1:], start=1):
            display_function(index, operation)
        display_format(32, symbol="=")

        # get user choice
        int_input: int = get_int("user choice", ["required"])

        clear_screen() # clear console screen before navigating
        
        # do operation based on user choice
        match int_input:
            case 0:
                break
            case 1:
                display_tables_menu()
            case 2:
                create_new_table_menu()
            case 3:
                drop_table_menu()
            case 4:
                select_table_menu()
            case 5:
                describe_table_schema_menu()
            case 6:
                add_or_remove_table_columns_menu()
            case 7:
                rename_table_menu()

# [ UI ]: Navigate to 'Data Operations' menu
def go_to_data_operations():
    while True:
        clear_screen()

        data_operations = [
            "Back",
            "Insert Row(s)",
            "View All Rows",
            "View Rows /w Filter",
            "Update Row(s)",
            "Delete Row(s)"
        ]

        # display 'Data Operations' header
        display_header("ZenDB", "Data Operations", width=30, symbol="=")
        display_selected_database() # display current selected database
        display_function(0, "Exit")
        print("=" * 32)

        # display 'Data' operations
        for index, operation in enumerate(data_operations[1:], start=1):
            display_function(index, operation)
        display_format(32, symbol="=")

        # get user choice
        int_input: int = get_int("user choice", ["required"])

        clear_screen() # clear console screen before navigating

        # do operation based on user choice
        match int_input:
            case 0:
                break
            case 1:
                insert_rows_menu()
            case 2:
                view_all_rows_menu()
            case 3:
                view_rows_with_filter_menu()
            case 4:
                update_rows_menu()
            case 5:
                delete_rows_menu()

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
    global current_engine, current_database, settings

    if settings.get("current_database") and current_engine is None:
        connect_database(settings["current_database"])

    while True:
        clear_screen()

        menu_operations = [
            "Exit",
            "Databases",
            "Tables",
            "Data Operations",
            "Schema Tools",
            "Utilities",
            "Settings",
        ]

        # display 'Main Menu' header
        display_header("ZenDB", "Main Menu", width=30, symbol="=")
        display_function(0, "Exit")
        print("=" * 32)

        # display 'Main Menu' operations
        for index, operation in enumerate(menu_operations[1:], start=1):
            display_function(index, operation)
        display_format(32, symbol="=")

        # get user choice
        int_input: int = get_int("user choice", ["required"])

        # do operation based on user choice
        match int_input:
            case 0: # Exit system
                print("Exiting ZenDB...", end="")
                exit(0)
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