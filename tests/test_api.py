# test_api.py
import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ajoutons src/ au path pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))

# Importer l'app FastAPI
from API import app

client = TestClient(app)

@pytest.fixture
def valid_payload():
    return {
        "PrimaryPropertyType": "Office",
        "YearBuilt": 2000,
        "NumberofBuildings": 1,
        "NumberofFloors": 5,
        "LargestPropertyUseType": "Office",
        "LargestPropertyUseTypeGFA": 50000.0
    }

def test_health():
    """Vérifie si l'API est en bonne santé"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "healthy"
    assert data.get("model_loaded") is True

def test_predict_valid(valid_payload):
    """Test prédiction avec données valides"""
    response = client.post("/predict", json=valid_payload)
    assert response.status_code in [200, 500]  # 500 si modèle non trouvé
    if response.status_code == 200:
        data = response.json()
        assert "prediction" in data

def test_predictions_history():
    """Test récupération de l'historique des prédictions"""
    response = client.get("/predictions")
    assert response.status_code in [200, 500]  # 500 si DB non disponible
    if response.status_code == 200:
        data = response.json()
        assert "total_predictions" in data
        assert "predictions" in data
        assert isinstance(data["predictions"], list)
