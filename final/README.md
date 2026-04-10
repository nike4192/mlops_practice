# Music Genre Classifier

ML-конвейер для классификации музыкальных жанров по аудио-характеристикам трека.

## Структура проекта

```
final/
├── src/
│   ├── data_collection.py      # Генерация/сбор датасета
│   ├── data_preprocessing.py   # Предобработка данных
│   ├── train.py                # Обучение модели
│   └── app.py                  # Flask API
├── data/                       # Данные (DVC)
├── models/                     # Обученные модели
├── tests/
│   ├── test_api.py             # Unit-тесты API
│   ├── test_data_quality.py    # Тесты качества данных
│   └── test_model.py           # Тесты качества модели
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Запуск

```bash
pip install -r requirements.txt
python src/data_collection.py
python src/data_preprocessing.py
python src/train.py
python src/app.py
```

## API

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"danceability": 0.7, "energy": 0.8, "loudness": -5.0, "speechiness": 0.05, "acousticness": 0.1, "instrumentalness": 0.0, "liveness": 0.15, "valence": 0.6, "tempo": 120.0}'
```

## Тесты

```bash
pytest tests/ -v
```

## Docker

```bash
docker-compose up --build
```
