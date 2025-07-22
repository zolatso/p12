from models.models import Base, Permission, Role, User, Contract, Client, Event, UserRoleEnum
from sqlalchemy.orm import sessionmaker

def create_test_users_roles_permissions(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create Permissions
    view_permission = Permission(name="view_content", description="Can view any content")
    edit_permission = Permission(name="edit_content", description="Can edit any content")
    admin_permission = Permission(name="manage_users", description="Can manage user accounts")

    session.add_all([view_permission, edit_permission, admin_permission])
    session.commit()

    # Create Roles and assign Permissions
    admin_role = Role(name=UserRoleEnum.COMMERCIAL.value, description="Administrator role")
    admin_role.permissions.append(view_permission)
    admin_role.permissions.append(edit_permission)
    admin_role.permissions.append(admin_permission)

    editor_role = Role(name=UserRoleEnum.GESTION.value, description="Editor role")
    editor_role.permissions.append(view_permission)
    editor_role.permissions.append(edit_permission)

    viewer_role = Role(name=UserRoleEnum.SUPPORT.value, description="Viewer role")
    viewer_role.permissions.append(view_permission)

    session.add_all([admin_role, editor_role, viewer_role])
    session.commit()

    # Create Users and assign Roles
    # Now include a plain text password to be hashed
    alice = User(username="alice", role_obj=admin_role)
    alice.set_password("admin_secure_password") # Hash the password
    bob = User(username="bob", role_obj=editor_role)
    bob.set_password("editor_password123")
    charlie = User(username="charlie", role_obj=viewer_role)
    charlie.set_password("viewer_pass")

    session.add_all([alice, bob, charlie])
    session.commit()

    # Query and inspect
    print("\n--- Users and their Roles/Permissions ---")
    all_users = session.query(User).all()
    for user in all_users:
        print(f"User: {user.username}, Role: {user.role_obj.name}")
        print(f"  Permissions:")
        for perm in user.role_obj.permissions:
            print(f"    - {perm.name}")

    # Verify passwords
    print("\n--- Password Verification ---")
    user_alice = session.query(User).filter_by(username="alice").first()
    if user_alice:
        print(f"Verifying Alice's password: '{user_alice.verify_password('admin_secure_password')}' (Should be True)")
        print(f"Verifying Alice's wrong password: '{user_alice.verify_password('wrong_password')}' (Should be False)")

    user_bob = session.query(User).filter_by(username="bob").first()
    if user_bob:
        print(f"Verifying Bob's password: '{user_bob.verify_password('editor_password123')}' (Should be True)")

    session.close()

def create_tables(engine):
    Base.metadata.create_all(engine)