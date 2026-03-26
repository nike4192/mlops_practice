#!/usr/bin/env python3
"""Предобработка данных: масштабирование числовых признаков с помощью StandardScaler."""

import pandas as pd
import pickle
from pathlib import Path
from sklearn.preprocessing import StandardScaler


def load_datasets(data_dir):
    """Загружает все CSV из директории."""
    datasets = {}
    for csv_file in data_dir.glob("*.csv"):
        datasets[csv_file.stem] = pd.read_csv(csv_file)
    return datasets


def main():
    lab_dir = Path(__file__).parent
    train_dir = lab_dir / "train"
    test_dir = lab_dir / "test"

    print("Загрузка данных...")
    train_datasets = load_datasets(train_dir)
    test_datasets = load_datasets(test_dir)

    if not train_datasets:
        raise FileNotFoundError(f"Нет CSV в {train_dir}. Сначала запусти data_creation.py")

    print(f"  Тренировочных: {len(train_datasets)}, тестовых: {len(test_datasets)}")

    # Объединяем train для обучения скейлера
    train_combined = pd.concat(train_datasets.values(), ignore_index=True)
    numerical_cols = [col for col in train_combined.columns
                     if col not in ['day', 'season'] and pd.api.types.is_numeric_dtype(train_combined[col])]
    print(f"Числовые признаки: {numerical_cols}")

    # Обучение скейлера
    scaler = StandardScaler()
    scaler.fit(train_combined[numerical_cols])

    # Масштабирование train
    for name, df in train_datasets.items():
        df_scaled = df.copy()
        df_scaled[numerical_cols] = scaler.transform(df[numerical_cols])
        df_scaled.to_csv(train_dir / f"{name}_scaled.csv", index=False)

    # Масштабирование test
    for name, df in test_datasets.items():
        df_scaled = df.copy()
        df_scaled[numerical_cols] = scaler.transform(df[numerical_cols])
        df_scaled.to_csv(test_dir / f"{name}_scaled.csv", index=False)

    # Сохраняем скейлер
    with open(lab_dir / "scaler.pkl", 'wb') as f:
        pickle.dump(scaler, f)

    print("Предобработка завершена!")


if __name__ == "__main__":
    main()
