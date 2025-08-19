from datetime import datetime

from .models import Role, User, Client
from . import get_db_session
from auth.exc import AuthError

def get_user_details(email : str, password : str) -> dict:
    """ Looks up a user, validates email/pw combo, returns details for JWT payload"""
    with get_db_session(read_only=True) as db:
        user = db.query(User).filter_by(email=email).first()
        if not user or not user.verify_password(password):
            raise AuthError("Email or password is incorrect")
        user_details = {
            "name" : user.name,
            "role" : user.role_obj.name.value,
            "permissions" : [perm.name for perm in user.role_obj.permissions],
        }
        return user_details
    
def get_usernames():
    with get_db_session(read_only=True) as db:
        return [n for (n, ) in db.query(User.name).all()]

def get_specific_user(name):
    with get_db_session(read_only=True) as db:
        object = db.query(User).filter_by(name=name).first()
        user = {
            "name" : object.name,
            "email" : object.email,
            "role" : object.role_obj.name.value
        }
        return user
    