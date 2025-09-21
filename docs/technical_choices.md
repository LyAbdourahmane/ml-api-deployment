# Documentation des Choix Techniques

## Vue d'ensemble

Ce document justifie les choix techniques effectués dans le développement de l'API de prédiction des émissions CO₂, en expliquant les alternatives considérées et les raisons des décisions prises.

## Architecture Générale

### Choix : Architecture Microservices Modulaire

**Décision** : Séparation claire entre API, interface web, et logique métier.

**Justification** :
- **Maintenabilité** : Chaque composant a une responsabilité unique
- **Évolutivité** : Possibilité de déployer les composants indépendamment
- **Testabilité** : Tests unitaires et d'intégration facilités
- **Réutilisabilité** : L'API peut être utilisée par d'autres interfaces

## Backend - FastAPI

### Choix : FastAPI comme Framework Web

**Décision** : Utilisation de FastAPI pour l'API REST.

**Justification** :
- **Performance** : Un des frameworks Python les plus rapides
- **Documentation automatique** : Swagger/OpenAPI intégré
- **Validation native** : Pydantic pour la validation des données
- **Type hints** : Support natif des annotations de type
- **Async/await** : Support natif pour la programmation asynchrone

**Alternatives considérées** :
- **Django REST** : Rejeté pour la lourdeur et la complexité
- **Flask** : Rejeté pour le manque de validation native
- **Express.js** : Rejeté pour maintenir la cohérence Python

### Choix : Pydantic pour la Validation

**Décision** : Utilisation de Pydantic pour la validation des données.

**Justification** :
- **Validation automatique** : Contraintes métier appliquées automatiquement
- **Documentation** : Schémas générés automatiquement
- **Performance** : Validation rapide avec Rust sous-jacent
- **Type safety** : Intégration avec les type hints Python

**Exemple de validation** :
```python
class PredictPayload(BaseModel):
    YearBuilt: int = Field(..., ge=1800, le=datetime.now().year)
    NumberofBuildings: int = Field(..., ge=1)
    
    @field_validator('PrimaryPropertyType')
    @classmethod
    def non_empty_str(cls, v):
        if not str(v).strip():
            raise ValueError("La valeur ne doit pas être vide.")
        return v
```

## Machine Learning - XGBoost

### Choix : XGBoost comme Algorithme Principal

**Décision** : Utilisation de XGBoost pour la régression.

**Justification** :
- **Performance** : Excellent sur les données tabulaires (en particulier ceux en disposition)
- **Robustesse** : Gestion native des valeurs manquantes
- **Interprétabilité** : Feature importance disponible
- **Rapidité** : Entraînement et prédiction rapides
- **Métriques** : R² = 0.78, RMSE = 45.2

**Alternatives considérées** :
- **Random Forest** : Performance inférieure (R² = 0.72)
- **Linear Regression** : Trop simple pour la complexité des données
- **SVM** : Performance inférieur

### Choix : Pipeline de Préprocessing

**Décision** : Pipeline scikit-learn avec imputation et scaling.

**Justification** :
- **Reproductibilité** : Même preprocessing en entraînement et prédiction
- **Robustesse** : Gestion des valeurs manquantes
- **Performance** : Scaling adapté aux algorithmes tree-based

```python
# Pipeline de préprocessing
num_pipeline = make_pipeline(
    SimpleImputer(strategy='median'),  # Robust aux outliers
    RobustScaler()                     # Moins sensible aux outliers que StandardScaler
)

cat_pipeline = make_pipeline(
    FunctionTransformer(label_encode_columns)  # Encoding simple et efficace
)
```

**Alternatives considérées** :
- **OneHotEncoder** : Rejeté pour la dimensionalité élevée
- **StandardScaler** : Rejeté pour la sensibilité aux outliers
- **KNNImputer** : Rejeté pour la complexité et la performance

## Base de Données - PostgreSQL

### Choix : PostgreSQL comme SGBD

**Décision** : Utilisation de PostgreSQL pour la persistance.

**Justification** :
- **Fiabilité** : ACID compliance et robustesse
- **Performance** : Excellent pour les requêtes complexes
- **Évolutivité** : Support des gros volumes de données
- **Écosystème** : Large support dans l'écosystème Python
- **JSON** : Support natif pour les données semi-structurées

**Alternatives considérées** :
- **SQLite** : Rejeté pour les limitations de concurrence
- **MongoDB** : Rejeté pour la complexité des requêtes relationnelles
- **MySQL** : Rejeté pour les limitations de fonctionnalités

### Choix : SQLAlchemy comme ORM

**Décision** : Utilisation de SQLAlchemy pour l'accès aux données.

**Justification** :
- **Maturité** : ORM Python le plus mature
- **Flexibilité** : Support SQL natif et ORM
- **Performance** : Optimisations avancées
- **Type safety** : Support des annotations de type
- **Migration** : Alembic pour les migrations

**Alternatives considérées** :
- **Django ORM** : Rejeté pour la dépendance à Django
- **Peewee** : Rejeté pour les limitations de fonctionnalités
- **Tortoise ORM** : Rejeté pour la maturité insuffisante

## Sécurité

### Choix : Authentification par Clé API

**Décision** : Système d'authentification basé sur des clés API.

**Justification** :
- **Simplicité** : Implémentation et utilisation simples
- **Flexibilité** : Activation/désactivation par environnement
- **Sécurité** : Contrôle d'accès granulaire
- **Audit** : Traçabilité des accès

**Implémentation** :
```python
def _verify_api_key(x_api_key: str | None) -> None:
    if not is_auth_enabled():
        return
    expected = get_api_key()
    if not expected or x_api_key != expected:
        raise HTTPException(status_code=401, detail="Clé API invalide ou absente")
```

**Alternatives considérées** :
- **JWT** : Rejeté pour la complexité excessive
- **OAuth2** : Rejeté pour la complexité d'implémentation
- **Basic Auth** : Rejeté pour la sécurité insuffisante

### Choix : Validation des Entrées

**Décision** : Validation stricte avec Pydantic.

**Justification** :
- **Sécurité** : Prévention des injections et attaques
- **Qualité** : Données cohérentes garanties
- **Documentation** : Schémas automatiquement générés
- **Performance** : Validation rapide

## Interface Web - Gradio

### Choix : Gradio pour l'Interface Utilisateur

**Décision** : Utilisation de Gradio pour l'interface web.

**Justification** :
- **Rapidité** : Développement d'interface en quelques lignes
- **Intégration** : Connexion directe à l'API
- **Responsive** : Interface adaptée à tous les écrans
- **Partage** : Possibilité de partage public
- **Maintenance** : Moins de code à maintenir

**Alternatives considérées** :
- **Streamlit** : Rejeté pour les limitations de personnalisation
- **React/Vue** : Rejeté pour la complexité de développement
- **Flask Templates** : Rejeté pour le temps de développement

## Conteneurisation - Docker

### Choix : Docker pour la Conteneurisation

**Décision** : Utilisation de Docker pour le déploiement.

**Justification** :
- **Portabilité** : Fonctionne sur tous les environnements
- **Reproductibilité** : Environnement identique partout
- **Isolation** : Séparation des dépendances
- **Évolutivité** : Facilite le scaling horizontal
- **CI/CD** : Intégration facile dans les pipelines

**Dockerfile optimisé** :
```dockerfile
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app
EXPOSE 8000
CMD ["sh", "-c", "python -m infra.create_db && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

**Alternatives considérées** :
- **Vagrant** : Rejeté pour la lourdeur
- **Kubernetes** : Rejeté pour la complexité excessive
- **Déploiement direct** : Rejeté pour les problèmes de dépendances

## Tests - pytest

### Choix : pytest comme Framework de Tests

**Décision** : Utilisation de pytest pour les tests.

**Justification** :
- **Simplicité** : Syntaxe claire et concise
- **Fonctionnalités** : Fixtures, paramétrage, couverture
- **Écosystème** : Plugins riches (cov, mock, etc.)
- **Performance** : Exécution rapide des tests
- **Intégration** : Support CI/CD natif

**Structure des tests** :
```
tests/
├── conftest.py              # Configuration et fixtures
├── test_api.py              # Tests des endpoints
├── test_db.py               # Tests de base de données
├── test_model_with_real_data.py  # Tests du modèle
└── test_train_and_save.py   # Tests d'entraînement
```

**Alternatives considérées** :
- **unittest** : Rejeté pour la verbosité
- **nose2** : Rejeté pour la maintenance limitée
- **pytest-asyncio** : Intégré pour les tests async

## Déploiement

### Choix : Déploiement Multi-Environnements

**Décision** : Support de plusieurs environnements (dev, prod).

**Justification** :
- **Séparation** : Isolation des environnements
- **Configuration** : Variables d'environnement par contexte
- **Sécurité** : Clés différentes par environnement
- **Flexibilité** : Adaptation aux besoins

**Configuration par environnement** :
```python
# infra/config.py
env = os.getenv("ENV", "dev")
dotenv_file = f".env.{env}" if env != "prod" else ".env"
```

**Alternatives considérées** :
- **Configuration unique** : Rejeté pour la sécurité
- **Configuration dynamique** : Rejeté pour la complexité

## Performance et Optimisation

### Choix : Optimisations Spécifiques

**Décision** : Optimisations ciblées pour les performances.

**Justifications** :

1. **Chargement du modèle** :
   - Modèle chargé une seule fois au démarrage
   - Cache en mémoire pour les prédictions rapides

2. **Base de données** :
   - Index sur les colonnes fréquemment utilisées
   - Requêtes optimisées avec SQLAlchemy

3. **API** :
   - Validation rapide avec Pydantic
   - Réponses JSON optimisées

4. **Docker** :
   - Image basée sur python:3.12-slim
   - Installation des dépendances en cache

## Évolutivité

### Choix : Architecture Évolutive

**Décision** : Design permettant l'évolution future.

**Justifications** :

1. **Modularité** :
   - Séparation claire des responsabilités
   - Interfaces bien définies

2. **Configuration** :
   - Variables d'environnement pour la flexibilité
   - Support multi-environnements

3. **Base de données** :
   - Schéma extensible
   - Migrations avec Alembic

4. **API** :
   - Versioning possible
   - Endpoints extensibles

## Documentation

### Choix : Documentation Multi-Formats

**Décision** : Documentation complète et variée.

**Justifications** :

1. **README.md** : Vue d'ensemble et guide d'utilisation
2. **docs/** : Documentation technique détaillée
3. **Swagger/OpenAPI** : Documentation interactive de l'API
4. **Docstrings** : Documentation du code
5. **Tests** : Documentation par l'exemple

## Conclusion

Les choix techniques effectués privilégient :

- **Simplicité** : Solutions éprouvées et maintenables
- **Performance** : Optimisations ciblées et efficaces
- **Sécurité** : Bonnes pratiques et validation stricte
- **Évolutivité** : Architecture modulaire et extensible
- **Documentation** : Clarté et facilité d'utilisation

Ces décisions permettent un développement rapide, une maintenance aisée et une évolution future facilitée.

---

*Cette documentation est mise à jour avec chaque évolution technique du projet.*
