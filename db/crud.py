from .__init__ import Session
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError
from .models import Role, User


@contextmanager
def get_db_session():
    db = Session()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        print(f"An error occurred during commit: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def create_user(db_session, username, email, plain_password, role_name):
    role = db_session.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise ValueError(f"Role '{role_name}' not found.")
    user = User(name=username, email=email, role_obj=role)
    user.set_password(plain_password)
    db_session.add(user)




