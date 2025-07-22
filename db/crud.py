from .__init__ import Session
from contextlib import contextmanager


@contextmanager
def get_db_session():
    db = Session()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()



