import joblib
import pandas as pd
import pytest

from src.train_and_save import train_and_save


@pytest.mark.slow
def test_train_and_save(tmp_path):
    # mini dataset factice
    df = pd.DataFrame({
        'PrimaryPropertyType': ['office']*5 + ['classroom']*5,
        'YearBuilt': [2000, 1995, 2010, 2005, 2012, 1998, 2003, 2007, 2015, 2020],
        'NumberofBuildings': [1, 2, 1, 3, 2, 1, 1, 2, 3, 1],
        'NumberofFloors': [5, 10, 3, 7, 4, 6, 8, 9, 2, 1],
        'LargestPropertyUseType': ['Office', 'School']*5,
        'LargestPropertyUseTypeGFA': [1000, 2000, 1500, 2500, 1800, 2200, 1600, 2400, 3000, 1200],
        'SiteEnergyUseWN(kBtu)': [100, 200, 150, 300, 180, 220, 160, 240, 300, 120],
        'TotalGHGEmissions': [10, 20, 15, 25, 18, 22, 16, 24, 30, 12],
        'ENERGYSTARScore': [50, 60, 55, 65, 58, 62, 57, 63, 70, 52]
    })
    csv_path = tmp_path / "fake_data.csv"
    df.to_csv(csv_path, index=False)

    model_path = tmp_path / "model.joblib"
    metadata_path = tmp_path / "metadata.joblib"

    model, metadata = train_and_save(csv_path, model_path, metadata_path)

    assert model_path.exists()
    assert metadata_path.exists()

    loaded_model = joblib.load(model_path)
    loaded_metadata = joblib.load(metadata_path)

    assert 'feature_names' in loaded_metadata and loaded_metadata['feature_names']
    assert hasattr(loaded_model, "predict")
