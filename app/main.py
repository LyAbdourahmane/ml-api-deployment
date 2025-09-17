from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session, joinedload

from infra.config import is_auth_enabled, get_api_key
from infra.db import get_db
from infra.models import Input, Prediction
from infra.db_utils import save_input, save_prediction

# src/model.py expose: load_model(), predict(dict)->float, get_model_info()->dict
from src.model import predict, get_model_info, load_model

# pour valider le payload, on s'aligne sur es features
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class PredictPayload(BaseModel):
    PrimaryPropertyType: str = Field(..., description="Type de propriété principal")
    YearBuilt: int = Field(..., ge=1800, le=datetime.now().year, description="Année de construction")
    NumberofBuildings: int = Field(..., ge=1, description="Nombre de bâtiments sur le site")
    NumberofFloors: int = Field(..., ge=0, description="Nombre d'étages")
    LargestPropertyUseType: str = Field(..., description="Type d'usage principal")
    LargestPropertyUseTypeGFA: float = Field(..., ge=1, description="Surface utile du type d’usage majeur")

    @field_validator('PrimaryPropertyType', 'LargestPropertyUseType')
    @classmethod
    def non_empty_str(cls, v):
        if not str(v).strip():
            raise ValueError("La valeur ne doit pas être vide.")
        return v

app = FastAPI(
    title="API Prédiction CO₂",
    description="API pour prédire les émissions de CO₂ des bâtiments (Seattle).",
    version="1.0.0",
)

def _verify_api_key(x_api_key: str | None) -> None:
    if not is_auth_enabled():
        return
    expected = get_api_key()
    if not expected or x_api_key != expected:
        raise HTTPException(status_code=401, detail="Clé API invalide ou absente")

@app.get("/")
def home():
    return {
        "message": "Bienvenue sur l'API de prédiction CO₂",
        "endpoints": ["/predict", "/model_info", "/predictions", "/health"],
    }

@app.get("/health")
def health():
    try:
        load_model()
        return {"status": "healthy", "model_loaded": True}
    except Exception:
        return {"status": "degraded", "model_loaded": False}

@app.get("/model_info")
def model_info(x_api_key: str | None = Header(default=None, alias="X-API-Key")):
    _verify_api_key(x_api_key)
    return get_model_info()

@app.post("/predict")
def predict_endpoint(
    payload: PredictPayload,
    db: Session = Depends(get_db),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    _verify_api_key(x_api_key)

    # 1) prédiction via TON modèle (src/model.py)
    features = payload.model_dump()
    y_pred = predict(features)

    # 2) traçabilité: enregistrement input + output en BDD
    input_id = save_input(db, features)
    save_prediction(db, input_id, y_pred)
    db.commit()

    # 3) réponse
    return {
        "prediction": y_pred,
        "unit": "Metric Tons CO2e",
        "model_info": get_model_info(),
        "input_features": payload,
    }

@app.get("/predictions")
def predictions_history(
    db: Session = Depends(get_db),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    _verify_api_key(x_api_key)
    rows = (
        db.query(Prediction)
        .options(joinedload(Prediction.input))
        .order_by(Prediction.id.desc())
        .limit(100)
        .all()
    )
    history = []
    for p in rows:
        i = p.input
        history.append(
            {
                "prediction_id": p.id,
                "input_id": p.input_id,
                "predicted_co2": p.predicted_co2,
                "prediction_date": str(p.created_at),
                "input_data": {
                    "PrimaryPropertyType": i.PrimaryPropertyType,
                    "YearBuilt": i.YearBuilt,
                    "NumberofBuildings": i.NumberofBuildings,
                    "NumberofFloors": i.NumberofFloors,
                    "LargestPropertyUseType": i.LargestPropertyUseType,
                    "LargestPropertyUseTypeGFA": i.LargestPropertyUseTypeGFA,
                    "created_at": str(i.created_at),
                },
            }
        )
    return {"total_predictions": len(history), "predictions": history}
