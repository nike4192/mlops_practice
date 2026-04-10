"""Unit-тесты Flask API."""

import pytest
from src.app import app

SAMPLE_TRACK = {
    "danceability": 0.72,
    "energy": 0.80,
    "loudness": -5.5,
    "speechiness": 0.06,
    "acousticness": 0.05,
    "instrumentalness": 0.50,
    "liveness": 0.14,
    "valence": 0.40,
    "tempo": 128.0,
}


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_predict_success(client):
    resp = client.post("/predict", json=SAMPLE_TRACK)
    assert resp.status_code == 200
    data = resp.get_json()
    assert "genre" in data
    assert "probabilities" in data
    assert data["genre"] in ["rock", "pop", "hip-hop", "classical", "electronic", "jazz"]


def test_predict_missing_features(client):
    resp = client.post("/predict", json={"danceability": 0.5})
    assert resp.status_code == 400
    assert "Missing features" in resp.get_json()["error"]


def test_predict_no_body(client):
    resp = client.post("/predict", content_type="application/json")
    assert resp.status_code == 400


def test_batch_predict(client):
    resp = client.post("/batch-predict", json={"tracks": [SAMPLE_TRACK, SAMPLE_TRACK]})
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data["predictions"]) == 2
    assert all("genre" in p for p in data["predictions"])


def test_predict_probabilities_sum(client):
    resp = client.post("/predict", json=SAMPLE_TRACK)
    probs = resp.get_json()["probabilities"]
    assert abs(sum(probs.values()) - 1.0) < 0.01
