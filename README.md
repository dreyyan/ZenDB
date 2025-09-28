# ZenDB
_A Guided, Beginner-Friendly Console for PostgreSQL Management_

**ZenDB** is a simple, interactive console application designed to make PostgreSQL database management accessible for beginners. Built with SQLAlchemy, it provides a menu-driven interface for common database operations, including creating and managing databases, tables, and data. No prior SQL knowledge is required—ZenDB guides you through each step with clear prompts and error handling.

The primary purpose of ZenDB is to simplify database management for those learning PostgreSQL or needing a lightweight tool for quick database tasks. It supports essential features like schema generation, data import/export, and custom queries, making it ideal for educational and small-scale projects.

## FEATURES
✅ **Database Management** – List, create, drop, connect, and view details of databases  
✅ **Table Management** – Create, drop, select, describe, modify, and rename tables  
✅ **Data Operations** – Insert, view, filter, update, and delete rows with guided prompts  
✅ **Schema Tools** – Generate and view Python model classes, sync models to tables  
✅ **Utilities** – Run raw SQL, export/import data (CSV/JSON), search across tables, view query history  
✅ **Settings** – Configure database connections, naming conventions, and logging levels  

## FUTURE IMPLEMENTATIONS
🚀 Support for additional database types (MySQL, Oracle, etc.) with seamless switching  
🚀 Enhanced model generation with advanced data types and relationships  
🚀 Batch data operations for bulk imports/exports  
🚀 Interactive query builder for easier SQL construction  

## UPDATES
🔄 Improved error handling with detailed feedback for users  
🔄 Optimized database connection management for reliability  
🔄 Enhanced console UI with better formatting and navigation  

## PROJECT DETAILS
📌 **Author:** dreyyan  
📌 **Started:** 2025-09-26  
📌 **Finished:** 2025-09-28  

## TECH STACK
🛠️ **Framework:** SQLAlchemy, Alembic  
🛠️ **Languages:** Python  
🛠️ **Dependencies:** psycopg2-binary, sqlalchemy-utils, pandas  

## INSTALLATION
### Prerequisites
- Python 3.8 or higher
- PostgreSQL server installed and running (default connection: `postgres:qwpoeriuty123@localhost:5432`)
- Create a virtual environment (recommended):
  ```
  python -m venv venv
  source venv/bin/activate  # On Unix/Mac
  venv\Scripts\activate     # On Windows
  ```

### Install Dependencies
```
pip install sqlalchemy psycopg2-binary sqlalchemy-utils alembic pandas
```

#### Optional: Support for Other Databases
```
pip install pymysql     # MySQL
pip install pyodbc      # Microsoft SQL Server
pip install cx_Oracle   # Oracle
```

### Verify Installation
```
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
```

## USAGE
Start ZenDB:
```
python -m main
```
Navigate using numbered menu choices. Press Enter to confirm inputs or cancel.

### Example Workflow
1. **Connect to a Database**: Databases > Connect Database
2. **Create a Table**: Tables > Create New Table
3. **Insert Data**: Data Operations > Insert Row(s)
4. **Run a Query**: Utilities > Run Raw SQL Queries
5. **Export Data**: Utilities > Export Table Data

### Configuration
- Settings stored in `config.json` (auto-generated)
- Default database URL: `postgresql+psycopg2://postgres:qwpoeriuty123@localhost:5432`
- Customize in Settings > Manage Database Connections

## DEBUGGING
Enable detailed logging in Settings > Configure Logging. Run with:
```
python -m main
```

## PROJECT STRUCTURE
- `main.py`: Entry point
- `menu.py`: Main menu navigation
- `databases_menu.py`: Database operations UI
- `tables_menu.py`: Table operations UI
- `data_operations_menu.py`: Data manipulation UI
- `schema_tools_menu.py`: Schema generation and syncing
- `utilities_menu.py`: Additional tools
- `settings_menu.py`: Configuration options
- `db_utils/database_manager.py`: Core database functions
- `utils/`: Helper modules (console, input, settings)
- `settings.py`: Global settings and utilities

## CONTRIBUTING
Fork the repo, create a feature branch, and submit a pull request:
1. `git checkout -b feature/new-feature`
2. `git commit -m "Add new feature"`
3. `git push origin feature/new-feature`
4. Open a pull request

Report issues or suggest features via GitHub Issues.

## LICENSE
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
