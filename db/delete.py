from .models import User
from . import get_db_session

def delete_specific_user(name):
    with get_db_session() as db:
        user = db.query(User).filter_by(name=name).first()
        db.delete(user) 