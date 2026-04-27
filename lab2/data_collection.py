"""Загрузка датасета Titanic из seaborn и сохранение в CSV."""

import argparse
import logging
import os
import sys

import pandas as pd


def setup_logging(log_file):
    """Настройка логирования в файл и консоль."""
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
    logger.info("Начало сбора данных")

    try:
        import seaborn as sns
        df = sns.load_dataset('titanic')
        logger.info(f"Датасет загружен: {df.shape}")

        # Проверка
        if df.empty:
            raise ValueError("Датасет пустой!")

        logger.info(f"Колонки: {list(df.columns)}")
        logger.info(f"Пропуски:\n{df.isnull().sum()}")

        # Сохранение
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        df.to_csv(args.output, index=False)
        logger.info(f"Сохранено: {args.output}")

    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/titanic_raw.csv")
    parser.add_argument("--log_file", default="logs/data_collection.log")
    args = parser.parse_args()
    sys.exit(main(args))
