# Лаба 1: ML Pipeline

Пайплайн из 4 скриптов для предсказания температуры по синтетическим данным.

## Запуск

```bash
python data_creation.py        # генерация данных
python data_preprocessing.py   # масштабирование
python model_preparation.py    # обучение модели
python model_testing.py        # тестирование
```

## Структура

- `data_creation.py` — генерация синтетических данных (температура, влажность, сезон)
- `data_preprocessing.py` — StandardScaler на числовые признаки
- `model_preparation.py` — обучение RandomForestRegressor
- `model_testing.py` — оценка на тестовых данных (MSE, MAE, R²)
