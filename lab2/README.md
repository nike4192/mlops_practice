# Лаба 2: Jenkins CI/CD Pipeline для ML

Автоматизация ML-пайплайна через Jenkins: сбор данных, предобработка, обучение, оценка.

## Структура

- `Jenkinsfile` — пайплайн из 6 стадий
- `data_collection.py` — загрузка Titanic из seaborn
- `data_preprocessing.py` — обработка пропусков, кодирование, train/test split
- `model_training.py` — обучение LogReg и RandomForest, выбор лучшей
- `model_testing.py` — оценка модели, генерация отчёта

## Локальный запуск

```bash
pip install -r requirements.txt

python data_collection.py
python data_preprocessing.py
python model_training.py
python model_testing.py
```

## Jenkins

1. Создать Pipeline job
2. Указать репозиторий и путь к `lab2/Jenkinsfile`
3. Build Now
