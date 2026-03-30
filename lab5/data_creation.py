"""Генерация данных для тестирования модели линейной регрессии."""

import os
import numpy as np
import pandas as pd

np.random.seed(42)

os.makedirs("data", exist_ok=True)

N = 200

# Чистые данные: y = 3*x1 + 5*x2 + 7
x1 = np.random.uniform(0, 10, N)
x2 = np.random.uniform(0, 10, N)
y_clean = 3 * x1 + 5 * x2 + 7

df_clean = pd.DataFrame({"x1": x1, "x2": x2, "y": y_clean})
df_clean.to_csv("data/clean_data.csv", index=False)
print(f"Чистые данные: {len(df_clean)} строк -> data/clean_data.csv")

# Зашумлённые данные: добавляем сильный шум
noise = np.random.normal(0, 15, N)
y_noisy = 3 * x1 + 5 * x2 + 7 + noise

df_noisy = pd.DataFrame({"x1": x1, "x2": x2, "y": y_noisy})
df_noisy.to_csv("data/noisy_data.csv", index=False)
print(f"Зашумлённые данные: {len(df_noisy)} строк -> data/noisy_data.csv")

print("Готово!")
