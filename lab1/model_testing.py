#!/usr/bin/env python3
"""Тестирование обученной модели на тестовых данных."""

import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


def main():
    lab_dir = Path(__file__).parent
    test_dir = lab_dir / "test"

    # Загрузка тестовых данных
    print("Загрузка тестовых данных...")
    datasets = []
    for csv_file in sorted(test_dir.glob("*_scaled.csv")):
        datasets.append(pd.read_csv(csv_file))

    if not datasets:
        raise FileNotFoundError("Нет scaled-данных. Сначала запусти data_preprocessing.py")

    test_data = pd.concat(datasets, ignore_index=True)
    X_test = test_data[['humidity', 'day']]
    y_test = test_data['temperature']

    # Загрузка модели
    model_path = lab_dir / "model.pkl"
    if not model_path.exists():
        raise FileNotFoundError("Модель не найдена. Сначала запусти model_preparation.py")

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    # Предсказание
    y_pred = model.predict(X_test)

    # Метрики
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\nРезультаты тестирования:")
    print(f"  MSE:  {mse:.4f}")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  MAE:  {mae:.4f}")
    print(f"  R²:   {r2:.4f}")
    print(f"  Точность: {max(0, r2 * 100):.2f}%")

    # Примеры предсказаний
    print(f"\nПримеры (первые 10):")
    print(f"{'Факт':<10} {'Предсказ.':<10} {'Ошибка':<10}")
    print("-" * 30)
    for i in range(min(10, len(y_test))):
        print(f"{y_test.iloc[i]:<10.2f} {y_pred[i]:<10.2f} {y_test.iloc[i] - y_pred[i]:<10.2f}")


if __name__ == "__main__":
    main()
