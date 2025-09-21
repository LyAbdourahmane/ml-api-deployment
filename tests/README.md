# Documentation des Tests

## Vue d'ensemble

Cette documentation décrit la stratégie de tests, les types de tests implémentés et les procédures d'exécution pour l'API de prédiction des émissions CO₂.

## Types de Tests

### Tests Unitaires
- **Objectif** : Tester les fonctions individuelles
- **Couverture** : Logique métier, validation, utilitaires
- **Fichiers** : `test_*.py` dans le répertoire `tests/`

### Tests d'Intégration
- **Objectif** : Tester l'interaction entre composants
- **Couverture** : API endpoints, base de données, modèle ML
- **Fichiers** : `test_api.py`, `test_db.py`

## Structure des Tests

```
tests/
├── conftest.py                    # Configuration et fixtures
├── test_api.py                    # Tests des endpoints API
├── test_db.py                     # Tests de base de données
├── test_model_with_real_data.py   # Tests du modèle ML
├── test_train_and_save.py         # Tests d'entraînement
└── README.md                      # Cette documentation
```

## Exécution des Tests

### Exécution des Tests

```bash
# Tous les tests
pytest

# Tests avec couverture
pytest --cov=app --cov=src --cov=infra

# Tests spécifiques
pytest tests/test_api.py -v

# Tests avec rapport HTML
pytest --cov=app --cov-report=html
```

*Cette documentation des tests est maintenue à jour avec l'évolution du projet et des bonnes pratiques de test.*
