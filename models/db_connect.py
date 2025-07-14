import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, ProgrammingError

db_password = os.environ.get("DB_PASSWORD")

if db_password is None:
    raise ValueError("DB_PASSWORD environment variable not set.")

# Example for MySQL
DATABASE_URL = f"mysql+pymysql://p12admin:{db_password}@localhost:3306/project12"
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        print("Successfully connected to the database!")
except OperationalError as e:
    print(f"Connection failed: {e}")
    print("Please check your database server status, host, port, and network connectivity.")
except ProgrammingError as e:
    print(f"Authentication or database error: {e}")
    print("Please check your username, password, and if the database exists.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")