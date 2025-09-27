# Imports: SQLAlchemy
from sqlalchemy import Engine, create_engine # for creating the db connection

# Imports: Utilities
from utils.console_utils import display_format

# Imports: Standard
import json
import logging

# SETTINGS: Links/Directories
CONFIG_FILE = "config.json"
DATABASE_URL = "postgresql+psycopg2://postgres:qwpoeriuty123@localhost:5432"

current_database: str = "postgres"
current_table: str = ""

# [ UTILITY ]: Load current settings from 'config.json'
def load_settings():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

# [ UTILITY ]: Save current settings from 'config.json'
def save_settings(settings: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(settings, f, indent=4)

# load current settings
settings = load_settings()

# [ UTILITY ]: Display currently selected database
def display_selected_database():
    global current_database, settings
    settings = load_settings()  # reload config.json
    current_database = settings.get("current_database", "")

    if not current_database:
        print(f"No connection.")
    else:
        print(f"Connected to: {current_database}")

    display_format(32, symbol="=")

# [ UTILITY ]: Display currently selected table
def display_selected_table():
    global current_table, current_database, settings

    # if no database connection, don't display the previously selected table
    if current_database == "":
        print("No connection.")
        display_format(32, symbol="=")
        return
    
    settings = load_settings() # reload config.json to reflect changes
    current_table = settings.get("current_table", "")

    if current_table == "":
        print("No selected table.")
    else:
        print(f"Selected Table: {current_table}")

    display_format(32, symbol="=")

logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING) # SETTING: don't show INFO logs

settings = load_settings()  # Load saved settings from config.json
current_database = settings.get("current_database", "")
current_table = settings.get("current_table", "")
current_engine = None

# Auto-load engine if database is already selected
if current_database:
    current_engine = create_engine(f"{DATABASE_URL}/{current_database}")