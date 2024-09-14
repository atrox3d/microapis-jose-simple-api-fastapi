from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User
from datetime import datetime, UTC

users = [
    User(created=datetime.now(UTC), email='haha@haha.com'),
    User(created=datetime.now(UTC), email='hoho@hoho.com'),
]
# create contex manager to get session
session_maker = sessionmaker(bind=create_engine('sqlite:///models.db'))

def delete_db_users():
    with session_maker() as session:
        session.query(User).delete()
        session.commit()

def create_db_users(users:list[User]):
    with session_maker() as session:
        session.add_all(users)
        session.commit()

def print_db_users():
    with session_maker() as session:
        dbusers = session.query(User).all()
        for user in dbusers:
            print(user.dict())

def create_users(users:list[User], *, delete:bool, print:bool=True):
    if delete:
        delete_db_users()
    
    create_db_users(users)

    if print:
        print_db_users()

if __name__ == "__main__":
    create_users(users, delete=True)