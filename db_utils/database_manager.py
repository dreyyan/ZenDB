from sqlalchemy.orm import declarative_base # for defining database tables
from sqlalchemy import create_engine # for creating the db connection
from sqlalchemy.orm import Session, sessionmaker # factory for sessions
from sqlalchemy import Column, Integer, String, text # define table columns
from sqlalchemy_utils import database_exists, create_database, drop_database

# Imports: Utilities
from utils.console_utils import *
from utils.input_utils import *
from utils.settings import *

''' METHODS: Database Operations '''
# [ METHOD ]: Display existing databases
def display_databases() -> None:
    engine = create_engine(DATABASE_URL)

    # display database names
    with engine.connect() as conn:
        result = conn.execute(text("SELECT datname FROM pg_database WHERE datistemplate = false;"))
        databases = result.fetchall()

    display_center("[ Database List ]", 32)
    display_format(32, '=')
    for db in databases:
        print(f"* {db[0]}")
    display_format(32, '=')

# [ METHOD ]: Attempt to create a database if not existing
def check_database_exists(name: str) -> bool:
    engine = create_engine(f"{DATABASE_URL}/{name}", echo=False) # create engine for specified database name
    return database_exists(engine.url)

# [ METHOD ]: Attempt to create a database if not existing
def create_new_database(name: str) -> None:
    engine = create_engine(f"{DATABASE_URL}/{name}", echo=False) # create engine for specified database name

    # create database if non-existing
    if not database_exists(engine.url):
        create_database(engine.url) # utility to create database
        success_message(f"Database '{name}' created!")
    else: # ERROR: Already existing database
        error_message(f"Database '{name}' already exists.")
        press_to_continue()

# [ METHOD ]: Drop a database if it exists
def drop_selected_database(name: str) -> None:
    engine = create_engine(f"{DATABASE_URL}/{name}", echo=False) # create engine for specified database name

    if check_database_exists(name):
        drop_database(engine.url)
        success_message(f"Database '{name}' has been dropped.")
    else:
        error_message(f"Database '{name}' does not exist.")

# [ METHOD ]: Select database
def select_database(name: str):
    # return no engine to unselect a databsae
    if not name:
        return None
    return create_engine(f"{DATABASE_URL}/{name}", echo=False)

# [ METHOD ]: Show current database details
def show_database_details():
    current_database = settings.get("current_database")

    if not current_database:
        error_message("No database selected.")
        return

    # Create engine connected to the selected database
    engine = create_engine(f"{DATABASE_URL}/{current_database}", echo=False)

    with engine.connect() as conn:
        result = conn.execute(text(f"""
            SELECT
                datname AS database_name,
                pg_size_pretty(pg_database_size(datname)) AS size,
                pg_encoding_to_char(encoding) AS encoding,
                datcollate AS collation,
                datctype AS ctype,
                datistemplate AS is_template
            FROM pg_database
            WHERE datname = :dbname;
        """), {"dbname": current_database})

        details = result.fetchone()

    if details:
        display_center(f"[ Database - '{current_database}' ]", 32)
        display_format(32, '=')
        print(f"{'Name':>12}: {details.database_name}")
        print(f"{'Size':>12}: {details.size}")
        print(f"{'Encoding':>12}: {details.encoding}")
        print(f"{'Collation':>12}: {details.collation}")
        print(f"{'CType':>12}: {details.ctype}")
        print(f"{'Template':>12}: {details.is_template}")
        display_format(32, '=')
    else:
        error_message(f"Database '{current_database}' not found.")