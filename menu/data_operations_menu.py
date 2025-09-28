# Imports: SQLAlchemy
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

# Imports: Utilities
from utils.console_utils import *
from utils.input_utils import *
from utils.settings import *

# Imports: Database Manager
from db_utils.database_manager import *

''' UIS: Data Operations '''

# [ UI ]: Insert rows into current table
def insert_rows_menu():
    global current_engine, current_table

    display_header("ZenDB", "Insert Rows", width=30, symbol="=")

    # ERROR: No database or table selected
    if not current_table:
        error_message("No table selected.")
        press_to_continue()
        return

    inspector = inspect(current_engine)
    columns = inspector.get_columns(current_table)

    # ERROR: No columns
    if not columns:
        error_message("Table has no columns.")
        press_to_continue()
        return

    # ask user how many rows to input
    while True:
        row_count_str = get_str("# of row/s", ['required'])

        # just exit if Enter is pressed
        if not row_count_str:
            info_message("Row insertion cancelled.")
            press_to_continue()
            return

        # unselect table if explicitly typed "none"
        if row_count_str.lower() == "none":
            select_table("")  # disconnect/unselect
            press_to_continue()
            return
        
        try:
            num_of_rows = int(row_count_str)  # convert to int
            if num_of_rows <= 0:
                raise ValueError
            break
        except ValueError:
            error_message("Not a valid positive integer.")
            continue

    inserted = 0
    try:
        with current_engine.begin() as conn:
            for i in range(num_of_rows):
                print(f"\n--- Row {i+1} of {num_of_rows} ---")
                values = {}

                # collect values for each column
                for col in columns:
                    col_name = col["name"]
                    col_type = col["type"]

                    val = input(f"Enter value for '{col_name}' ({col_type}): ").strip()
                    if val == "":
                        val = None
                    values[col_name] = val

                # insert row
                cols = ", ".join(values.keys())
                placeholders = ", ".join([f":{k}" for k in values.keys()])
                query = text(f"INSERT INTO {current_table} ({cols}) VALUES ({placeholders})")
                conn.execute(query, values)
                inserted += 1

        success_message(f"\n{inserted} row(s) inserted successfully!")
    except Exception as e:
        error_message(f"Failed to insert rows: {e}")

    press_to_continue()


# [ UI ]: Display all rows in selected table
def view_all_rows_menu():
    global current_engine, current_table

    display_header("ZenDB", "View All Rows", width=30, symbol="=")

    if not require_engine() or not current_table:
        error_message("No table selected.")
        press_to_continue()
        return

    try:
        with current_engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {current_table}"))
            rows = result.fetchall()

        if not rows:
            info_message("No rows found.")
        else:
            for row in rows:
                print(row)

    except Exception as e:
        error_message(f"Failed to fetch rows: {e}")

    press_to_continue()


# [ UI ]: Display filtered rows
def view_rows_with_filter_menu():
    global current_engine, current_table

    display_header("ZenDB", "View Rows with Filter", width=30, symbol="=")

    if not require_engine() or not current_table:
        error_message("No table selected.")
        press_to_continue()
        return

    condition = input("Enter SQL WHERE condition (e.g., id = 1): ").strip()
    if not condition:
        info_message("Filter cancelled.")
        press_to_continue()
        return

    try:
        with current_engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {current_table} WHERE {condition}"))
            rows = result.fetchall()

        if not rows:
            info_message("No matching rows found.")
        else:
            for row in rows:
                print(row)

    except Exception as e:
        error_message(f"Failed to fetch rows: {e}")

    press_to_continue()


# [ UI ]: Update rows in selected table
def update_rows_menu():
    global current_engine, current_table

    display_header("ZenDB", "Update Rows", width=30, symbol="=")

    if not require_engine() or not current_table:
        error_message("No table selected.")
        press_to_continue()
        return

    set_clause = input("Enter SET clause (e.g., name = 'John'): ").strip()
    condition = input("Enter WHERE condition (leave blank to update all): ").strip()

    if not set_clause:
        info_message("Update cancelled.")
        press_to_continue()
        return

    query = f"UPDATE {current_table} SET {set_clause}"
    if condition:
        query += f" WHERE {condition}"

    try:
        with current_engine.begin() as conn:
            conn.execute(text(query))
        success_message("Rows updated successfully.")
    except Exception as e:
        error_message(f"Failed to update rows: {e}")

    press_to_continue()


# [ UI ]: Delete rows in selected table
def delete_rows_menu():
    global current_engine, current_table

    display_header("ZenDB", "Delete Rows", width=30, symbol="=")

    if not require_engine() or not current_table:
        error_message("No table selected.")
        press_to_continue()
        return

    condition = input("Enter WHERE condition (leave blank to delete ALL rows): ").strip()

    confirm = input(f"Are you sure? This will delete {'ALL rows' if not condition else 'matching rows'} [yes/no]: ").lower()
    if confirm != "yes":
        info_message("Delete cancelled.")
        press_to_continue()
        return

    query = f"DELETE FROM {current_table}"
    if condition:
        query += f" WHERE {condition}"

    try:
        with current_engine.begin() as conn:
            conn.execute(text(query))
        success_message("Rows deleted successfully.")
    except Exception as e:
        error_message(f"Failed to delete rows: {e}")

    press_to_continue()
