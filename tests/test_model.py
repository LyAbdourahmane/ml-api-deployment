# test_model.py
import pytest
import sys
import os
import numpy as np

# Ajoutons src au path pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from model import load_model, predict

# ==== Fixtures ====
@pytest.fixture
def valid_data():
    return {
        'PrimaryPropertyType': 'Office',
        'YearBuilt': 2000,
        'NumberofBuildings': 1,
        'NumberofFloors': 5,
        'LargestPropertyUseType': 'Office',
        'LargestPropertyUseTypeGFA': 50000.0
    }

# ==== Tests essentiels ====
def test_load_model_success():
    """Test basique du chargement du modèle"""
    try:
        model, metadata = load_model()
        assert model is not None
        assert "feature_names" in metadata
    except FileNotFoundError:
        pytest.skip("Modèle introuvable - entraînez-le avant de tester")

def test_predict_with_valid_data(valid_data):
    """Test d'une prédiction valide"""
    try:
        prediction = predict(valid_data)
        assert isinstance(prediction, float)
        assert prediction >= 0
        assert not np.isnan(prediction)
    except FileNotFoundError:
        pytest.skip("Modèle introuvable - entraînez-le avant de tester")
