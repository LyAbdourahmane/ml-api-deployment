# src/payload_setup.py
from sklearn.preprocessing import LabelEncoder
import pandas as pd

def label_encode_columns(df: pd.DataFrame) -> pd.DataFrame:
    df_encoded = df.copy()
    for col in df_encoded.columns:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
    return df_encoded
