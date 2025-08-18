import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, ProgrammingError, SQLAlchemyError


def db_connect(root=False):
    db_password = os.environ.get("DB_ROOT_PASSWORD") if root else os.environ.get("DB_PASSWORD")
    db_user = "root" if root else "p12admin"

    if db_password is None:
        raise ValueError(f"Database password environment variable not set. You are trying to login as {db_user}.")

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

engine = db_connect(root=True)

Session = sessionmaker(bind=engine)

@contextmanager
def get_db_session(read_only: bool = False):
    db = Session()
    try:
        yield db
        if not read_only:
            db.commit()
    except SQLAlchemyError as e:
        print(f"An error occurred during commit: {e}")
        db.rollback()
        raise
    finally:
        db.close()

