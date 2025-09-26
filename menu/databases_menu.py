# Imports: Utilities
from utils.console_utils import *
from utils.input_utils import *
from utils.settings import *

# Imports: Database Manager
from db_utils.database_manager import *

''' METHODS: Database Menu '''
# [ METHOD ]: Display existing databases
def display_databases_menu():
    display_databases()
    press_to_continue()

# [ METHOD ]: Create a new database
def create_new_database_menu():
    # display existing databases
    display_databases()

    while True:
        # prompt user to enter a database name
        db_name: str = get_str("database name", ['required'])

        # cancel creating database if user provided no database name
        if not db_name:
            info_message("Database creation cancelled")
            press_to_continue()
            return
        
        # ERROR: Existing database
        if check_database_exists(db_name):
            error_message(f"Database with name '{db_name}' already exists", 2)
        else: break
        
    # create database if unique database name
    create_new_database(db_name)

    press_to_continue()

# [ METHOD ]: Drop (delete) an existing database
def drop_database_menu():
    # display existing databases
    display_databases()

    while True:
        # prompt user to enter a database name
        db_name: str = get_str("database name", ['required'])

        # cancel creating database if user provided no database name
        if not db_name:
            info_message("Database dropping cancelled")
            press_to_continue()
            return
        
        # ERROR: Non-existing database
        if not check_database_exists(db_name):
            error_message(f"Database with name '{db_name}' does not exist", 2)
        else: break

    # drop (delete) database if existing
    drop_selected_database(db_name)

    press_to_continue()

# [ METHOD ]: Select an existing database
def select_database_menu():
    global settings, current_engine

    # display existing databases
    display_databases()

    while True:
        # prompt user to enter a database name
        db_name: str = get_str("database name ['none' to unselect]", ['required'])

        # unselect database
        if db_name == "none" or not db_name:
            settings["current_database"] = ""
            save_settings(settings)

            current_engine = None
            success_message(f"Disconnected to '{db_name}'!")
            press_to_continue()
            return # return to 'Databases' menu

        # ERROR: Non-existing database
        elif not check_database_exists(db_name):
            error_message(f"Database with name '{db_name}' does not exist", 2)
        else: break

    # save selected database name in 'config.json'
    settings["current_database"] = db_name
    save_settings(settings)

    # refer to the selected database for future database operations
    current_engine = select_database(db_name)
    success_message(f"Connected to database '{db_name}'!")
    
    press_to_continue()

# [ METHOD ]: Show selected database's details
def show_database_details_menu():
    # display current database details
    show_database_details()
    
    press_to_continue()