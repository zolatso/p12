from datetime import datetime
from sqlalchemy import select

from .models import Role, User, Client, Contract, Event
from . import get_db_session
from auth.exc import AuthError


def get_user_details(email: str, password: str) -> dict:
    """Looks up a user, validates email/pw combo, returns details for JWT payload"""
    with get_db_session(read_only=True) as db:
        user = db.query(User).filter_by(email=email).first()
        if not user or not user.verify_password(password):
            raise ValueError("Email or password is incorrect")
        user_details = {
            "name": user.name,
            "role": user.role_obj.name.value,
            "permissions": [perm.name for perm in user.role_obj.permissions],
        }
        return user_details


def get_usernames():
    with get_db_session(read_only=True) as db:
        return [n for (n,) in db.query(User.name).all()]


def get_equipe_usernames(equipe):
    with get_db_session(read_only=True) as db:
        return [
            n
            for (n,) in db.query(User.name)
            .join(User.role_obj)
            .filter(Role.name == equipe)
        ]


def get_clients():
    with get_db_session(read_only=True) as db:
        return [n for (n,) in db.query(Client.fullname).all()]


def get_clients_represented_by_commercial(name):
    """Returns only the clients represented by the commercial passed as an arg"""
    with get_db_session(read_only=True) as db:
        clients = db.scalars(
            select(Client.fullname).join(User.clients).filter(User.name == name)
        )
        return clients


def get_specific_user(name):
    with get_db_session(read_only=True) as db:
        object = db.query(User).filter_by(name=name).first()
        user = {
            "name": object.name,
            "email": object.email,
            "role": object.role_obj.name.value,
        }
        return user


def get_specific_client(name):
    with get_db_session(read_only=True) as db:
        client = db.query(Client).filter_by(fullname=name).first()
        client_dict = {
            "name": client.fullname,
            "email": client.email,
            "phone": client.phone,
            "business_name": client.business_name,
            "created_at": client.created_at,
            "updated_at": client.updated_at,
            "user": client.user.name,
            "contracts": [
                f"Contrat crée le {contract.created_at}"
                for contract in client.contracts
            ],
        }
        return client_dict


def get_contracts_for_client(name):
    with get_db_session(read_only=True) as db:
        contracts = (
            db.query(Contract).join(Client.contracts).filter(Client.fullname == name)
        )
        contract_dicts = []
        # Cycle through each returned contract for the client and create a dictionary
        for contract in contracts:
            # We also include the commercial associé avec ce contract (via le client)
            associated_commercial = (
                db.query(User.name)
                .join(Client.user)
                .filter(Client.fullname == name)
                .scalar()
            )
            contract_dict = {
                "id": contract.id,
                "total_amount": contract.total_amount,
                "amount_remaining": contract.amount_remaining,
                "associated_commercial": associated_commercial,
                "created_at": contract.created_at,
                "is_signed": contract.is_signed,
            }
            # Add the event associated with the contract if it exists
            event = db.scalar(select(Event.name).filter_by(contract_id=contract.id))
            if event is not None:
                contract_dict["event"] = event
            contract_dicts.append(contract_dict)

        return contract_dicts


def signed_contracts_by_my_clients(name):
    with get_db_session(read_only=True) as db:
        client_ids = db.scalars(
            select(Client.id).join(User.clients).filter(User.name == name)
        )
        all_signed_contracts = []
        # Get the valid contracts add them to a list
        for client_id in client_ids:
            # This also needs to check that there is not already an event attached
            signed_contracts = (
                db.query(Contract).filter_by(client_id=client_id, is_signed=True).all()
            )
            # Construct dictionaries
            for contract in signed_contracts:
                # Only need these three fields for display and referencing
                contract_dict = {
                    "id": contract.id,
                    "total_amount": contract.total_amount,
                    "created_at": datetime.strftime(contract.created_at, "%d/%m/%Y"),
                }
                all_signed_contracts.append(contract_dict)

        return all_signed_contracts


def get_all_events():
    with get_db_session(read_only=True) as db:
        return db.scalars(select(Event.name))


def get_events_for_support(name):
    with get_db_session(read_only=True) as db:
        support_id = db.scalar(select(User.id).filter_by(name=name))
        events = db.scalars(select(Event.name).filter_by(support_id=support_id))
        return events


def get_all_support():
    with get_db_session(read_only=True) as db:
        support_role_id = db.scalar(select(Role.id).filter_by(name="support"))
        print(support_role_id)
        return [
            n for (n,) in db.query(User.name).filter_by(role_id=support_role_id).all()
        ]


def get_specific_event(name):
    # This function is used when a support team member wants to modify an event.
    # Hence, we only return the fields that they are able to modify.
    with get_db_session(read_only=True) as db:
        event = db.query(Event).filter_by(name=name).scalar()
        support = db.scalar(select(User).filter_by(id=event.support_id))
        event_dict = {
            "name": event.name,
            "client_contact": event.client_contact,
            "event_start": event.event_start,
            "event_end": event.event_end,
            "location": event.location,
            "attendees": event.attendees,
            "notes": event.notes,
        }
        if support:
            event_dict["support"] = support.name
        return event_dict
