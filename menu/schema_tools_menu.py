# Imports: SQLAlchemy
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

# Imports: Utilities
from utils.console_utils import *
from utils.input_utils import *
from utils.settings import *

# Imports: Database Manager
from db_utils.database_manager import *

# [ UI ]: Generate model class from table
def generate_model_class_menu():
    display_header("ZenDB", "Generate Model Class", width=32, symbol="=")

    if not require_engine():
        return

    # Show available tables
    inspector = inspect(current_engine)
    tables = inspector.get_table_names()

    if not tables:
        error_message("No tables found in current database.")
        press_to_continue()
        return

    print("\nAvailable tables:")
    for idx, t in enumerate(tables, start=1):
        print(f"{idx}. {t}")

    table_name = get_str("table name", ["required"])
    if table_name not in tables:
        error_message_with_delay(f"Table '{table_name}' does not exist.", 3)
        return

    # Call implementation
    generate_model_class(table_name)
    press_to_continue()


# [ UI ]: View generated model class code
def view_model_class_code_menu():
    display_header("ZenDB", "View Model Class Code", width=32, symbol="=")

    if not require_engine():
        return

    table_name = get_str("table name", ["required"])
    view_model_class_code(table_name)
    press_to_continue()


# [ UI ]: Sync model to table (create table if missing)
def sync_model_to_table_menu():
    display_header("ZenDB", "Sync Model to Table", width=32, symbol="=")

    if not require_engine():
        return

    table_name = get_str("table name", ["required"])
    sync_model_to_table(table_name)
    press_to_continue()