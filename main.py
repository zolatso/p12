from db.db_init import add_roles_users_permissions, create_tables
from db import get_db_session
from db.models import User

def main():
    add_roles_users_permissions()

if __name__ == "__main__":
    main()

