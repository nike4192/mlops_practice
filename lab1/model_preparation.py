#!/usr/bin/env python3
"""Обучение модели RandomForest на масштабированных данных."""

import pandas as pd
import pickle
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


def main():
    lab_dir = Path(__file__).parent
    train_dir = lab_dir / "train"

    # Загрузка масштабированных данных
    print("Загрузка данных...")
    datasets = []
    for csv_file in sorted(train_dir.glob("*_scaled.csv")):
        datasets.append(pd.read_csv(csv_file))
        print(f"  {csv_file.name}")

    if not datasets:
        raise FileNotFoundError("Нет scaled-данных. Сначала запусти data_preprocessing.py")

    train_data = pd.concat(datasets, ignore_index=True)
    X = train_data[['humidity', 'day']]
    y = train_data['temperature']

    # Разбиение для валидации
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Train: {len(X_train)}, Val: {len(X_val)}")

    # Обучение
    print("Обучение RandomForest...")
    model = RandomForestRegressor(
        n_estimators=100, max_depth=15,
        min_samples_split=5, min_samples_leaf=2,
        random_state=42, n_jobs=-1
    )
    model.fit(X_train, y_train)

    # Валидация
    y_pred = model.predict(X_val)
    print(f"\nМетрики на валидации:")
    print(f"  MSE:  {mean_squared_error(y_val, y_pred):.4f}")
    print(f"  MAE:  {mean_absolute_error(y_val, y_pred):.4f}")
    print(f"  R²:   {r2_score(y_val, y_pred):.4f}")

    # Сохранение модели
    with open(lab_dir / "model.pkl", 'wb') as f:
        pickle.dump(model, f)

    with open(lab_dir / "features.pkl", 'wb') as f:
        pickle.dump(list(X.columns), f)

    print("\nМодель сохранена!")


if __name__ == "__main__":
    main()
