# ZenDB: 

### INSTALLATION
> Note: Make sure to create a Python virtual environment to avoid cluttering
#### 1. Install SQLAlchemy and required packages:
```powershell
pip install sqlalchemy psycopg2-binary sqlalchemy-utils alembic
```

#### 2. (Opt.) Install drivers for other databases
```powershell
pip install pymysql                # MySQL
pip install pyodbc                 # Microsoft SQL Server
pip install cx_Oracle              # Oracle
```

#### 3. Verify installation
```powershell
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
```