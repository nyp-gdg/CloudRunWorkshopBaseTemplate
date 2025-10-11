## Initialize the DB
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

DB_URL = os.getenv("DB_URL", "sqlite:////tmp/workshop.db")
## For future integrations into CloudSQL ^

engine = create_engine(DB_URL, future = True)
SessionLocal = sessionmaker(bind = engine, autoflush = False, autocommit = False, future = True)

def init_db():
    Base.metadata.create_all(bind = engine)