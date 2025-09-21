# Besoins Analytiques et Métriques

## Vue d'ensemble

Ce document définit les besoins analytiques, les métriques de performance et les indicateurs clés pour l'API de prédiction des émissions CO₂.

## Objectifs Analytiques

### Objectifs Principaux

1. **Performance du Modèle**
   - Mesurer la précision des prédictions
   - Détecter la dérive des performances
   - Optimiser les paramètres du modèle

2. **Utilisation de l'API**
   - Comprendre les patterns d'utilisation
   - Identifier les cas d'usage principaux
   - Optimiser les performances techniques

3. **Qualité des Données**
   - Surveiller la qualité des inputs
   - Détecter les anomalies
   - Améliorer la validation

4. **Impact Business**
   - Mesurer l'adoption de l'API
   - Évaluer la satisfaction utilisateur
   - Guider les évolutions futures

## Métriques de Performance du Modèle

### Métriques Techniques

| Métrique | Valeur Actuelle | Objectif | Seuil d'Alerte |
|----------|-----------------|----------|----------------|
| **RMSE** | 402.4 | < 300 | > 550 |
| **MAE** | 113.9 | < 100 | > 110 |
| **WAPE** | 0.58 (58%) | < 30% | > 60% |
| **R²** | 0.78 | > 0.78 | < 0.70 |

### Métriques de Dérive

1. **Data Drift**
   - Distribution des features d'entrée
   - Comparaison avec les données d'entraînement
   - Détection des changements de patterns

2. **Concept Drift**
   - Évolution des relations features/target
   - Performance sur les nouvelles données
   - Détection des changements métier

3. **Performance Drift**
   - Évolution des métriques dans le temps
   - Comparaison avec les performances de référence
   - Alertes automatiques


## Métriques d'Utilisation de l'API

##  Métriques de Qualité des Données

### Qualité des Prédictions

1. **Cohérence des Prédictions**
   - Comparaison avec des prédictions similaires
   - Détection d'incohérences
   - Validation croisée

2. **Plausibilité des Résultats**
   - Vérification des plages de valeurs
   - Comparaison avec des références métier
   - Alertes sur les valeurs extrêmes

## Indicateurs Clés de Performance (KPI)

### KPI Techniques

 **Précision du Modèle**
   - R² maintenu > 0.78
   - RMSE maintenu < 402
   - MAE maintenu < 113

### KPI Business

1. **Adoption**
   - Croissance du nombre d'utilisateurs
   - Fréquence d'utilisation
   - Rétention des utilisateurs

2. **Satisfaction**
   - Temps de réponse perçu
   - Facilité d'utilisation
   - Qualité des prédictions

3. **Impact**
   - Nombre de décisions basées sur les prédictions
   - Réduction des émissions CO₂ estimée
   - Valeur ajoutée pour les utilisateurs

*Cette documentation des besoins analytiques évolue avec les objectifs et les métriques du projet.*
