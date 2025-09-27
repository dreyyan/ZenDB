# Imports: SQLAlchemy
from sqlalchemy import Column, Integer, String, MetaData, Table, inspect, text # define table columns
from sqlalchemy.engine import Engine

# Imports: Utilities
from utils.console_utils import *
from utils.input_utils import *

# Imports: Database Manager
from db_utils.database_manager import *

''' METHODS: Tables Menu '''
# [ METHOD ]: Display existing tables
def display_tables_menu():
    global current_engine

    # display header
    display_header("ZenDB", "Display Tables", width=30, symbol="=")

    display_tables()

    press_to_continue()

# [ METHOD ]: Create a new table
def create_new_table_menu():
    global current_engine

    # display header
    display_header("ZenDB", "Create New Table", width=30, symbol="=")

    # ERROR: No database connection
    if current_engine is None:
        error_message("No active database connection.")
        press_to_continue()
        return
    
    # display existing tables
    display_tables()

    while True:
        # prompt user to enter a table name
        table_name: str = get_str("table name", ['required'])

        # exit if no table name provided
        if not table_name:
            info_message("Table creation cancelled.")
            press_to_continue()
            return
        else:
            # check if table exists
            inspector = inspect(current_engine)
            tables = inspector.get_table_names()

            # ERROR: Existing table
            if table_name in tables:
                error_message_with_delay(f"Table '{table_name}' already exists.", 2)
            else: break

    columns = []

    # this loop runs until user inputs blank (to finish)
    while True:
        # prompt user to enter column name
        col_name = input("Column name (leave blank to finish): ").strip()

        # finish creating table
        if not col_name:
            break

        # ERROR: Existing same name column
        if any(c.name == col_name for c in columns):
            error_message(f"Column '{col_name}' already added.")
            press_to_continue()
            continue

        while True:
            # prompt user to enter column type
            col_type = input("Column type (int, str): ").strip().lower()

            # create column based on type specified
            if col_type == "int":
                col = Column(col_name, Integer)
                break
            elif col_type == "str":
                # Let user specify optional length for String
                length = input("Max length (press Enter for default): ").strip()
                if length.isdigit():
                    col = Column(col_name, String(int(length)))
                else:
                    col = Column(col_name, String)
                break
            else:
                # ERROR: Invalid type
                error_message("Invalid type. Use 'int' or 'str'.")
                press_to_continue()

        # ask user if column is a primary key
        pk = input("Primary key? (y/n): ").lower()
        if pk == "y":
            col.primary_key = True

        # add input column to the list of columns to add
        columns.append(col)

    # ERROR: No column input
    if not columns:
        error_message("No columns defined. Table not created.")
        press_to_continue()
        return

    # create table if unique table name
    try:
        # convert dashes (-) to underscores (_) before creating table
        table_name = table_name.replace("-", "_")

        create_table(table_name, columns)
    except Exception as e:
        error_message(f"Failed to create table: {e}")

    press_to_continue()

# [ METHOD ]: Drop (delete) an existing table
def drop_table_menu():
    global current_engine

    # display header
    display_header("ZenDB", "Drop Table", width=30, symbol="=")

    # ERROR: No database connection
    if current_engine is None:
        error_message("No active database connection.")
        press_to_continue()
        return

    # display existing tables
    inspector = inspect(current_engine)
    tables = inspector.get_table_names()

    # ERROR: No existing tables
    if not tables:
        error_message("No tables exist in the current database.")
        press_to_continue()
        return

    # display existing tables
    display_tables()

    while True:
        # prompt user to enter a table name
        table_name: str = get_str("database name", ['required'])

        # exit if no table name provided
        if table_name == "":
            info_message("Dropping cancelled.")
            press_to_continue()
            return
        # ERROR: Non-existing table
        elif table_name not in tables:
            error_message_with_delay(f"Table '{table_name}' does not exist.", 2)
        else: break

    while True:
        # confirm databse dropping to user
        user_confirmation = input("Are you sure? This process cannot be undone [yes/no]: ")
        
        if user_confirmation == "yes":
            try:
                drop_table(table_name)
                break
            except Exception as e:
                error_message(f"Failed to drop table: {e}")
        elif user_confirmation == "no":
            info_message("Table dropping cancelled.")
            press_to_continue()
            return
        else:
            error_message_with_delay("Invalid input, please enter 'yes' to confirm dropping and 'no to cancel.", 3)

    press_to_continue()

# [ METHOD ]: Select an existing table
def select_table_menu():
    global current_engine, current_table

    # display header
    display_header("ZenDB", "Select Table", width=30, symbol="=")

    # ERROR: No active database connection
    if current_engine is None:
        error_message("No active database connection.")
        press_to_continue()
        return

    # get list of tables
    inspector = inspect(current_engine)
    tables = inspector.get_table_names()

    # ERROR: No tables exist
    if not tables:
        error_message("No tables exist in the current database.")
        press_to_continue()
        return

    # display available tables
    display_tables()

    # prompt user for selection
    choice = get_str("table name ['none' to unselect]", ["required"])

    # just exit if Enter is pressed
    if not choice:
        info_message("Table selection cancelled.")
        press_to_continue()
        return
    
    # unselect table if explicitly typed "none"
    if choice.lower() == "none":
        select_table("")  # disconnect/unselect
        press_to_continue()
        return
        
    # check if already selected
    if choice == current_table:
        error_message(f"Table '{choice}' is already selected.")
        press_to_continue()
        return
    
    # validate choice
    if choice in tables:
        current_table = choice
        settings["current_table"] = current_table
        save_settings(settings)
        success_message(f"Selected table: {current_table}")
    else:
        error_message(f"Table '{choice}' does not exist.")
        press_to_continue()
        return

    press_to_continue()

# [ METHOD ]: Display and describe a selected table's schema (column fields)
def describe_table_schema_menu():
    global current_engine, current_table

    # display header
    display_header("ZenDB", "Table Schema", width=30, symbol="=")

    # ERROR: No database connection
    if current_engine is None:
        error_message("No active database connection.")
        press_to_continue()
        return
    
    if not current_table:
        error_message("No table selected.")
        press_to_continue()
        return

    # display each column fields
    describe_table_schema(current_table)
    press_to_continue()

# [ METHOD ]: Add or remove table columns from a selected table
def add_or_remove_table_columns_menu():
    global current_engine, current_table

    # display header
    display_header("ZenDB", "Modify Table Columns", width=30, symbol="=")

    # ERROR: No database connection
    if current_engine is None:
        error_message("No active database connection.")
        press_to_continue()
        return
    
    # ERROR: No selected table
    if not current_table:
        error_message("No table selected.")
        press_to_continue()
        return

    # Reload table list to ensure rename is reflected
    inspector = inspect(current_engine)
    if current_table not in inspector.get_table_names():
        error_message(f"Selected table '{current_table}' does not exist anymore.")
        press_to_continue()
        return

    # Display schema for the selected table
    describe_table_schema(current_table)

    action = input("Do you want to add or remove a column? (add/remove): ").strip().lower()

    if action == "add":
        col_name = input("New column name: ").strip()
        col_type = input("Column type (int/str): ").strip().lower()
        add_column(current_table, col_name, col_type)
    elif action == "remove":
        col_name = input("Column name to remove: ").strip()
        remove_column(current_table, col_name)
    else:
        error_message("Invalid action.")
        press_to_continue()
        return

    press_to_continue()

# [ METHOD ]: Rename a selected table
def rename_table_menu():
    global current_engine, current_table

    # display header
    display_header("ZenDB", "Rename Table", width=30, symbol="=")

    # ERROR: No database connection
    if current_engine is None:
        error_message("No active database connection.")
        press_to_continue()
        return

    # display old table name
    print(f"Old table name: {current_table}")

    # enter new table name
    new_name = input("Enter new table name: ").strip()

    # ERROR: Empty new table name
    if not new_name:
        error_message("New table name cannot be empty.")
        press_to_continue()
        return

    # rename table if existing
    rename_table(new_name)

    press_to_continue()