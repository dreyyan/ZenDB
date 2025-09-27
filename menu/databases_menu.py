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
            info_message("Database creation cancelled.")
            press_to_continue()
            return
        
        # ERROR: Existing database
        if check_database_exists(db_name):
            error_message_with_delay(f"Database with name '{db_name}' already exists.", 2)
        else: break
        
    # create database if unique database name
    create_new_database(db_name)

    press_to_continue()

# [ METHOD ]: Drop (delete) an existing database
def drop_database_menu():
    global current_database, current_engine, settings

    # display existing databases
    display_databases()

    while True:
        # prompt user to enter a database name
        db_name: str = get_str("database name", ['required'])

        # cancel creating database if user provided no database name
        if not db_name:
            info_message("Database dropping cancelled.")
            press_to_continue()
            return
        
        # ERROR: Non-existing database
        if not check_database_exists(db_name):
            error_message_with_delay(f"Database with name '{db_name}' does not exist.", 2)
        else: break

    while True:
        # confirm databse dropping to user
        user_confirmation = input("Are you sure? This process cannot be undone [yes/no]: ")

        if user_confirmation == "yes":
            # drop (delete) database if existing
            drop_selected_database(db_name)

            # If we dropped the currently connected database, clear it
            if db_name == current_database:
                current_database = ""
                current_engine = None

                settings["current_database"] = ""
                save_settings(settings)
                
                info_message("Dropped the connected database — connection cleared.")
            break

        elif user_confirmation == "no":
            info_message("Database dropping cancelled.")
            press_to_continue()
            return
        else:
            error_message_with_delay("Invalid input, please enter 'yes' to confirm dropping and 'no to cancel.", 3)

    press_to_continue()

# [ METHOD ]: Select an existing database
def connect_database_menu():
    global settings, current_engine, current_database

    # display existing databases
    display_databases()

    while True:
        # prompt user to enter a database name
        db_name: str = get_str("database name ['none' to unselect]", ['required'])

        # just exit if Enter is pressed
        if not db_name:
            info_message("Database selection cancelled.")
            press_to_continue()
            return

        # unselect database if explicitly typed "none"
        if db_name.lower() == "none":
            connect_database("")  # disconnect/unselect
            press_to_continue()
            return

        # ERROR: Non-existing database
        elif not check_database_exists(db_name):
            error_message_with_delay(f"Database '{db_name}' does not exist.", 2)
        else:
            break
        
    connect_database(db_name)
    press_to_continue()

# [ METHOD ]: Show selected database's details
def show_database_details_menu():
    # display current database details
    show_database_details()
    
    press_to_continue()