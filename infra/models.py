from sqlalchemy import String, Integer, Float, ForeignKey, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infra.db import Base
from datetime import datetime

class Input(Base):
    __tablename__ = "inputs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    PrimaryPropertyType: Mapped[str | None] = mapped_column(String(120))
    YearBuilt: Mapped[int | None] = mapped_column(Integer)
    NumberofBuildings: Mapped[int | None] = mapped_column(Integer)
    NumberofFloors: Mapped[int | None] = mapped_column(Integer)
    LargestPropertyUseType: Mapped[str | None] = mapped_column(String(120))
    LargestPropertyUseTypeGFA: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )

    predictions: Mapped[list["Prediction"]] = relationship(
        back_populates="input", cascade="all, delete-orphan"
    )

class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    input_id: Mapped[int] = mapped_column(
        ForeignKey("inputs.id", ondelete="CASCADE"), index=True
    )
    predicted_co2: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )

    input: Mapped[Input] = relationship(back_populates="predictions")
