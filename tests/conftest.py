# tests/conftest.py
import os
import sys
from pathlib import Path
import pytest

# 1) Ajouter la racine du repo au PYTHONPATH (avant tout import du projet)
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# 2) Environnement de test par défaut
os.environ.setdefault("ENV", "test")
os.environ.setdefault("AUTH_ENABLED", "false")

# 3) Charger .env.test si présent (sans écraser les env déjà définies par la CI)
try:
    from dotenv import load_dotenv  # python-dotenv
    env_test = ROOT / ".env.test"
    if env_test.exists():
        load_dotenv(env_test, override=False)
except Exception:
    pass

# 4) Créer le schéma DB avant toute session de tests (idempotent)
@pytest.fixture(scope="session", autouse=True)
def _ensure_schema():
    from infra.db import Base, engine  # import après avoir fixé sys.path
    Base.metadata.create_all(bind=engine)
    yield

# 5) Client FastAPI prêt avec DB initialisée
@pytest.fixture
def client(_ensure_schema):
    from fastapi.testclient import TestClient
    from app.main import app
    with TestClient(app) as c:
        yield c
