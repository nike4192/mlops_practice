"""Обучение моделей (LogisticRegression, RandomForest) и выбор лучшей."""

import argparse
import logging
import os
import sys
import pickle

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def setup_logging(log_file):
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


def main(args):
    logger = setup_logging(args.log_file)
    logger.info("Начало обучения")

    # Загрузка данных
    input_path = args.input
    train_path = input_path.replace('.csv', '_train.csv')
    test_path = input_path.replace('.csv', '_test.csv')

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    target = 'survived'
    X_train = train_df.drop(columns=[target])
    y_train = train_df[target]
    X_test = test_df.drop(columns=[target])
    y_test = test_df[target]

    logger.info(f"Train: {X_train.shape}, Test: {X_test.shape}")

    # Масштабирование
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Обучение нескольких моделей
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
    }

    best_model = None
    best_name = None
    best_acc = 0

    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        acc = accuracy_score(y_test, model.predict(X_test_scaled))
        logger.info(f"{name}: accuracy = {acc:.4f}")

        if acc > best_acc:
            best_acc = acc
            best_model = model
            best_name = name

    logger.info(f"Лучшая модель: {best_name} ({best_acc:.4f})")

    # Сохранение
    for path in [args.model_output, args.scaler_output]:
        d = os.path.dirname(path)
        if d and not os.path.exists(d):
            os.makedirs(d)

    with open(args.model_output, 'wb') as f:
        pickle.dump(best_model, f)
    with open(args.scaler_output, 'wb') as f:
        pickle.dump(scaler, f)

    logger.info(f"Модель сохранена: {args.model_output}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/titanic_processed.csv")
    parser.add_argument("--model_output", default="models/titanic_model.pkl")
    parser.add_argument("--scaler_output", default="models/scaler.pkl")
    parser.add_argument("--log_file", default="logs/training.log")
    args = parser.parse_args()
    sys.exit(main(args))
