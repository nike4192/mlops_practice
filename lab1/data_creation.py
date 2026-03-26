#!/usr/bin/env python3
"""Генерация синтетических данных о температуре для обучения и тестирования."""

import numpy as np
import pandas as pd
from pathlib import Path


def create_temperature_dataset(num_days=365, anomaly_rate=0.05, seed=42):
    """Создаёт синтетический датасет температуры с сезонным паттерном."""
    np.random.seed(seed)

    data = []
    for day in range(num_days):
        day_of_year = day % 365
        # Сезонный паттерн
        base_temp = 15 + 10 * np.sin(2 * np.pi * day_of_year / 365)
        noise = np.random.normal(0, 2)
        temperature = base_temp + noise

        # Аномалии
        if np.random.random() < anomaly_rate:
            temperature += np.random.choice([-1, 1]) * np.random.uniform(10, 20)

        # Влажность (обратная зависимость от температуры)
        humidity = 70 - (temperature - 15) * 2 + np.random.normal(0, 5)
        humidity = np.clip(humidity, 20, 95)

        # Сезон
        if day_of_year < 80 or day_of_year >= 355:
            season = "winter"
        elif 80 <= day_of_year < 172:
            season = "spring"
        elif 172 <= day_of_year < 264:
            season = "summer"
        else:
            season = "autumn"

        data.append({
            'day': day,
            'temperature': round(temperature, 2),
            'humidity': round(humidity, 2),
            'season': season
        })

    return pd.DataFrame(data)


def main():
    lab_dir = Path(__file__).parent
    train_dir = lab_dir / "train"
    test_dir = lab_dir / "test"
    train_dir.mkdir(exist_ok=True)
    test_dir.mkdir(exist_ok=True)

    print("Создание датасетов...")

    # Тренировочные
    df1 = create_temperature_dataset(365, anomaly_rate=0.02, seed=42)
    df1.to_csv(train_dir / "temperature_normal.csv", index=False)
    print(f"  train/temperature_normal.csv — {len(df1)} строк")

    df2 = create_temperature_dataset(365, anomaly_rate=0.08, seed=43)
    df2.to_csv(train_dir / "temperature_anomalies.csv", index=False)
    print(f"  train/temperature_anomalies.csv — {len(df2)} строк")

    # Тестовые
    df3 = create_temperature_dataset(100, anomaly_rate=0.03, seed=44)
    df3.to_csv(test_dir / "temperature_test_normal.csv", index=False)
    print(f"  test/temperature_test_normal.csv — {len(df3)} строк")

    df4 = create_temperature_dataset(100, anomaly_rate=0.07, seed=45)
    df4.to_csv(test_dir / "temperature_test_anomalies.csv", index=False)
    print(f"  test/temperature_test_anomalies.csv — {len(df4)} строк")

    print("Готово!")


if __name__ == "__main__":
    main()
