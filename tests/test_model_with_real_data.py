# test_model_with_real_data.py
import pytest
import sys
import os
import pandas as pd
import numpy as np

# Ajout du chemin src au path pour les imports 
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from model import load_model, predict

class TestModelMinimal:
    """Tests indispensables du modèle"""

    @pytest.fixture
    def seattle_data(self):
        """Chargement des données"""
        data_path = os.path.join(os.path.dirname(__file__), "..", "src", "ville_de_seattle.csv")
        try:
            return pd.read_csv(data_path)
        except FileNotFoundError:
            pytest.skip("Fichier ville_de_seattle.csv non trouvé")

    @pytest.fixture
    def model_and_metadata(self):
        """Chargement du modèle et métadonnées"""
        try:
            return load_model()
        except FileNotFoundError:
            pytest.skip("Modèle non trouvé")

    def test_data_completeness(self, seattle_data):
        """Les colonnes essentielles doivent exister et contenir des données"""
        required_columns = [
            'PrimaryPropertyType', 'YearBuilt', 'NumberofBuildings',
            'NumberofFloors', 'LargestPropertyUseType', 
            'LargestPropertyUseTypeGFA', 'TotalGHGEmissions'
        ]
        for col in required_columns:
            assert col in seattle_data.columns, f"Colonne manquante: {col}"
        assert len(seattle_data) > 0, "Le fichier de données est vide"

    def test_model_load_and_predict(self, seattle_data):
        """Vérifie que le modèle se charge et prédit correctement"""
        sample = seattle_data.iloc[0]  # Première ligne
        input_data = {
            'PrimaryPropertyType': sample['PrimaryPropertyType'],
            'YearBuilt': sample['YearBuilt'],
            'NumberofBuildings': sample['NumberofBuildings'],
            'NumberofFloors': sample['NumberofFloors'],
            'LargestPropertyUseType': sample['LargestPropertyUseType'],
            'LargestPropertyUseTypeGFA': sample['LargestPropertyUseTypeGFA']
        }
        prediction = predict(input_data)
        assert isinstance(prediction, (int, float)), "La prédiction n'est pas un nombre"
        assert prediction >= 0, "La prédiction est négative"
        assert not np.isnan(prediction), "La prédiction est NaN"
        assert not np.isinf(prediction), "La prédiction est infinie"
