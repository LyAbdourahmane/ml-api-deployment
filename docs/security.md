# Documentation de Sécurité

## Vue d'ensemble

Ce document décrit les mesures de sécurité implémentées dans l'API de prédiction des émissions CO₂, les bonnes pratiques appliquées et les recommandations pour un déploiement sécurisé.

## Architecture de Sécurité

### Principes de Sécurité Appliqués

1. **Principe du Moindre Privilège**
   - Accès minimal nécessaire aux ressources
   - Séparation des environnements
   - Isolation des composants

2. **Défense en Profondeur**
   - Multiple couches de sécurité
   - Validation à chaque niveau
   - Monitoring continu

3. **Sécurité par Conception**
   - Intégration dès le développement
   - Validation automatique
   - Tests de sécurité

## Authentification et Autorisation

### Système d'Authentification par Clé API

**Implémentation** :
```python
def _verify_api_key(x_api_key: str | None) -> None:
    if not is_auth_enabled():
        return
    expected = get_api_key()
    if not expected or x_api_key != expected:
        raise HTTPException(status_code=401, detail="Clé API invalide ou absente")
```

**Caractéristiques** :
- **Clé unique** : Une clé par environnement
- **Rotation** : Changement régulier recommandé
- **Stockage sécurisé** : Variables d'environnement
- **Transmission** : Header HTTP `X-API-Key`

### Configuration de Sécurité

| Paramètre | Développement | Production | Description |
|-----------|---------------|------------|-------------|
| `AUTH_ENABLED` | `false` | `true` | Activation de l'authentification |
| `API_KEY` | `dev-key-123` | `complex-secret-key` | Clé API |
| `ENV` | `dev` | `prod` | Environnement |

### Bonnes Pratiques d'Authentification

1. **Génération de Clés Sécurisées**
```python
import secrets
# Générer une clé API sécurisée
api_key = secrets.token_urlsafe(32)
print(f"API_KEY={api_key}")
```

2. **Rotation des Clés**
   - Changement mensuel recommandé
   - Notification des utilisateurs
   - Période de transition

3. **Gestion des Clés**
   - Stockage dans des variables d'environnement
   - Jamais dans le code source
   - Chiffrement au repos

## Validation et Sécurisation des Données

### Validation des Entrées

**Pydantic pour la Validation** :
```python
class PredictPayload(BaseModel):
    PrimaryPropertyType: str = Field(..., description="Type de propriété principal")
    YearBuilt: int = Field(..., ge=1800, le=datetime.now().year)
    NumberofBuildings: int = Field(..., ge=1)
    NumberofFloors: int = Field(..., ge=0)
    LargestPropertyUseType: str = Field(..., description="Type d'usage principal")
    LargestPropertyUseTypeGFA: float = Field(..., ge=1)

    @field_validator('PrimaryPropertyType', 'LargestPropertyUseType')
    @classmethod
    def non_empty_str(cls, v):
        if not str(v).strip():
            raise ValueError("La valeur ne doit pas être vide.")
        return v
```

**Protections Implémentées** :
- **Validation de type** : Types stricts
- **Contraintes métier** : Plages de valeurs valides
- **Validation de contenu** : Chaînes non vides
- **Sanitisation** : Nettoyage automatique


## Configuration de Sécurité par Environnement

### Développement

```env
# .env.dev
ENV=dev
AUTH_ENABLED=False
API_KEY=dev-key-123
DB_PASSWORD=dev-password
DEBUG=true
```

**Caractéristiques** :
- **Authentification désactivée** pour faciliter le développement
- **Mots de passe simples** (non critiques)
- **Debug activé** pour le développement

### Production

```env
# .env.prod
ENV=prod
AUTH_ENABLED=true
API_KEY=complex-secure-key-32-chars
DB_PASSWORD=strong-production-password
DEBUG=false
```

**Caractéristiques** :
- **Authentification obligatoire**
- **Mots de passe complexes**
- **Debug désactivé**
- **Logs de sécurité activés**

*Cette documentation de sécurité est mise à jour régulièrement pour refléter les meilleures pratiques et les évolutions des menaces.*
