# Лаба 5: Тестирование качества ML-модели с pytest

Jupyter-ноутбук с автоматическими тестами качества модели линейной регрессии.

## Идея

- Обучаем модель на чистых данных (R² ≈ 0.99)
- Тестируем на чистых и зашумлённых данных
- pytest ловит деградацию качества на шумных данных

## Запуск

```bash
pip install numpy pandas scikit-learn pytest matplotlib
jupyter notebook lab5_testing.ipynb
```

Или из командной строки:
```bash
python data_creation.py
python model_training.py
pytest test_model.py -v
```

## Ожидаемый результат

5 тестов пройдено (чистые данные), 2 провалено (зашумлённые) — это нормально,
показывает что тесты ловят деградацию.
