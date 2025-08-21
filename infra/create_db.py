# create_db.py
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
# Connexion PostgreSQL locale
# Chargons les variables d'environnement
load_dotenv()

mdp = os.getenv("DB_PASSWORD")
user = os.getenv("DB_USER")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")

engine = create_engine(
    f"postgresql+psycopg2://{user}:{mdp}@{host}:{port}/{dbname}",
    echo=True
)
Base = declarative_base()

# Notre Table inputs
class Input(Base):
    __tablename__ = "inputs"
    id = Column(Integer, primary_key=True)
    PrimaryPropertyType = Column(String, nullable=False)
    YearBuilt = Column(Integer, nullable=False)
    NumberofBuildings = Column(Integer, nullable=False)
    NumberofFloors = Column(Integer, nullable=False)
    LargestPropertyUseType = Column(String, nullable=False)
    LargestPropertyUseTypeGFA = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    predictions = relationship("Prediction", back_populates="input_data")

# Notre Table predictions
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)
    input_id = Column(Integer, ForeignKey("inputs.id"))
    predicted_co2 = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    input_data = relationship("Input", back_populates="predictions")


# Crée toutes les tables
Base.metadata.create_all(engine)

print("Tables créées avec succès !")
