from sqlalchemy.orm import Session
from infra.models import Input, Prediction

def save_input(db: Session, data: dict) -> int:
    row = Input(**data)
    db.add(row)
    db.flush()
    return row.id

def save_prediction(db: Session, input_id: int, value: float) -> int:
    row = Prediction(input_id=input_id, predicted_co2=value)
    db.add(row)
    db.flush()
    return row.id
