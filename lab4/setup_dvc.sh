#!/bin/bash
# Демонстрация DVC: создание 3 версий датасета с версионированием

set -e

PROJECT_DIR="dvc_project"
REMOTE_DIR="dvc_remote_storage"

echo "=== Инициализация проекта ==="

# Очистка предыдущего запуска
rm -rf "$PROJECT_DIR" "$REMOTE_DIR"
mkdir -p "$PROJECT_DIR" "$REMOTE_DIR"

cd "$PROJECT_DIR"
git init
dvc init

# Настройка удалённого хранилища (локальная папка)
dvc remote add -d local_remote "../$REMOTE_DIR"

mkdir -p data

# Копируем скрипт
cp ../create_dataset.py .

echo ""
echo "=== Версия 1: базовый датасет ==="
python create_dataset.py --version 1
cp data/titanic_v1.csv data/titanic.csv
dvc add data/titanic.csv
git add data/titanic.csv.dvc data/.gitignore create_dataset.py .dvc .dvcignore
git commit -m "v1: базовый датасет Titanic"
git tag v1
dvc push

echo ""
echo "=== Версия 2: NaN заполнены средним ==="
python create_dataset.py --version 2
cp data/titanic_v2.csv data/titanic.csv
dvc add data/titanic.csv
git add data/titanic.csv.dvc
git commit -m "v2: NaN в Age заполнены средним"
git tag v2
dvc push

echo ""
echo "=== Версия 3: One-hot encoding ==="
python create_dataset.py --version 3
cp data/titanic_v3.csv data/titanic.csv
dvc add data/titanic.csv
git add data/titanic.csv.dvc
git commit -m "v3: One-hot encoding Sex"
git tag v3
dvc push

echo ""
echo "=== Демонстрация переключения ==="

echo "Текущая версия (v3):"
head -2 data/titanic.csv

echo ""
echo "Переключение на v1..."
git checkout v1 -- data/titanic.csv.dvc
dvc checkout
echo "Версия 1:"
head -2 data/titanic.csv

echo ""
echo "Переключение обратно на v3..."
git checkout v3 -- data/titanic.csv.dvc
dvc checkout
echo "Версия 3:"
head -2 data/titanic.csv

echo ""
echo "=== Готово! ==="
echo "Проект: $PROJECT_DIR/"
echo "Хранилище DVC: $REMOTE_DIR/"
echo ""
echo "Команды для переключения версий:"
echo "  git checkout v1 -- data/titanic.csv.dvc && dvc checkout"
echo "  git checkout v2 -- data/titanic.csv.dvc && dvc checkout"
echo "  git checkout v3 -- data/titanic.csv.dvc && dvc checkout"
