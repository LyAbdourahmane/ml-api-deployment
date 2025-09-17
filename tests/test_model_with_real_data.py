import os
import numpy as np
import pandas as pd
import pytest

from src.model import load_model, predict


class TestModelMinimal:
    @pytest.fixture
    def seattle_data(self):
        data_path = os.path.join(
            os.path.dirname(__file__), "..", "src", "ville_de_seattle.csv"
        )
        try:
            return pd.read_csv(data_path)
        except FileNotFoundError:
            pytest.skip("Fichier ville_de_seattle.csv non trouvé")

    def test_data_completeness(self, seattle_data):
        required_columns = [
            "PrimaryPropertyType", "YearBuilt", "NumberofBuildings",
            "NumberofFloors", "LargestPropertyUseType",
            "LargestPropertyUseTypeGFA", "TotalGHGEmissions"
        ]
        for col in required_columns:
            assert col in seattle_data.columns, f"Colonne manquante: {col}"
        assert len(seattle_data) > 0, "Le fichier de données est vide"

    def test_model_load_and_predict(self, seattle_data):
        _model, _meta = load_model()
        sample = seattle_data.iloc[0]
        input_data = {
            "PrimaryPropertyType": sample["PrimaryPropertyType"],
            "YearBuilt": sample["YearBuilt"],
            "NumberofBuildings": sample["NumberofBuildings"],
            "NumberofFloors": sample["NumberofFloors"],
            "LargestPropertyUseType": sample["LargestPropertyUseType"],
            "LargestPropertyUseTypeGFA": sample["LargestPropertyUseTypeGFA"],
        }
        y = predict(input_data)
        assert isinstance(y, (int, float))
        assert y >= 0 and not np.isnan(y) and not np.isinf(y)
