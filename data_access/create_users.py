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

with session_maker() as session:
    # session.query(User).delete()
    session.add_all(users)
    session.commit()
