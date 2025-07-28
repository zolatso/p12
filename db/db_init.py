from .__init__ import engine, get_db_session
from .models import UserRoleEnum, Role, User, Base
from .crud import create_user


def add_roles_users_permissions():
    # Add roles if they don't exist
    with get_db_session() as db:
        if db.query(Role).first() is None:
            db.add(Role(name=UserRoleEnum.COMMERCIAL))
            db.add(Role(name=UserRoleEnum.GESTION))
            db.add(Role(name=UserRoleEnum.SUPPORT))

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
            
    # Add permissions if table is empty
            
def create_tables():
    Base.metadata.create_all(engine)