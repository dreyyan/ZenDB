# Imports: Utilities
from utils.console_utils import *

# Imports: Standard
import json

CONFIG_FILE = "config.json"

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