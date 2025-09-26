from sqlalchemy.orm import declarative_base # for defining database tables
from sqlalchemy import create_engine # for creating the db connection
from sqlalchemy.orm import Session, sessionmaker # factory for sessions
from sqlalchemy import Column, Integer, String, text # define table columns
from sqlalchemy_utils import database_exists, create_database

from utilities.console_utils import display_format, clear_screen

DATABASE_URL = "postgresql+psycopg2://postgres:qwpoeriuty123@localhost:5432"

# METHODS: Database

# [ METHOD ]: Attempt to create a database if not existing
def attempt_create_database(name: str) -> None:
    engine = create_engine(f"{DATABASE_URL}/{name}", echo=True) # create engine for specified database name

    # create database if non-existing
    if not database_exists(engine.url):
        create_database(engine.url) # utility to create database
        print(f"Database '{name}' created!")
    else: # ERROR: Already existing database
        print(f"Database '{name}' already exists.")

# [ METHOD ]: Display existing databases
def display_databases() -> None:
    engine = create_engine(DATABASE_URL)

    # display database names
    with engine.connect() as conn:
        result = conn.execute(text("SELECT datname FROM pg_database WHERE datistemplate = false;"))
        databases = result.fetchall()

    print("[ Database List ]")
    display_format(17, '=')
    for db in databases:
        print(f"* {db[0]}")
    display_format(17, '=')