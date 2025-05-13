# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base               # importa o declarative_base() do seu models

import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependência FastAPI — abre uma sessão e garante .close()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# (opcional) criar as tabelas automaticamente em dev:
def create_tables():
    Base.metadata.create_all(bind=engine)
