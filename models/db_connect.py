import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, ProgrammingError

def db_connect(root):
    db_password = os.environ.get("DB_ROOT_PASSWORD") if root else os.environ.get("DB_PASSWORD")
    db_user = "root" if root else "p12admin"

    if db_password is None:
        raise ValueError("DB_PASSWORD environment variable not set.")

    # Example for MySQL
    DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@localhost:3306/project12"
    engine = create_engine(DATABASE_URL)

    try:
        with engine.connect() as connection:
            return engine
    except OperationalError as e:
        return f"Connection failed: {e}"
    except ProgrammingError as e:
        return f"Authentication or database error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"