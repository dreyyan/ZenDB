# Here's the modified code for database_manager.py. Updated drop_selected_database to force terminate any active connections before dropping the database. This ensures the drop succeeds even if there are lingering connections. Also, changed create_new_database, check_database_exists, and drop_selected_database to use URL strings instead of creating unnecessary engines.

# Imports: SQLAlchemy
from sqlalchemy.orm import declarative_base # for defining database tables
from sqlalchemy import create_engine # for creating the db connection
from sqlalchemy.orm import Session, sessionmaker # factory for sessions
from sqlalchemy import Column, Integer, String, MetaData, Table, inspect, text # define table columns
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.exc import SQLAlchemyError

# Imports: Utilities
from db_utils.database_models import Base
from utils.console_utils import *
from utils.input_utils import *
from utils.settings import *

# Imports: File Formats
import pandas as pd

# Globals
db_connections = {}
naming_conventions = {
    "class": "PascalCase",
    "table": "snake_case",
    "column": "snake_case"
}
logging_config = {
    "enabled": False,
    "level": "INFO",
    "file": None
}

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

    display_format(32, '=')
    display_center("Available Databases:", 32)
    for db in databases:
        print(f"* {db[0]}")
    display_format(32, '=')

# [ METHOD ]: Attempt to create a database if not existing
def check_database_exists(name: str) -> bool:
    return database_exists(f"{DATABASE_URL}/{name}")

# [ METHOD ]: Attempt to create a database if not existing
def create_new_database(name: str) -> None:
    url = f"{DATABASE_URL}/{name}"

    # create database if non-existing
    if not database_exists(url):
        create_database(url) # utility to create database
        success_message(f"Database '{name}' created!")
    else: # ERROR: Already existing database
        error_message_with_delay(f"Database '{name}' already exists.", 2)

# [ METHOD ]: Drop a database if it exists
def drop_selected_database(name: str) -> None:
    if not check_database_exists(name):
        error_message_with_delay(f"Database '{name}' does not exist.", 2)
        return

    # Connect to default 'postgres' database to execute commands
    default_engine = create_engine(f"{DATABASE_URL}/postgres", echo=False)

    try:
        with default_engine.connect() as conn:
            # Ensure autocommit mode for termination
            conn.execution_options(isolation_level="AUTOCOMMIT")

            # Terminate all connections to the target database
            terminate_query = text(f"""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = :dbname
                  AND pid <> pg_backend_pid();
            """)
            conn.execute(terminate_query, {"dbname": name})

            # Now drop the database
            drop_query = text(f"DROP DATABASE {name};")
            conn.execute(drop_query)

        success_message(f"Database '{name}' has been dropped.")
    except Exception as e:
        error_message(f"Failed to drop database: {str(e)}")

# [ METHOD ]: Select database
def connect_database(name: str):
    global current_engine, current_database, settings

    # unselect
    if not name:
        current_engine = None
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

        with current_engine.connect() as conn:
            pass # Forces an actual connection test

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
    tables = inspector.get_table_names(schema="public")

    # Display header
    display_center("[ Table List ]", 32)
    display_format(32, '=')

    if not tables:
        info_message("No tables found in the current database.")
    else:
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
    global current_engine, current_table, settings
    
    # ERROR: no database connection
    if not require_engine() or current_engine is None:
        return
    
    try:
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=current_engine)
        metadata.drop_all(current_engine, [table])
        success_message(f"Table '{table_name}' dropped successfully.")

        # If the dropped table is the current one
        if table_name == current_table:
            current_table = ""
            settings["current_table"] = ""
            save_settings(settings)

    except Exception as e:
        error_message(f"Failed to drop table: {e}")

# [ METHOD ]: Select a table
def select_table(name: str):
    global current_table, settings

    # Unselect table if empty
    if not name:
        current_table = ""
        settings["current_table"] = ""
        save_settings(settings)
        success_message("Unselected table.")
        return None

    # If already selected
    if name == current_table:
        error_message(f"Already selected table: '{name}'")
        return current_table

    try:
        current_table = name
        settings["current_table"] = name
        save_settings(settings)
        success_message(f"Selected table: {name}!")
        return current_table
    except Exception as e:
        error_message(f"Failed to select table: {e}")
        return None


# [ METHOD ]: Describe a table schema
def describe_table_schema(table_name: str):
    global current_engine
    
    # ERROR: no database connection
    if not require_engine() or current_engine is None:
        return []
    
    inspector = inspect(current_engine)
    columns = inspector.get_columns(table_name)
    
    display_center(f"[ '{table_name}' - Schema ]", 32)
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

    inspector = inspect(current_engine)
    columns = inspector.get_columns(table_name)

    # ERROR: only 1 column in the table
    if len(columns) <= 1:
        error_message(f"Cannot remove column '{col_name}'. Table '{table_name}' must have at least one column.")
        return

    # ERROR: column does not exist
    col_names = [col["name"] for col in columns]
    if col_name not in col_names:
        error_message(f"Column '{col_name}' does not exist in table '{table_name}'.")
        return

    # Drop column if safe
    with current_engine.connect() as conn:
        conn.execute(text(f"ALTER TABLE {table_name} DROP COLUMN {col_name};"))
    success_message(f"Column '{col_name}' removed from '{table_name}'.")

# [ METHOD ]: Rename a table
def rename_table(new_name: str):
    global current_engine, current_table, settings

    if not require_engine() or current_engine is None:
        return None

    old_name = current_table

    try:
        with current_engine.connect() as conn:
            conn.execute(text(f"ALTER TABLE {old_name} RENAME TO {new_name};"))

        # Update runtime state
        current_table = new_name

        # Update persistent state
        settings["current_table"] = new_name
        save_settings(settings)

        success_message(f"Table renamed from '{old_name}' to '{new_name}'.")

        # Force reload table names to avoid stale inspector state
        inspector = inspect(current_engine)
        inspector.get_table_names()

        return current_table

    except Exception as e:
        error_message(f"Failed to rename table: {e}")
        return None


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


''' METHODS: Schema Tools '''
# [ METHOD ]: Generate SQLAlchemy model class from a table
def generate_model_class(table_name: str):
    if not require_engine() or current_engine is None:
        return None
    
    try:
        inspector = inspect(current_engine)
        columns = inspector.get_columns(table_name)

        class_name = table_name.capitalize()
        success_message(f"\nGenerated model for table '{table_name}':\n")

        code = f"class {class_name}(Base):\n"
        code += f"    __tablename__ = '{table_name}'\n\n"
        for col in columns:
            col_name = col['name']
            col_type = col['type']
            code += f"    {col_name} = Column({col_type})\n"

        print(code)
        return code

    except Exception as e:
        error_message(f"Failed to generate model: {e}")
        return None

# [ METHOD ]: View generated model class code
def view_model_class_code(table_name: str):
    global current_engine

    if not require_engine() or current_engine is None:
        return None
    
    try:
        inspector = inspect(current_engine)
        columns = inspector.get_columns(table_name)

        type_map = {
            "INTEGER": "Integer",
            "VARCHAR": "String",
            "TEXT": "String",
            "FLOAT": "Float",
            "BOOLEAN": "Boolean",
            "TIMESTAMP": "DateTime",
        }

        # start building the class code
        class_name = ''.join(word.capitalize() for word in table_name.split('_'))
        code = f"class {class_name}(Base):\n"
        code += f"    __tablename__ = '{table_name}'\n\n"

        for col in columns:
            col_name = col['name']
            col_type = str(col['type']).upper().split("(")[0]  # e.g. "VARCHAR(255)" → "VARCHAR"
            sqlalchemy_type = type_map.get(col_type, "String")
            code += f"    {col_name} = Column({sqlalchemy_type})\n"

        success_message(f"Generated model class for table '{table_name}':\n")
        print(code)

        return code

    except Exception as e:
        error_message(f"Failed to view model class: {e}")
        return None

# [ METHOD ]: Sync model to table
def sync_model_to_table(table_name: str):
    if not require_engine() or current_engine is None:
        return None
    
    try:
        metadata = MetaData()
        metadata.reflect(bind=current_engine)

        if table_name not in metadata.tables:
            info_message(f"Table '{table_name}' does not exist. Creating...")
            
            # Dynamically build a table with one column if needed
            Table(table_name, Base.metadata, Column("id", Integer, primary_key=True))
            Base.metadata.create_all(current_engine, tables=[Base.metadata.tables[table_name]])

            success_message(f"Table '{table_name}' created successfully.")
        else:
            info_message(f"Table '{table_name}' already exists, nothing to sync.")

    except Exception as e:
        error_message(f"Failed to sync table: {e}")


''' METHODS: Utilities '''
# [ METHOD ]: Execute custom SQL
def run_raw_sql_queries(sql: str):
    global current_engine, settings

    if not require_engine() or current_engine is None:
        return None
    
    try:
        with current_engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = result.fetchall() if result.returns_rows else []

        # Save to query log
        settings.setdefault("query_log", []).append(sql)
        save_settings(settings)

        success_message("Query executed successfully.")
        if rows:
            for row in rows:
                print(row)

    except Exception as e:
        error_message(f"Failed to execute query: {e}")

# [ METHOD ]: Export to CSV/JSON
def export_table_data(table_name: str, fmt: str, file_path: str):
    global current_engine

    if not require_engine() or current_engine is None:
        return None
    
    try:
        df = pd.read_sql_table(table_name, current_engine)
        if fmt == "csv":
            df.to_csv(file_path, index=False)
        elif fmt == "json":
            df.to_json(file_path, orient="records", indent=2)
        else:
            error_message("Invalid format. Must be 'csv' or 'json'.")
            return
        success_message(f"Exported table '{table_name}' to {file_path}")
    except Exception as e:
        error_message(f"Failed to export: {e}")

# [ METHOD ]: Import from CSV/JSON
def import_table_data(table_name: str, file_path: str):
    global current_engine

    if not require_engine() or current_engine is None:
        return None
    
    if not os.path.exists(file_path):
        error_message("File does not exist.")
        return

    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".csv":
            df = pd.read_csv(file_path)
        elif ext == ".json":
            df = pd.read_json(file_path)
        else:
            error_message("Unsupported format. Use CSV or JSON.")
            return

        df.to_sql(table_name, current_engine, if_exists="append", index=False)
        success_message(f"Imported {len(df)} row(s) into '{table_name}'")

    except Exception as e:
        error_message(f"Failed to import: {e}")

# [ METHOD ]: Search a string in all text-like columns across tables
def search_across_tables(keyword: str):
    global current_engine
    found = False

    if not require_engine() or current_engine is None:
        return None
    
    try:
        inspector = inspect(current_engine)
        tables = inspector.get_table_names()

        for table in tables:
            columns = inspector.get_columns(table)
            text_cols = [c["name"] for c in columns if "CHAR" in str(c["type"]).upper() or "TEXT" in str(c["type"]).upper()]

            for col in text_cols:
                sql = text(f"SELECT * FROM {table} WHERE {col} LIKE :kw")
                with current_engine.connect() as conn:
                    result = conn.execute(sql, {"kw": f"%{keyword}%"})
                    rows = result.fetchall()
                    if rows:
                        found = True
                        success_message(f"Matches in {table}.{col}:")
                        for row in rows:
                            print(row)

        if not found:
            info_message(f"No matches found for '{keyword}'.")

    except Exception as e:
        error_message(f"Search failed: {e}")

# [ METHOD ]: View query history (session + persistent log)
def show_recent_queries():
    logs = settings.get("query_log", [])
    if not logs:
        info_message("No queries logged yet.")
    else:
        for i, q in enumerate(logs[-10:], start=1):
            print(f"{i}. {q}")


''' METHODS: Settings '''
# [ METHOD ]: Configure default DB connection
def configure_default_database_connection():
    global current_engine, current_db_url

    db_url = get_str("Enter database URL (e.g., sqlite:///mydb.db)", ["required"])
    if not db_url:
        info_message("Configuration cancelled.")
        return

    try:
        engine = create_engine(db_url)
        # test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        current_engine = engine
        current_db_url = db_url
        success_message(f"Default DB connection set: {db_url}")
    except SQLAlchemyError as e:
        error_message(f"Failed to connect: {e}")

# [ METHOD ]: Manage database connections
def manage_database_connections():
    global db_connections

    while True:
        print("\nAvailable connections:")
        if not db_connections:
            print("  (none)")
        else:
            for name, url in db_connections.items():
                print(f"  {name} → {url}")

        print("\nOptions:")
        print("  1. Add connection")
        print("  2. Remove connection")
        print("  3. Select connection")
        print("  4. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            name = get_str("Connection name", ["required"])
            url = get_str("Connection URL", ["required"])
            db_connections[name] = url
            success_message(f"Added connection '{name}'.")

        elif choice == "2":
            name = get_str("Connection name to remove", ["required"])
            if name in db_connections:
                del db_connections[name]
                success_message(f"Removed connection '{name}'.")
            else:
                error_message("No such connection.")

        elif choice == "3":
            name = get_str("Connection name to select", ["required"])
            if name in db_connections:
                try:
                    engine = create_engine(db_connections[name])
                    with engine.connect() as conn:
                        conn.execute(text("SELECT 1"))
                    globals()["current_engine"] = engine
                    globals()["current_db_url"] = db_connections[name]
                    success_message(f"Switched to connection '{name}'.")
                except SQLAlchemyError as e:
                    error_message(f"Connection failed: {e}")
            else:
                error_message("No such connection.")

        elif choice == "4":
            break
        else:
            error_message("Invalid choice.")

# [ METHOD ]: Set naming conventions
def set_naming_conventions_for_models():
    global naming_conventions

    print("\nCurrent conventions:")
    for k, v in naming_conventions.items():
        print(f"  {k.capitalize()}: {v}")

    print("\nOptions: PascalCase | snake_case | camelCase")
    class_conv = get_str("Class naming convention", [])
    table_conv = get_str("Table naming convention", [])
    column_conv = get_str("Column naming convention", [])

    if class_conv:
        naming_conventions["class"] = class_conv
    if table_conv:
        naming_conventions["table"] = table_conv
    if column_conv:
        naming_conventions["column"] = column_conv

    success_message("Naming conventions updated.")

# [ METHOD ]: Configure logging
def configure_logging():
    global logging_config

    enabled = get_str("Enable logging? (yes/no)", ["required"]).lower()
    if enabled not in ["yes", "no"]:
        error_message("Invalid choice.")
        return

    logging_config["enabled"] = (enabled == "yes")

    if logging_config["enabled"]:
        level = get_str("Logging level (DEBUG, INFO, WARNING, ERROR)", ["required"])
        log_file = get_str("Log file path (leave blank for console only)", [])

        logging_config["level"] = level.upper()
        logging_config["file"] = log_file if log_file else None

        success_message(f"Logging enabled (Level: {logging_config['level']}, File: {logging_config['file'] or 'stdout'})")
    else:
        success_message("Logging disabled.")