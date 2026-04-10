"""Тесты качества модели."""

import pandas as pd
import joblib
import pytest
from pathlib import Path

BASE = Path(__file__).parent.parent
FEATURE_COLS = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo",
]


@pytest.fixture
def model():
    return joblib.load(BASE / "models" / "genre_classifier.pkl")


@pytest.fixture
def scaler():
    return joblib.load(BASE / "models" / "scaler.pkl")


@pytest.fixture
def test_data():
    return pd.read_csv(BASE / "data" / "test.csv")


def test_model_accuracy(model, test_data):
    X = test_data[FEATURE_COLS]
    y = test_data["genre"]
    accuracy = model.score(X, y)
    assert accuracy > 0.7, f"Accuracy {accuracy:.2f} below threshold 0.7"


def test_model_predicts_all_genres(model, test_data):
    X = test_data[FEATURE_COLS]
    predictions = set(model.predict(X))
    expected = set(test_data["genre"].unique())
    assert predictions == expected, f"Missing genres: {expected - predictions}"


def test_no_single_class_dominance(model, test_data):
    """Модель не должна предсказывать один класс для >50% примеров."""
    X = test_data[FEATURE_COLS]
    preds = pd.Series(model.predict(X))
    max_ratio = preds.value_counts().max() / len(preds)
    assert max_ratio < 0.5, f"Single class dominates: {max_ratio:.2%}"


def test_predict_single_sample(model, scaler):
    """Модель корректно обрабатывает один пример."""
    import numpy as np
    sample = np.array([[0.72, 0.80, -5.5, 0.06, 0.05, 0.50, 0.14, 0.40, 128.0]])
    scaled = scaler.transform(sample)
    pred = model.predict(scaled)
    assert len(pred) == 1
    assert pred[0] in ["rock", "pop", "hip-hop", "classical", "electronic", "jazz"]
