# API de Prédiction des Émissions CO₂ - Bâtiments Non-Résidentiels

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-green.svg)](https://fastapi.tiangolo.com)
[![XGBoost](https://img.shields.io/badge/XGBoost-3.0.5-orange.svg)](https://xgboost.readthedocs.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)

## Table des Matières

- [Vue d'ensemble](#-vue-densemble)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [API Documentation](#-api-documentation)
- [Interface Web](#-interface-web)
- [Déploiement](#-déploiement)
- [Sécurité](#-sécurité)
- [Tests](#-tests)
- [Contribution](#-contribution)

## Vue d'ensemble

Cette API prédit les émissions de CO₂ des bâtiments non-résidentiels basée sur des caractéristiques architecturales et d'usage. Le modèle a été entraîné sur les données de la ville de Seattle et utilise XGBoost pour fournir des prédictions précises.

### Fonctionnalités principales

- **Prédiction en temps réel** des émissions CO₂
- **Traçabilité complète** des inputs/outputs en base de données
- **Authentification par clé API** (optionnelle)
- **Interface web intuitive** avec Gradio
- **Déploiement Docker** prêt à l'emploi
- **Monitoring et métriques** de performance

### Cas d'usage

- **Urbanistes** : Évaluation environnementale de nouveaux projets
- **Architectes** : Optimisation énergétique des bâtiments
- **Politiques publiques** : Planification urbaine durable
- **Certification** : Validation des standards énergétiques

## Architecture

### Stack Technologique

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Interface     │    │   API FastAPI   │    │   Base de       │
│   Gradio        │◄──►│   + Pydantic    │◄──►│   Données       │
│   (Port 7860)   │    │   (Port 8000)   │    │   PostgreSQL    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Modèle ML     │
                       │   XGBoost       │
                       │   (joblib)      │
                       └─────────────────┘
```

### Composants

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| **API Backend** | FastAPI + Pydantic | Endpoints REST, validation, orchestration |
| **Interface Web** | Gradio | Interface utilisateur intuitive |
| **Base de données** | PostgreSQL + SQLAlchemy | Stockage des prédictions et traçabilité |
| **Modèle ML** | XGBoost + scikit-learn | Prédiction des émissions CO₂ |
| **Conteneurisation** | Docker | Déploiement et portabilité |
| **Tests** | pytest | Assurance qualité |

## Installation

### Prérequis

- Python 3.12+
- PostgreSQL 15+
- Docker (optionnel)

### Installation locale

1. **Cloner le repository**
```bash
git clone https://github.com/LyAbdourahmane/ml-api-deployment
cd ml-api-deployment
```

2. **Créer un environnement virtuel**
```bash
python -m venv mon_env
source mon_env/bin/activate  # Linux/Mac
# ou
mon_env\Scripts\activate     # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configuration de la base de données**
```bash
# Créer la base de données PostgreSQL
createdb prediction_emission (ou autre)

# Configurer les variables d'environnement
cp .env.example .env.dev
# Éditer .env.dev avec vos paramètres
```

5. **Initialiser la base de données**
```bash
python -m infra.create_db
```

6. **Entraîner le modèle (si nécessaire)**
```bash
python src/train_and_save.py
```

### Installation avec Docker

```bash
# Construire l'image
docker build -t co2-prediction-api .

# Lancer avec docker-compose
docker-compose up -d
```

## Configuration

### Variables d'environnement

Créez un fichier `.env.dev` ou `.env.prod` :

```env
# Base de données
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ml
DATABASE_URL=postgresql+psycopg2://user:password@host:port/db

# Sécurité
AUTH_ENABLED=true
API_KEY=your-secret-api-key

# Application
ENV=dev
PORT=8000
```

### Configuration par environnement

| Variable | Développement | Production | Description |
|----------|---------------|------------|-------------|
| `ENV` | `dev` | `prod` | Environnement d'exécution |
| `AUTH_ENABLED` | `false` | `true` | Activation de l'authentification |
| `DB_HOST` | `localhost` | `db-container` | Hôte de la base de données |

## Utilisation

### Démarrage de l'API

```bash
# Mode développement
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Mode production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Démarrage de l'interface web

```bash
python ui_gradio.py
```

L'interface sera disponible sur `http://localhost:7860`

### Test rapide

```bash
# Test de santé
curl http://localhost:8000/health

# Test de prédiction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "PrimaryPropertyType": "Office",
    "YearBuilt": 2000,
    "NumberofBuildings": 1,
    "NumberofFloors": 5,
    "LargestPropertyUseType": "Office",
    "LargestPropertyUseTypeGFA": 50000.0
  }'
```

## API Documentation

### Endpoints principaux

| Endpoint | Méthode | Description | Authentification |
|----------|---------|-------------|------------------|
| `/` | GET | Page d'accueil | Non |
| `/health` | GET | État de santé | Non |
| `/model_info` | GET | Informations du modèle | Oui |
| `/predict` | POST | Prédiction CO₂ | Oui |
| `/predictions` | GET | Historique des prédictions | Oui |

### Documentation interactive

Une fois l'API démarrée, accédez à :
- **Swagger UI** : `http://localhost:8000/docs`
- **ReDoc** : `http://localhost:8000/redoc`

### Exemple de requête de prédiction

```json
{
  "PrimaryPropertyType": "Small- and Mid-Sized Office",
  "YearBuilt": 2000,
  "NumberofBuildings": 1,
  "NumberofFloors": 4,
  "LargestPropertyUseType": "Office",
  "LargestPropertyUseTypeGFA": 10000.0
}
```

### Exemple de réponse

```json
{
  "prediction": 186.65,
  "unit": "Metric Tons CO2e",
  "model_info": {
    "model_type": "XGBoost",
    "performance": {
      "rmse": 45.2,
      "mae": 28.7,
      "wape": 0.15,
      "r2_score": 0.78
    }
  },
  "input_features": { ... }
}
```

## Interface Web

L'interface Gradio offre une expérience utilisateur intuitive :

### Fonctionnalités

- **Formulaire interactif** avec validation en temps réel
- **Prédictions instantanées** avec métriques de performance
- **Informations détaillées** sur le modèle
- **Interface responsive** adaptée à tous les écrans

### Accès

- **Local** : `http://localhost:7860`
- **Partage public** : Activé par défaut (option `share=True`)

## Sécurité

### Authentification

L'API utilise un système d'authentification par clé API via header `X-API-Key` :

```bash
curl -H "X-API-Key: your-secret-key" http://localhost:8000/predict
```

### Configuration de sécurité

| Paramètre | Valeur recommandée | Description |
|-----------|-------------------|-------------|
| `AUTH_ENABLED` | `true` (prod) | Active l'authentification |
| `API_KEY` | Chaîne complexe | Clé secrète pour l'API |
| `ENV` | `prod` | Environnement de production |

### Bonnes pratiques

- **Rotation des clés** : Changer régulièrement les clés API
- **HTTPS** : Utiliser SSL/TLS en production
- **Rate limiting** : Implémenter une limitation de débit
- **Logs de sécurité** : Monitorer les tentatives d'accès
- **Validation d'entrée** : Pydantic valide automatiquement les données

## Tests

### Exécution des tests

```bash
# Tous les tests
pytest -v

# Tests avec couverture
pytest --cov=app --cov=src --cov=infra

# Tests spécifiques
pytest tests/test_api.py -v
```

### Types de tests

| Type | Fichier | Description |
|------|---------|-------------|
| **API** | `test_api.py` | Tests des endpoints |
| **Base de données** | `test_db.py` | Tests de persistance |
| **Modèle** | `test_model_with_real_data.py` | Tests de prédiction |
| **Entraînement** | `test_train_and_save.py` | Tests du pipeline ML |

## Déploiement

### Déploiement Docker

```bash
# Construction de l'image
docker build -t co2-prediction-api:latest .

# Lancement du conteneur
docker run -d \
  --name co2-api \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -e API_KEY="your-secret-key" \
  co2-prediction-api:latest
```

## Auteur

**Abdourahamane LY**
- Email : lyabdourahamane66@gmail.com
- LinkedIn : [abdourahamane-ly-ab322a35b](https://www.linkedin.com/in/abdourahamane-ly-ab322a35b/)
- GitHub : [LyAbdourahmane](https://github.com/LyAbdourahmane)
- Site : [Site de Portfolio](https://lyabdourahamane.netlify.app/)

---

*Développé avec ❤️ pour la transition énergétique et l'urbanisme durable*
