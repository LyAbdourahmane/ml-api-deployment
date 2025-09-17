# infra/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from infra.config import get_database_url

class Base(DeclarativeBase):
    pass

DATABASE_URL = get_database_url()

engine = create_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True,
    connect_args={
        "application_name": "emission_co2",          # ASCII only
        "options": "-c client_encoding=UTF8",  # force UTF-8 côté client
    },
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
