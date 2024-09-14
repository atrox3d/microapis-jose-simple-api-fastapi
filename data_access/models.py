import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

def generate_uuid() -> str:
    return str(uuid.uuid4())

class DictMixin:
    def dict(self):
        return {col:getattr(self, col) for col in self.__table__.columns.keys()}


class User(Base):
    __tablename__ = 'user'

    id = Column(String, primary_key=True, default=generate_uuid)
    created = Column(DateTime, nullable=False)
    email = Column(String, nullable=False)

    tasks = relationship('Task')

    def dict(self):
        return {col:getattr(self, col) for col in self.__table__.columns.keys()}


class Task(Base):
    __tablename__ = 'task'

    id = Column(String, primary_key=True, default=generate_uuid)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)
    priority = Column(String, nullable=False)
    status = Column(String, nullable=False)
    task = Column(String, nullable=False)

    user_id = Column(String, ForeignKey('user.id'))

    def dict(self):
        return {col:getattr(self, col) for col in self.__table__.columns.keys()
                if col in 'id priority status task created'.split()}
