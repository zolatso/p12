from datetime import datetime

from .models import Role, User, Client
from . import get_db_session
    
def create_user(name, email, plain_password, role_name):
    with get_db_session() as db:
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            raise ValueError(f"Role '{role_name}' not found.")
        user = User(name=name, email=email, role_obj=role)
        user.set_password(plain_password)
        db.add(user)

def create_client(user, fullname, email, phone, business_name, created_at):
    with get_db_session() as db:
        user_id = db.query(User.id).filter_by(name=user).scalar()
        client_kwargs = {
            "fullname": fullname,
            "email": email,
            "phone": phone,
            "business_name": business_name,
            "created_at": datetime.strptime(created_at, "%d/%m/%Y"),
            "updated_at": datetime.now(),
            "user_id": user_id
        }

        new_client = Client(**client_kwargs)
        db.add(new_client)

def create_user_init(db_session, username, email, plain_password, role_name):
    role = db_session.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise ValueError(f"Role '{role_name}' not found.")
    user = User(name=username, email=email, role_obj=role)
    user.set_password(plain_password)
    db_session.add(user)

