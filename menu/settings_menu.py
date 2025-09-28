# Imports: SQLAlchemy
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

# Imports: Utilities
from utils.console_utils import *
from utils.input_utils import *
from utils.settings import *

# Imports: Database Manager
from db_utils.database_manager import *

# [ UI ]: Configure default DB connection
def configure_default_database_connection_menu():
    display_header("ZenDB", "Configure Default DB Connection", width=32, symbol="=")
    configure_default_database_connection()
    press_to_continue()

# [ UI ]: Manage multiple DB connections
def manage_database_connections_menu():
    display_header("ZenDB", "Manage Database Connections")
    manage_database_connections()
    press_to_continue()

# [ UI ]: Set naming conventions
def set_naming_conventions_for_models_menu():
    display_header("ZenDB", "Set Naming Conventions for Models", width=32, symbol="=")
    set_naming_conventions_for_models()
    press_to_continue()

# [ UI ]: Configure logging
def configure_logging_menu():
    display_header("ZenDB", "Configure Logging", width=32, symbol="=")
    configure_logging()
    press_to_continue()