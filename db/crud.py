from .models import Role, User
from .__init__ import get_db_session

def get_user(email : str, password : str) -> tuple[User | None, str | None]:
    with get_db_session(read_only=True) as db:
        user = db.query(User).filter_by(email=email).first()
        if not user:
            return None, "This user does not exist"
        if not user.verify_password(password):
            return None, "The password is incorrect"
        return user, None


def create_user(db_session, username, email, plain_password, role_name):
    role = db_session.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise ValueError(f"Role '{role_name}' not found.")
    user = User(name=username, email=email, role_obj=role)
    user.set_password(plain_password)
    db_session.add(user)




