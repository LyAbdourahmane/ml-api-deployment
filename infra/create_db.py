# infra/create_db.py
from __future__ import annotations
from urllib.parse import urlparse, urlunparse
from sqlalchemy import create_engine, text
from infra.config import get_database_url
from infra import models  # IMPORTANT: enregistre les tables
from infra.db import Base  # Base = DeclarativeBase

def ensure_database():
    url = get_database_url()
    parsed = urlparse(url)
    dbname = (parsed.path or "/").lstrip("/") or "postgres"

    # se connecte à la DB 'postgres' pour créer la base cible si besoin
    root_url = urlunparse(parsed._replace(path="/postgres"))
    root_engine = create_engine(
        root_url,
        future=True,
        isolation_level="AUTOCOMMIT",
        connect_args={
            "application_name": "ml_api_bootstrap",
            "options": "-c client_encoding=UTF8",
        },
    )
    with root_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname=:n"), {"n": dbname}
        ).first()
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{dbname}"'))
    root_engine.dispose()

def create_tables():
    from infra.db import engine  # engine pointant vers la base cible
    Base.metadata.create_all(bind=engine)

def main():
    ensure_database()
    create_tables()
    print("Base et tables prêtes.")

if __name__ == "__main__":
    main()
