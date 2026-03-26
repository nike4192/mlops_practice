"""Оценка модели на тестовых данных и генерация отчёта."""

import argparse
import logging
import os
import sys
import pickle

import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, classification_report
)


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
    logger.info("Начало тестирования модели")

    # Загрузка данных
    test_path = args.data.replace('.csv', '_test.csv')
    test_df = pd.read_csv(test_path)

    target = 'survived'
    X_test = test_df.drop(columns=[target])
    y_test = test_df[target]

    # Загрузка модели и скейлера
    with open(args.model, 'rb') as f:
        model = pickle.load(f)
    with open(args.scaler, 'rb') as f:
        scaler = pickle.load(f)

    logger.info(f"Тестовая выборка: {X_test.shape}")

    # Предсказание
    X_test_scaled = scaler.transform(X_test)
    y_pred = model.predict(X_test_scaled)
    y_proba = model.predict_proba(X_test_scaled)[:, 1]

    # Метрики
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc = roc_auc_score(y_test, y_proba)

    logger.info(f"Accuracy:  {acc:.4f}")
    logger.info(f"Precision: {prec:.4f}")
    logger.info(f"Recall:    {rec:.4f}")
    logger.info(f"F1 Score:  {f1:.4f}")
    logger.info(f"ROC AUC:   {roc:.4f}")

    # Отчёт
    report_dir = os.path.dirname(args.report_output)
    if report_dir and not os.path.exists(report_dir):
        os.makedirs(report_dir)

    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=['Не выжил', 'Выжил'])

    with open(args.report_output, 'w') as f:
        f.write("Отчёт оценки модели\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Accuracy:  {acc:.4f}\n")
        f.write(f"Precision: {prec:.4f}\n")
        f.write(f"Recall:    {rec:.4f}\n")
        f.write(f"F1 Score:  {f1:.4f}\n")
        f.write(f"ROC AUC:   {roc:.4f}\n\n")
        f.write(f"Матрица ошибок:\n{cm}\n\n")
        f.write(f"Подробный отчёт:\n{report}\n")

    logger.info(f"Отчёт сохранён: {args.report_output}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/titanic_processed.csv")
    parser.add_argument("--model", default="models/titanic_model.pkl")
    parser.add_argument("--scaler", default="models/scaler.pkl")
    parser.add_argument("--report_output", default="logs/evaluation_report.txt")
    parser.add_argument("--log_file", default="logs/testing.log")
    args = parser.parse_args()
    sys.exit(main(args))
