# Imports: SQLAlchemy
from sqlalchemy import create_engine # for creating the db connection

# Imports: Utilities
from utils.console_utils import display_format

# Imports: Standard
import json

# Links/Directories
CONFIG_FILE = "config.json"
DATABASE_URL = "postgresql+psycopg2://postgres:qwpoeriuty123@localhost:5432"

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
    current_database: str = settings.get("current_database")
    print(f"Selected: {"N/A" if current_database == "" else current_database}")
    display_format(32, symbol="=")

settings = load_settings() # Load saved settings from config.json
current_engine = None # Initialize current_engine

# Auto-load engine if database is already selected
if settings.get("current_database"):
    current_engine = create_engine(f"{DATABASE_URL}/{settings['current_database']}", echo=True)

# load current settings
settings = load_settings()
current_engine = None