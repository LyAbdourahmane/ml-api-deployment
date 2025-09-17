# ========= Base =========
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PGCLIENTENCODING=UTF8 \
    ENV=prod

WORKDIR /app

# ========= Dépendances =========
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# ========= Code =========
COPY . /app

# ========= Réseau =========
EXPOSE 8000

# ========= Démarrage =========
# 1) crée la DB + tables si besoin
# 2) lance l'API
CMD ["sh", "-c", "python -m infra.create_db && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
