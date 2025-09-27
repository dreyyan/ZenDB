# Imports: SQLAlchemy
from sqlalchemy.orm import declarative_base # for defining database tables
from sqlalchemy import create_engine # for creating the db connection
from sqlalchemy.orm import Session, sessionmaker # factory for sessions
from sqlalchemy import Column, Integer, String, MetaData, Table, inspect, text # define table columns
from sqlalchemy_utils import database_exists, create_database, drop_database

# Imports: Utilities
from utils.console_utils import *
from utils.input_utils import *
from utils.settings import *

''' METHODS: Utilities '''
def require_engine() -> bool:
    global current_engine
    return current_engine is not None

''' METHODS: Databases '''
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
        error_message_with_delay(f"Database '{name}' already exists.", 2)

# [ METHOD ]: Drop a database if it exists
def drop_selected_database(name: str) -> None:
    engine = create_engine(f"{DATABASE_URL}/{name}", echo=False) # create engine for specified database name

    if check_database_exists(name):
        drop_database(engine.url)
        success_message(f"Database '{name}' has been dropped.")
    else:
        error_message_with_delay(f"Database '{name}' does not exist.", 2)

# [ METHOD ]: Select database
def connect_database(name: str):
    global current_engine, current_database, settings

    # unselect
    if not name:
        current_engine = None
        previous_database: str = current_database
        current_database = ""
        settings["current_database"] = ""
        save_settings(settings)
        success_message("Disconnected from database.")
        return None

    # If already connected to this database
    if name == current_database:
        error_message(f"Already connected to database: '{name}'")
        return current_engine
    
    try:
        connection_url = f"{DATABASE_URL}/{name}"
        current_engine = create_engine(connection_url, echo=False)
        current_database = name
        settings["current_database"] = name
        save_settings(settings)
        success_message(f"Connected to database: {name}!")
        return current_engine
    except Exception as e:
        error_message(f"Failed to connect: {e}")
        current_engine = None
        return None

# [ METHOD ]: Show current database details
def show_database_details():
    current_database = settings.get("current_database")

    if not current_database:
        error_message_with_delay("No database selected.", 2)
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
        error_message_with_delay(f"Database '{current_database}' not found.", 2)


''' METHODS: Tables '''
# [ METHOD ]: List all tables
def display_tables():
    global current_engine

    # Check if there’s an active engine
    if not require_engine() or current_engine is None:
        error_message("No engine available — cannot display tables")
        return
    
    inspector = inspect(current_engine)
    tables = inspector.get_table_names()

    # Display header
    display_center("[ Table List ]", 32)
    display_format(32, '=')

    if not tables:
        info_message("No tables found in the current database.")
    else:
        print("\nCurrent tables in the database:")
        for i, table in enumerate(tables, start=1):
            print(f"  {i}. {table}")

    display_format(32, '=')

# [ METHOD ]: List all tables
def list_tables():
    global current_engine

    # ERROR: no database connection
    if not require_engine() or current_engine is None:
        return []
    
    inspector = inspect(current_engine)
    return inspector.get_table_names()

# [ METHOD ]: Create a new table
def create_table(table_name: str, columns: list[Column]):
    global current_engine
    
    # ERROR: no database connection
    if current_engine is None:
        error_message_with_delay("No active database connection.", 2)
        return []
    
    metadata = MetaData()
    new_table = Table(table_name, metadata, *columns)
    metadata.create_all(current_engine)
    success_message(f"Table '{table_name}' created successfully!")

# [ METHOD ]: Drop a table
def drop_table(table_name: str):
    global current_engine
    
    # ERROR: no database connection
    if not require_engine() or current_engine is None:
        return
    
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=current_engine)
    metadata.drop_all(current_engine, [table])
    success_message(f"Table '{table_name}' dropped.")

# [ METHOD ]: Describe a table schema
def describe_table_schema(table_name: str):
    global current_engine
    
    # ERROR: no database connection
    if not require_engine() or current_engine is None:
        return []
    
    inspector = inspect(current_engine)
    columns = inspector.get_columns(table_name)
    
    display_center(f"[ {table_name} - Schema ]", 32)
    display_format(32, '=')
    for col in columns:
        print(f"{col['name']} - {col['type']} (nullable={col['nullable']})")
    display_format(32, '=')

# [ METHOD ]: Add a column
def add_column(table_name: str, col_name: str, col_type: str):
    global current_engine

    # ERROR: no database connection
    if not require_engine() or current_engine is None:
        return []

    col_type_sql = "INTEGER" if col_type == "int" else "VARCHAR"
    with current_engine.connect() as conn:
        conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type_sql};"))
    success_message(f"Column '{col_name}' added to '{table_name}'.")

# [ METHOD ]: Remove a column
def remove_column(table_name: str, col_name: str):
    global current_engine

    # ERROR: no database connection
    if not require_engine() or current_engine is None:
        return []
    
    with current_engine.connect() as conn:
        conn.execute(text(f"ALTER TABLE {table_name} DROP COLUMN {col_name};"))
    success_message(f"Column '{col_name}' removed from '{table_name}'.")

# [ METHOD ]: Rename a table
def rename_table(new_name: str):
    global current_engine, current_table

    # ERROR: no database connection
    if not require_engine() or current_engine is None:
        return []

    # Update current table's name
    current_table = new_name

    with current_engine.connect() as conn:
        conn.execute(text(f"ALTER TABLE {current_table} RENAME TO {new_name};"))
    success_message(f"Table renamed from '{current_table}' to '{new_name}'.")


''' METHODS: Data Operations '''
# [ METHOD ]: View all rows
def view_all_rows(engine, table_class):
    with Session(engine) as session:
        rows = session.query(table_class).all()
        if not rows:
            error_message_with_delay("No rows found.", 2)
        else:
            display_center(f"[ {table_class.__tablename__} - All Rows ]", 32)
            for row in rows:
                data = {k: v for k, v in row.__dict__.items() if not k.startswith("_")}
                print(data)

# [ METHOD ]: View rows with filters
def view_rows_with_filters(engine, table_class, filter_query: str):
    with Session(engine) as session:
        query = f"SELECT * FROM {table_class.__tablename__} WHERE {filter_query}"
        result = session.execute(text(query)).fetchall()
        if not result:
            error_message_with_delay("No rows match the filter.", 2)
        else:
            display_center(f"[ {table_class.__tablename__} - Filtered Rows ]", 32)
            for r in result:
                print(r)

# [ METHOD ]: Update row(s)
def update_row(engine, table_class, filter_query: str, updates: dict):
    with Session(engine) as session:
        query = session.query(table_class).filter(text(filter_query))
        rows = query.all()
        if not rows:
            error_message_with_delay("No matching rows found.", 2)
            return

        for row in rows:
            for key, val in updates.items():
                setattr(row, key, val)
        session.commit()
        success_message(f"{len(rows)} row(s) updated.")

# [ METHOD ]: Delete row(s)
def delete_row(engine, table_class, filter_query: str):
    with Session(engine) as session:
        query = session.query(table_class).filter(text(filter_query))
        rows = query.all()
        if not rows:
            error_message_with_delay("No matching rows found.", 2)
            return

        confirm = input(f"Delete {len(rows)} row(s)? (y/n): ").lower()
        if confirm == "y":
            for row in rows:
                session.delete(row)
            session.commit()
            success_message(f"{len(rows)} row(s) deleted.")
        else:
            error_message_with_delay("Delete operation cancelled.", 2)

# [ METHOD ]: Batch insert
def batch_insert(engine, table_class, rows_data: list[dict]):
    with Session(engine) as session:
        objs = [table_class(**data) for data in rows_data]
        session.add_all(objs)
        session.commit()
        success_message(f"{len(rows_data)} row(s) inserted.")


''' METHODS: Data Operations '''
# [ METHOD ]: Insert row(s) with guided prompts
def insert_row(table_class):
    global current_engine

    with Session(current_engine) as session:
        # get column info
        columns = table_class.__table__.columns
        values = {}

        for col in columns:
            if col.primary_key:  # skip PK if auto-generated
                continue
            val = input(f"Enter value for {col.name} ({col.type}): ")
            values[col.name] = val if val != "" else None

        new_row = table_class(**values)
        session.add(new_row)
        session.commit()
        success_message("Row inserted successfully!")