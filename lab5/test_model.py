"""Тесты качества модели линейной регрессии с pytest."""

import pickle
import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


@pytest.fixture
def model():
    with open("models/linear_model.pkl", "rb") as f:
        return pickle.load(f)


@pytest.fixture
def clean_data():
    df = pd.read_csv("data/clean_data.csv")
    return df[["x1", "x2"]], df["y"]


@pytest.fixture
def noisy_data():
    df = pd.read_csv("data/noisy_data.csv")
    return df[["x1", "x2"]], df["y"]


# --- Тесты на чистых данных (все должны пройти) ---

def test_r2_clean(model, clean_data):
    """R² на чистых данных должен быть > 0.99."""
    X, y = clean_data
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    assert r2 > 0.99, f"R² = {r2:.4f}, ожидалось > 0.99"


def test_mse_clean(model, clean_data):
    """MSE на чистых данных должен быть < 1."""
    X, y = clean_data
    y_pred = model.predict(X)
    mse = mean_squared_error(y, y_pred)
    assert mse < 1.0, f"MSE = {mse:.4f}, ожидалось < 1"


def test_mae_clean(model, clean_data):
    """MAE на чистых данных должен быть < 1."""
    X, y = clean_data
    y_pred = model.predict(X)
    mae = mean_absolute_error(y, y_pred)
    assert mae < 1.0, f"MAE = {mae:.4f}, ожидалось < 1"


def test_coefficients(model):
    """Коэффициенты должны быть близки к истинным (3, 5)."""
    coefs = model.coef_
    assert abs(coefs[0] - 3.0) < 0.5, f"coef[0] = {coefs[0]:.2f}, ожидалось ~3"
    assert abs(coefs[1] - 5.0) < 0.5, f"coef[1] = {coefs[1]:.2f}, ожидалось ~5"


def test_intercept(model):
    """Intercept должен быть близок к 7."""
    assert abs(model.intercept_ - 7.0) < 1.0, \
        f"intercept = {model.intercept_:.2f}, ожидалось ~7"


# --- Тесты на зашумлённых данных (ожидаем провал) ---

def test_r2_noisy(model, noisy_data):
    """R² на зашумлённых данных должен быть > 0.99 (провалится)."""
    X, y = noisy_data
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    assert r2 > 0.99, f"R² = {r2:.4f}, ожидалось > 0.99"


def test_mse_noisy(model, noisy_data):
    """MSE на зашумлённых данных должен быть < 1 (провалится)."""
    X, y = noisy_data
    y_pred = model.predict(X)
    mse = mean_squared_error(y, y_pred)
    assert mse < 1.0, f"MSE = {mse:.4f}, ожидалось < 1"
