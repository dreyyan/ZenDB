# Imports: Utilities
from utils.console_utils import *
from utils.input_utils import *
from utils.settings import *

# Imports: Database Manager
from db_utils.database_manager import *

# load current settings
settings = load_settings()

''' METHODS: Database Menu '''
# [ METHOD ]: Display existing databases
def display_databases_menu():
    display_databases()
    press_to_continue()
    pass

# [ METHOD ]: Create a new database
def create_new_database_menu():
    # display existing databases
    display_databases()

    while True:
        # prompt user to enter a database name
        db_name: str = get_str("Database Name", ['required'])

        # ERROR: Existing database
        if check_database_exists(db_name):
            error_message(f"Database with name '{db_name} already exists'")
            press_to_continue()
        else: break
        
    # create database if unique database name
    create_new_database(db_name)

    press_to_continue()
    pass

# [ METHOD ]: Drop (delete) an existing database
def drop_database_menu():
    # display existing databases
    display_databases()

    while True:
        # prompt user to enter a database name
        db_name: str = get_str("Database Name", ['required'])

        # ERROR: Non-existing database
        if not check_database_exists(db_name):
            error_message(f"Database with name '{db_name} does not exist'")
            press_to_continue()
        else: break

    # drop (delete) database if existing
    drop_selected_database(db_name)

    press_to_continue()
    pass

# [ METHOD ]: Select an existing database
def select_database_menu():
    # display existing databases
    display_databases()

    while True:
        # prompt user to enter a database name
        db_name: str = get_str("Database Name", ['required'])

        # ERROR: Non-existing database
        if not check_database_exists(db_name):
            error_message(f"Database with name '{db_name} does not exist'")
            press_to_continue()
        else: break

    # save selected database name in 'config.json'
    settings["current_database"] = db_name
    save_settings(settings)

    # refer to the selected database for future database operations
    engine = select_database(db_name)
    print(f"Connected to database '{db_name}'!")
    
    press_to_continue()
    pass

# [ METHOD ]: Show selected database's details
def show_database_details_menu():
    # display current database details
    show_database_details()
    
    press_to_continue()
    pass