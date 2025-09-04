from datetime import datetime, date

from .models import Role, User, Client, Contract, Event
from . import get_db_session


def create_user(name, email, plain_password, role_name):
    """
    Prend un nom, une adresse e-mail, un mot de passe non haché et un nom de rôle.
    Récupère l'ID associé au nom du rôle dans la table Role.
    Utilise la méthode User pour hacher le mot de passe.
    Ajoute tout à la base de données.
    """
    with get_db_session() as db:
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            raise ValueError(f"Role '{role_name}' not found.")
        user = User(name=name, email=email, role_obj=role)
        user.set_password(plain_password)
        db.add(user)


def create_client(user, fullname, email, phone, business_name, created_at):
    """
    Prend les variables fournies par l'utilisateur, les convertit aux formats requis
    pour le modèle Client, puis les ajoute à la base de données.
    Cela inclut le champ relationnel où l'ID de l'utilisateur/employé est inclus dans le tableau.
    """
    with get_db_session() as db:
        user_id = db.query(User.id).filter_by(name=user).scalar()
        client_kwargs = {
            "fullname": fullname,
            "email": email,
            "phone": phone,
            "business_name": business_name,
            "created_at": datetime.strptime(created_at, "%d/%m/%Y"),
            "updated_at": datetime.now(),
            "user_id": user_id,
        }

        new_client = Client(**client_kwargs)
        db.add(new_client)


def create_contract(client, amount, amount_remaining, created_at, is_signed):
    """
    Gère les variables saisies par l'utilisateur, s'assure qu'elles sont au format
    correct pour être ajoutées au modèle Contract.
    Les ajoute à la base de données.
    """
    with get_db_session() as db:
        # Get client id from name
        client_id = db.query(Client.id).filter_by(fullname=client).scalar()
        # Convert is_signed to boolean
        is_signed = True if is_signed == "Oui" else False
        new_contract = Contract(
            client_id=client_id,
            total_amount=amount,
            amount_remaining=amount_remaining,
            created_at=datetime.strptime(created_at, "%d/%m/%Y"),
            is_signed=is_signed,
        )
        db.add(new_contract)


def create_event(
    contract_id,
    event_name,
    event_contact,
    event_start,
    event_end,
    location,
    attendees,
    notes,
):
    """
    Gérer et traiter les entrées nécessaires à la création d'un nouvel événement.
    Ajouter à la base de données.
    """
    with get_db_session() as db:
        new_event = Event(
            contract_id=contract_id,
            name=event_name,
            client_contact=event_contact,
            event_start=datetime.strptime(event_start, "%d/%m/%Y %H:%M"),
            event_end=datetime.strptime(event_end, "%d/%m/%Y %H:%M"),
            location=location,
            attendees=attendees,
            notes=notes,
        )
        db.add(new_event)
