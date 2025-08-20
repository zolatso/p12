from datetime import datetime

from .models import Role, User, Client, Contract
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

def update_contract(contract_id, field, new_value):
    with get_db_session() as db:
        # For changing the user, we need to extract the correct id
        if field == "created_at":
            value = datetime.strptime(new_value, "%d/%m/%Y"),
        elif field == "is_signed":
            value = True if new_value == "Oui" else False 
        else:
            # Otherwise we are modifying either total amount or amount outstanding
            value = int(new_value)

        db.query(Contract).filter_by(id=contract_id).update({field: value})