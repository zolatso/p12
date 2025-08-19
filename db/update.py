from .models import Role, User, Client
from . import get_db_session

def update_user(user, field, new_value):
    with get_db_session() as db:
        # For changing the role, we need to extract the correct id
        if field == "role":
            field = "role_id"
            value = db.query(Role.id).filter(Role.name == new_value).scalar()
        else:
            value = new_value

        db.query(User).filter_by(name=user).update({field: value})

def update_client(client, field, new_value):
    with get_db_session() as db:
        # For changing the user, we need to extract the correct id
        if field == "user":
            field = "user_id"
            value = db.query(User.id).filter(User.name == new_value).scalar()
        else:
            value = new_value

        db.query(Client).filter_by(fullname=client).update({field: value})