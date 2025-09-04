from . import engine, get_db_session
from .models import (
    UserRoleEnum,
    Role,
    User,
    Base,
    Permission,
    role_permission_association,
)


def add_roles_users_permissions():
    with get_db_session() as db:
        # Add roles, permissions, and their relations if they don't exist
        if db.query(Role).first() is None:
            commercial = Role(name=UserRoleEnum.COMMERCIAL)
            gestion = Role(name=UserRoleEnum.GESTION)
            support = Role(name=UserRoleEnum.SUPPORT)
            db.add_all([commercial, gestion, support])

        if db.query(Permission).first() is None:
            can_read = Permission(name="read a resource", description="anyone")
            create_client = Permission(
                name="create client", description="equipe commercial"
            )
            update_client = Permission(
                name="update client", description="equipe commercial"
            )
            update_contract = Permission(
                name="update contract", description="equipes commercial et gestion"
            )
            create_event = Permission(
                name="create event", description="equipe commercial"
            )
            update_event = Permission(name="update event", description="equipe support")
            create_contract = Permission(
                name="create contract", description="equipe gestion"
            )
            update_user = Permission(name="update user", description="equipe gestion")
            add_new_user = Permission(name="create user", description="equipe gestion")
            delete_user = Permission(name="delete user", description="equipe gestion")
            db.add_all(
                [
                    can_read,
                    create_client,
                    update_client,
                    update_contract,
                    create_event,
                    update_event,
                    create_contract,
                    update_user,
                    add_new_user,
                    delete_user,
                ]
            )

        if db.query(role_permission_association).first() is None:
            commercial.permissions.extend(
                [can_read, create_client, update_client, update_contract, create_event]
            )
            gestion.permissions.extend(
                [
                    can_read,
                    create_contract,
                    update_event,
                    update_user,
                    add_new_user,
                    delete_user,
                    update_contract,
                ]
            )
            support.permissions.extend([can_read, update_event])

        # Add users if they don't exist
        if db.query(User).first() is None:
            create_user_init(
                db,
                "Tom Saunders",
                "tomsaunders1@gmail.com",
                "OpenClassrooms2025!!!",
                UserRoleEnum.COMMERCIAL,
            )
            create_user_init(
                db,
                "Tom Smith",
                "tomsmith1@gmail.com",
                "OpenClassrooms2025!!!",
                UserRoleEnum.GESTION,
            )
            create_user_init(
                db,
                "John Smith",
                "johnsmith1@gmail.com",
                "OpenClassrooms2025!!!",
                UserRoleEnum.SUPPORT,
            )


def create_tables():
    Base.metadata.create_all(engine)


def create_user_init(db_session, username, email, plain_password, role_name):
    role = db_session.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise ValueError(f"Role '{role_name}' not found.")
    user = User(name=username, email=email, role_obj=role)
    user.set_password(plain_password)
    db_session.add(user)


def recreate_initial_db():
    create_tables()
    add_roles_users_permissions()
