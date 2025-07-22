from db.db_connect import db_connect
from db.db_actions import create_tables

if __name__ == "__main__":
    
    engine = db_connect(root=True)

    create_tables(engine)


