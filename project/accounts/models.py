from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

metadata = MetaData()


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String)
    password = Column(String, nullable=False)
