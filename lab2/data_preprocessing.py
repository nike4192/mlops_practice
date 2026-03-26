"""Предобработка Titanic: заполнение пропусков, кодирование, разбиение на train/test."""

import argparse
import logging
import os
import sys

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


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


def handle_missing_values(df, logger):
    """Заполнение пропусков и удаление ненужных колонок."""
    # Заполняем пропуски
    if 'age' in df.columns:
        median = df['age'].median()
        df['age'] = df['age'].fillna(median)
        logger.info(f"age: пропуски заполнены медианой ({median:.1f})")

    if 'embarked' in df.columns:
        mode = df['embarked'].mode()[0]
        df['embarked'] = df['embarked'].fillna(mode)
        logger.info(f"embarked: пропуски заполнены модой ({mode})")

    if 'fare' in df.columns:
        median = df['fare'].median()
        df['fare'] = df['fare'].fillna(median)
        logger.info(f"fare: пропуски заполнены медианой ({median:.1f})")

    # Убираем колонки с большим количеством пропусков
    cols_to_drop = ['deck', 'embark_town']
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

    return df


def encode_categorical(df, logger):
    """Кодирование категориальных признаков через LabelEncoder."""
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    logger.info(f"Категориальные колонки: {list(cat_cols)}")

    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))

    return df


def main(args):
    logger = setup_logging(args.log_file)
    logger.info("Начало предобработки")

    df = pd.read_csv(args.input)
    logger.info(f"Загружено: {df.shape}")

    # Обработка пропусков
    df = handle_missing_values(df, logger)

    # Кодирование
    df = encode_categorical(df, logger)

    # Убираем target-leakage и дубли
    target = 'survived'
    cols_to_drop = ['who', 'adult_male', 'alone', 'alive', 'class']
    X = df.drop(columns=[target] + [c for c in cols_to_drop if c in df.columns])
    y = df[target]

    logger.info(f"Признаки: {list(X.columns)}")
    logger.info(f"Распределение таргета:\n{y.value_counts()}")

    # Разбиение
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    logger.info(f"Train: {len(X_train)}, Test: {len(X_test)}")

    # Сохранение
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)

    train_df.to_csv(args.output.replace('.csv', '_train.csv'), index=False)
    test_df.to_csv(args.output.replace('.csv', '_test.csv'), index=False)
    pd.concat([train_df, test_df]).to_csv(args.output, index=False)

    logger.info("Предобработка завершена")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/titanic_raw.csv")
    parser.add_argument("--output", default="data/titanic_processed.csv")
    parser.add_argument("--log_file", default="logs/preprocessing.log")
    args = parser.parse_args()
    sys.exit(main(args))
