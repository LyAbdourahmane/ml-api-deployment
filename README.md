# Prédiction CO₂ des bâtiments de Seattle — API & Interface Gradio

## Description

Projet complet pour entraîner, servir et tester un modèle de régression (XGBoost) qui prédit les émissions de CO₂ des bâtiments non résidentiels de Seattle.

- **API** : FastAPI (docs Swagger/OpenAPI sur `/docs`)
- **Modèle** : XGBoost dans un pipeline scikit-learn
- **Persistance** : PostgreSQL via SQLAlchemy
- **Interface** : Gradio (test visuel du modèle)
- **CI/CD** : GitHub Actions (tests + formatage)
- **Conteneurisation** : Docker (image unique API/Gradio)

---

## Démarrage rapide (local)

### Cloner et installer

```bash
git clone https://github.com/LyAbdourahmane/ml-api-deployment
cd Déployez_un_modèle_de_Machine_Learning
pip install -r requirements.txt
```

### Configurer l’environnement

Créer un fichier `.env` à la racine :

```env
# Base de données PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=prediction_emission
DB_USER=postgres
DB_PASSWORD=motdepasse

# URL complète pour l'API (utilisée par Gradio)
API_BASE_URL=http://localhost:8000

# Optionnel pour Docker
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/prediction_emission
```

### Lancer PostgreSQL et créer les tables

```bash
createdb prediction_emission
python infra/create_db.py
```

### Entraîner le modèle

```bash
python src/train_and_save.py
# Génère : models/model_emissions_co2.joblib et models/model_metadata.joblib
```

### Démarrer l’API

```bash
uvicorn app.API:app --reload --host 0.0.0.0 --port 8000
```

Docs : [http://localhost:8000/docs](http://localhost:8000/docs)

### Lancer l’interface Gradio

```bash
python gradio_app.py
```

Interface : [http://localhost:7860](http://localhost:7860)

---

## Docker (API ou Gradio)

### Construire l’image

```bash
docker build -t co2-app .
```

### Lancer en mode API FastAPI

```bash
docker run --env-file .env -p 8000:8000 co2-app uvicorn app.API:app --host 0.0.0.0 --port 8000
```

### Lancer en mode Gradio

```bash
docker run --env-file .env -p 7860:7860 co2-app python gradio_app.py
```

---

## Déploiement

### Hugging Face Spaces

- Type : **Gradio**
- Fichier : `gradio_app.py`
- Dépendances : `requirements.txt`
- Configurer `API_BASE_URL` dans les Secrets pour pointer vers ton API hébergée (Render ou autre)

### Render

- Type : **Web Service**
- Commande :
  - API : `uvicorn app.API:app --host 0.0.0.0 --port $PORT`
  - Gradio : `python gradio_app.py`
- Variables d’environnement : `DATABASE_URL`, `API_BASE_URL`

---

## Arborescence

```
Déployez_un_modèle_de_Machine_Learning/
  app/                # API FastAPI
  infra/              # Scripts DB
  models/             # Modèle et métadonnées
  src/                # Code ML
  tests/              # Tests Pytest
  gradio_app.py       # Interface Gradio
  Dockerfile
  requirements.txt
  README.md
```

---

## API — Endpoints principaux

- **POST** `/predict` : prédiction + métadonnées
- **GET** `/model_info` : infos modèle
- **GET** `/health` : statut
- **GET** `/predictions` : historique

---

## Tests

```bash
pytest -v
pytest -v --cov=src --cov=app --cov=infra --cov-report=term-missing
```

---

## Support

- Docs API : `/docs`
- Historique : `/predictions`
- Issues : via GitHub

---
