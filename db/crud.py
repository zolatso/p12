from .models import Role, User
from .__init__ import get_db_session
from exc import InvalidPasswordError, UserDoesNotExistError

def get_user(email, password):
    with get_db_session(read_only=True) as db:
        user = db.query(User).filter_by(email=email).first()
        if not user:
            raise UserDoesNotExistError("User does not exist")
        if not user.verify_password(password):
            raise InvalidPasswordError("Invalid password")
        return user


def create_user(db_session, username, email, plain_password, role_name):
    role = db_session.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise ValueError(f"Role '{role_name}' not found.")
    user = User(name=username, email=email, role_obj=role)
    user.set_password(plain_password)
    db_session.add(user)




