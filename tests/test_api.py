# tests/test_api.py
import pytest

def test_health_endpoint(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert "status" in body and body["status"] in {"healthy", "degraded"}
    assert "model_loaded" in body

@pytest.fixture
def valid_payload():
    return {
        "PrimaryPropertyType": "Office",
        "YearBuilt": 2005,
        "NumberofBuildings": 1,
        "NumberofFloors": 4,
        "LargestPropertyUseType": "Office",
        "LargestPropertyUseTypeGFA": 2200.0,
    }

def test_predict_valid(client, valid_payload):
    r = client.post("/predict", json=valid_payload)
    assert r.status_code == 200
    data = r.json()
    assert "prediction" in data
    assert "model_info" in data
    assert "input_features" in data

def test_predict_invalid_payload(client):
    r = client.post("/predict", json={"YearBuilt": "not_a_number"})
    assert r.status_code == 422

def test_predictions_history_shape(client, valid_payload):
    client.post("/predict", json=valid_payload)
    r = client.get("/predictions")
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body["predictions"], list)
    if body["predictions"]:
        item = body["predictions"][0]
        assert {"prediction_id","input_id","predicted_co2","prediction_date","input_data"} <= set(item)
