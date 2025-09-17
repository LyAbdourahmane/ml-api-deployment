# train_and_save.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, FunctionTransformer
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.pipeline import make_pipeline
from xgboost import XGBRegressor
import numpy as np
from sklearn.preprocessing import LabelEncoder

from src.payload_setup import label_encode_columns


def build_pipeline():
    num_selector = make_column_selector(dtype_include=[np.number])
    cate_selector = make_column_selector(dtype_exclude=[np.number])

    num_pipeline = make_pipeline(SimpleImputer(strategy='median'), RobustScaler())
    label_pipeline = make_pipeline(FunctionTransformer(label_encode_columns, validate=False))

    preprocessor = make_column_transformer(
        (num_pipeline, num_selector),
        (label_pipeline, cate_selector),
        verbose_feature_names_out=False
    )

    model = make_pipeline(
        preprocessor,
        XGBRegressor(
            random_state=0,
            n_estimators=65,
            learning_rate=0.18,
            max_depth=2,
            subsample=0.85,
            gamma=0.3
        )
    )
    return model

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

def train_and_save(data_path, model_path, metadata_path):
    df = pd.read_csv(data_path)
    trainset, testset = train_test_split(
        df, test_size=0.2, random_state=0, stratify=df['PrimaryPropertyType']
    )

    X_train = trainset.drop(columns=['SiteEnergyUseWN(kBtu)', 'TotalGHGEmissions', 'ENERGYSTARScore'])
    y_train = trainset['TotalGHGEmissions']

    X_test = testset.drop(columns=['SiteEnergyUseWN(kBtu)', 'TotalGHGEmissions', 'ENERGYSTARScore'])
    y_test = testset['TotalGHGEmissions']

    model = build_pipeline()
    model.fit(X_train, y_train)

    #Prédictions sur le test set
    y_pred = model.predict(X_test)

    #Calcul des métriques
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    wape = np.sum(np.abs(y_test - y_pred)) / np.sum(np.abs(y_test))
    r2 = r2_score(y_test, y_pred)

    # Sauvegarde du modèle
    joblib.dump(model, model_path)

    #Sauvegarde des métadonnées complètes
    metadata = {
        'feature_names': X_train.columns.tolist(),
        'target_name': 'TotalGHGEmissions',
        'model_type': 'XGBoost',
        'performance': {
            'rmse': rmse,
            'mae': mae,
            'wape': wape,
            'r2_score': r2
        },
        'description': (
            "Total greenhouse gas emissions (CO2, CH4, N2O) from energy consumption, "
            "expressed in CO2-equivalent using 2023 utility-specific emissions factors."
        )
    }
    joblib.dump(metadata, metadata_path)

    return model, metadata


if __name__ == "__main__":
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_DIR = os.path.join(BASE_DIR, "..", "models")
    os.makedirs(MODEL_DIR, exist_ok=True)

    DATA_PATH = os.path.join(BASE_DIR, "ville_de_seattle.csv")
    MODEL_PATH = os.path.join(MODEL_DIR, "model_emissions_co2.joblib")
    METADATA_PATH = os.path.join(MODEL_DIR, "model_metadata.joblib")

    model, metadata = train_and_save(DATA_PATH, MODEL_PATH, METADATA_PATH)
    print(f"Modèle sauvegardé dans {MODEL_PATH}")
    print(f"Métadonnées sauvegardées dans {METADATA_PATH}")
