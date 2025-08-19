from .models import Role, User, Client
from . import get_db_session

def update_user(user, field, new_value):
    with get_db_session() as db:
        # More complicated logic for changing the role
        if field == "role":
            field = "role_id"
            value = db.query(Role.id).filter(Role.name == new_value).scalar()
        else:
            value = new_value

        db.query(User).filter_by(name=user).update({field: value})

def update_client():
    pass