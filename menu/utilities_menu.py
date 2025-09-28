# Imports: SQLAlchemy
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

# Imports: Utilities
from utils.console_utils import *
from utils.input_utils import *
from utils.settings import *

# Imports: Database Manager
from db_utils.database_manager import *

# [ UI ]: Execute custom SQL
def run_raw_sql_queries_menu():
    global current_engine

    display_header("ZenDB", "Run Raw SQL Query", width=32, symbol="=")

    if not require_engine():
        press_to_continue()
        return

    sql = get_str("SQL query", ["required"])
    if not sql:
        info_message("Query cancelled.")
        press_to_continue()
        return

    run_raw_sql_queries(sql)
    press_to_continue()

# [ UI ]: Export to CSV/JSON
def export_table_data_menu():
    global current_engine

    display_header("ZenDB", "Export Table Data", width=32, symbol="=")

    if not require_engine():
        press_to_continue()
        return

    table_name = get_str("table name", ['required'])
    fmt = get_str("format (csv/json)", ['required']).lower()
    file_path = get_str("output file path", ['required'])

    export_table_data(table_name, fmt, file_path)
    press_to_continue()

# [ UI ]: Import from CSV/JSON
def import_table_data_menu():
    global current_engine

    display_header("ZenDB", "Import Table Data", width=32, symbol="=")

    if not require_engine():
        press_to_continue()
        return

    table_name = get_str("table name", ['required'])
    file_path = get_str("file path (CSV/JSON)", ['required'])

    import_table_data(table_name, file_path)
    press_to_continue()


# [ UI ]: Search a string in all text-like columns across tables
def search_across_tables_menu():
    global current_engine

    display_header("ZenDB", "Search Across Tables", width=32, symbol="=")

    if not require_engine():
        press_to_continue()
        return

    keyword = get_str("search keyword", ['required'])
    search_across_tables(keyword)
    press_to_continue()

# [ UI ]: View query history (session + persistent log)
def show_recent_queries_menu():
    display_header("ZenDB", "Recent Queries", width=32, symbol="=")
    show_recent_queries()
    press_to_continue()