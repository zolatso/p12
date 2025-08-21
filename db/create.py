from datetime import datetime

from .models import Role, User, Client, Contract, Event
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

def create_contract(client, amount, amount_remaining, created_at, is_signed):
    with get_db_session() as db:
        # Get client id from name
        client_id = db.query(Client.id).filter_by(fullname=client).scalar()
        # Convert is_signed to boolean
        is_signed = True if is_signed == "Oui" else False 
        new_contract = Contract(
            client_id=client_id,
            total_amount=amount,
            amount_remaining=amount_remaining,
            created_at=created_at,
            is_signed=is_signed
        )
        db.add(new_contract)

def create_event(contract_id, event_name, event_contact, event_start, event_end, location, attendees, notes):
    with get_db_session() as db:
        new_event = Event(
            contract_id=contract_id,
            name=event_name,
            client_contact=event_contact,
            event_start=datetime.strptime(event_start, "%d/%m/%Y"),
            event_end=datetime.strptime(event_end, "%d/%m/%Y"),
            location=location,
            attendees=attendees,
            notes=notes
        )
        db.add(new_event)