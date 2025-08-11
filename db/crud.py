from .models import Role, User
from .__init__ import get_db_session
from auth.exc import AuthError

def get_user_details(email : str, password : str) -> dict:
    """ Looks up a user, validates email/pw combo, returns details for JWT payload"""
    with get_db_session(read_only=True) as db:
        user = db.query(User).filter_by(email=email).first()
        if not user:
            raise AuthError("Email not exist")
        if not user.verify_password(password):
            raise AuthError("password is incorrect")
        user_details = {
            "name" : user.name,
            "role" : user.role_obj.name.value,
            "permissions" : [perm.name for perm in user.role_obj.permissions],
        }
        return user_details


def create_user(db_session, username, email, plain_password, role_name):
    role = db_session.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise ValueError(f"Role '{role_name}' not found.")
    user = User(name=username, email=email, role_obj=role)
    user.set_password(plain_password)
    db_session.add(user)




