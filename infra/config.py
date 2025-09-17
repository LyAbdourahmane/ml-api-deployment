# infra/config.py
import os
from dotenv import load_dotenv

# On choisit quel fichier .env charger
env = os.getenv("ENV", "dev")  # par défaut "dev"
dotenv_file = f".env.{env}" if env != "prod" else ".env"
if os.path.exists(dotenv_file):
    load_dotenv(dotenv_file)

# Récupération des variables
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ml")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def get_database_url() -> str:
    """Retourne l'URL de base de données à utiliser.

    Priorité à la variable d'environnement `DATABASE_URL` si définie,
    sinon reconstruit depuis DB_USER/DB_PASSWORD/DB_HOST/DB_PORT/DB_NAME.
    """
    url = os.getenv("DATABASE_URL")
    if url and url.strip():
        return url
    return f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def is_auth_enabled() -> bool:
    """Indique si l'authentification via X-API-Key est activée."""
    return _as_bool(os.getenv("AUTH_ENABLED"), default=True)


def get_api_key() -> str | None:
    """Retourne la clé API attendue si l'authentification est activée."""
    return os.getenv("API_KEY")