"""Обучение модели линейной регрессии на чистых данных."""

import os
import pickle
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

os.makedirs("models", exist_ok=True)

# Загрузка данных
df = pd.read_csv("data/clean_data.csv")
X = df[["x1", "x2"]]
y = df["y"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Обучение
model = LinearRegression()
model.fit(X_train, y_train)

train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f"Коэффициенты: {model.coef_}")
print(f"Intercept: {model.intercept_:.4f}")
print(f"R² (train): {train_score:.6f}")
print(f"R² (test):  {test_score:.6f}")

# Сохранение
with open("models/linear_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Модель сохранена: models/linear_model.pkl")
