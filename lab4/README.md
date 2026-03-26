# Lab 4: DVC — версионирование наборов данных

## Цель
Продемонстрировать навыки использования DVC для версионирования данных.

## Датасет
Titanic (seaborn) — признаки: Pclass, Sex, Age.

## 3 версии датасета

| Версия | Описание | Коммит |
|--------|----------|--------|
| v1 | Базовый датасет (с NaN в Age) | `v1: базовый датасет Titanic` |
| v2 | NaN в Age заполнены средним значением | `v2: NaN в Age заполнены средним` |
| v3 | One-hot encoding для признака Sex | `v3: One-hot encoding Sex` |

## Файлы

- `create_dataset.py` — скрипт создания версий датасета
- `setup_dvc.sh` — полный скрипт демонстрации (init → 3 версии → переключение)
- `README.md` — документация

## Быстрый старт

```bash
# Установка
pip install dvc seaborn pandas

# Запуск полной демонстрации
chmod +x setup_dvc.sh
./setup_dvc.sh
```

## Переключение между версиями

```bash
cd dvc_project

# Посмотреть текущую версию
head data/titanic.csv

# Переключиться на v1
git checkout v1 -- data/titanic.csv.dvc
dvc checkout

# Переключиться на v2
git checkout v2 -- data/titanic.csv.dvc
dvc checkout
```

## Удалённое хранилище

В демо используется локальная папка `dvc_remote_storage/`.

Для Google Drive:
```bash
dvc remote add -d gdrive gdrive://<folder_id>
pip install dvc[gdrive]
```
