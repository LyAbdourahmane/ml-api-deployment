FROM python:3.12-slim

# Répertoire de travail
WORKDIR /app

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=7860 \
    API_BASE_URL=http://localhost:8000

# Dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Dépendances Python
COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Code source
COPY . .

# Utilisateur non-root
RUN adduser --disabled-password --gecos "" appuser \
 && chown -R appuser:appuser /app
USER appuser

# Port exposé
EXPOSE ${PORT}

# Commande de démarrage
CMD ["python", "gradio_app.py"]
