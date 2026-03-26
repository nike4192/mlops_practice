# Лаба 3: Контейнеризация ML-модели

Flask API для обслуживания предсказаний модели Iris в Docker-контейнере.

## Файлы

- `train_model.py` — обучение RandomForest на Iris, сохранение в pickle
- `app.py` — Flask-сервер с эндпоинтами `/predict`, `/predict/batch`, `/health`
- `test_api.py` — тесты API

## Запуск

```bash
pip install -r requirements.txt
python train_model.py   # обучение модели
python app.py           # запуск сервера на порту 5000
python test_api.py      # тесты (в отдельном терминале)
```

## API

- `GET /health` — проверка состояния
- `GET /model/info` — информация о модели
- `POST /predict` — предсказание: `{"features": [5.1, 3.5, 1.4, 0.2]}`
- `POST /predict/batch` — батч: `{"batch": [[5.1, 3.5, 1.4, 0.2], ...]}`
