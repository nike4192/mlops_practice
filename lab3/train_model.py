"""Обучение модели Iris для контейнеризации."""

import pickle
import os
import json
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

os.makedirs('models', exist_ok=True)

# Загрузка данных
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# Обучение
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])
pipeline.fit(X_train, y_train)

print(f"Train accuracy: {pipeline.score(X_train, y_train):.4f}")
print(f"Test accuracy:  {pipeline.score(X_test, y_test):.4f}")

# Сохранение модели
with open('models/iris_model.pkl', 'wb') as f:
    pickle.dump(pipeline, f)

# Метаданные
metadata = {
    'model_name': 'Iris Classifier',
    'model_version': '1.0',
    'features': ['sepal_length', 'sepal_width', 'petal_length', 'petal_width'],
    'classes': ['setosa', 'versicolor', 'virginica'],
    'test_accuracy': float(pipeline.score(X_test, y_test))
}

with open('models/metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print("Модель сохранена в models/")
