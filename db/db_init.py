from .__init__ import engine, get_db_session
from .models import UserRoleEnum, Role, User, Base, Permission
from .crud import create_user


def add_roles_users_permissions():
    # Add roles if they don't exist
    with get_db_session() as db:
        if db.query(Role).first() is None:
            commercial = db.add(Role(name=UserRoleEnum.COMMERCIAL))
            gestion = db.add(Role(name=UserRoleEnum.GESTION))
            support = db.add(Role(name=UserRoleEnum.SUPPORT))

        if db.query(Permission).first() is None:
            create_client = db.add(Permission(name="create client", description="equipe commercial"))
            update_client = db.add(Permission(name="update client", description="only the commercial who is responsible for the client"))
            create_contract = db.add(Permission(name="create contract", description="equipe gestion"))
            updated_contract = db.add(Permission(name="update contract", description="only those contracts that commercial is responsible for"))
            create_event = db.add(Permission(name="create event", description="equipe commercial"))
            read = db.add(Permission(name="read a resouce", description="anyone"))
            add_support_to_event = db.add(Permission(name="add support to event", description="equipe gestion"))
            update_user = db.add(Permission(name="update user", description="equipe gestion"))
            add_new_user = db.add(Permission(name="create user", description="equipe gestion"))
            delete_user = db.add(Permission(name="delete user", description="equipe gestion"))
        
    # Add test users if table is empty
    with get_db_session() as db:
        if db.query(User).first() is None:
            create_user(
                db, 
                "Tom Saunders", 
                "tomsaunders1@gmail.com", 
                "OpenClassrooms2025!!!", 
                UserRoleEnum.COMMERCIAL
                )
            create_user(
                db, 
                "Tom Smith", 
                "tomsmith1@gmail.com", 
                "OpenClassrooms2025!!!", 
                UserRoleEnum.GESTION
                )
            create_user(
                db, 
                "John Smith", 
                "johnsmith1@gmail.com", 
                "OpenClassrooms2025!!!", 
                UserRoleEnum.SUPPORT
                )
            
    # Create permissions to roles relationships
            
def create_tables():
    Base.metadata.create_all(engine)