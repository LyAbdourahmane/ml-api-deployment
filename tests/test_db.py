import pytest
from sqlalchemy.orm import sessionmaker

from infra.db import Base  # <-- Base vient de infra.db
from infra.models import Input, Prediction  # <-- modèles viennent de infra.models
from infra.db_utils import save_input, save_prediction


# Active les FK pour SQLite
def _fk_pragma_on_connect(dbapi_con, con_record):
    cursor = dbapi_con.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.fixture
def session():
    # Session sur le moteur PostgreSQL défini dans l'app
    from infra.db import engine as pg_engine

    Base.metadata.create_all(bind=pg_engine)
    Session = sessionmaker(bind=pg_engine, autoflush=False, autocommit=False)
    s = Session()
    try:
        yield s
    finally:
        s.close()


@pytest.fixture
def sample_input_dict():
    return {
        "PrimaryPropertyType": "Office",
        "YearBuilt": 2000,
        "NumberofBuildings": 1,
        "NumberofFloors": 2,
        "LargestPropertyUseType": "Office",
        "LargestPropertyUseTypeGFA": 1234.5,
    }


def test_save_and_retrieve_input(session, sample_input_dict):
    input_id = save_input(session, sample_input_dict)
    session.commit()
    db_input = session.get(Input, input_id)
    assert db_input is not None
    assert db_input.PrimaryPropertyType == "Office"
    assert db_input.YearBuilt == 2000


def test_save_prediction_linked_to_input(session, sample_input_dict):
    input_id = save_input(session, sample_input_dict)
    pred_id = save_prediction(session, input_id, 42.0)
    session.commit()

    db_pred = session.get(Prediction, pred_id)
    assert db_pred is not None
    assert db_pred.input_id == input_id
    assert abs(db_pred.predicted_co2 - 42.0) < 1e-6


def test_timestamps_present(session, sample_input_dict):
    input_id = save_input(session, sample_input_dict)
    pred_id = save_prediction(session, input_id, 1.23)
    session.commit()

    inp = session.get(Input, input_id)
    pred = session.get(Prediction, pred_id)
    assert inp.created_at is not None
    assert pred.created_at is not None
