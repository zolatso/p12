from datetime import datetime

from .models import Role, User, Client, Contract, Event
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
    
def get_commercial_usernames():
    with get_db_session(read_only=True) as db:
        return [n for (n, ) in db.query(User.name).join(User.role_obj).filter(Role.name == "commercial")]
    
def get_clients():
    with get_db_session(read_only=True) as db:
        return [n for (n, ) in db.query(Client.fullname).all()]
    
def get_clients_represented_by_commercial(name):
    """Returns only the clients represented by the commercial passed as an arg"""
    with get_db_session(read_only=True) as db:
        clients = db.query(Client.fullname).join(User.clients).filter(User.name == name).all()
        return clients

def get_specific_user(name):
    with get_db_session(read_only=True) as db:
        object = db.query(User).filter_by(name=name).first()
        user = {
            "name" : object.name,
            "email" : object.email,
            "role" : object.role_obj.name.value
        }
        return user
    
def get_specific_client(name):
    with get_db_session(read_only=True) as db:
        client = db.query(Client).filter_by(fullname=name).first()
        client_dict = {
            "name" : client.fullname,
            "email" : client.email,
            "phone" : client.phone,
            "business_name" : client.business_name,
            "created_at" : client.created_at,
            "updated_at" : client.updated_at,
            "user" : client.user.name,
            "contracts" : client.contracts
        }
        return client_dict
    
def get_contracts_for_client(name):
    with get_db_session(read_only=True) as db:
        contracts = db.query(Contract).join(Client.contracts).filter(Client.fullname==name)
        contract_dicts = []
        # Cycle through each returned contract for the client and create a dictionary
        for contract in contracts:
            # We also include the commercial associé avec ce contract (via le client)
            associated_commercial = db.query(User.name).join(Client.user).filter(Client.fullname==name).scalar()
            contract_dict = {
                "id" : contract.id,
                "total_amount" : contract.total_amount,
                "amount_remaining" : contract.amount_remaining,
                "associated_commercial" : associated_commercial,
                "created_at" : contract.created_at,
                "is_signed" : contract.is_signed,
            }
            # Add the event associated with the contract if it exists
            event = db.query(Event.name).filter_by(contract_id=contract.id).first()
            if event is not None:
                contract_dict["event"] = event
            contract_dicts.append(contract_dict)
        
        return contract_dicts


