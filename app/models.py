## Database Models for SQLite

from dataclasses import dataclass
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

@dataclass
class User(Base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(80), unique = True, nullable = False)
    password_hash: str = Column(String(200), nullable = False)

    