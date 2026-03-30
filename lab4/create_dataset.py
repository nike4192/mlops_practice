"""
Lab 4: Создание и версионирование датасета Titanic с помощью DVC.

Скрипт создаёт 3 версии датасета:
  v1 — базовый (Pclass, Sex, Age)
  v2 — NaN в Age заполнены средним
  v3 — One-hot encoding для Sex
"""

import argparse
import pandas as pd
import numpy as np


def load_titanic() -> pd.DataFrame:
    """Загружает Titanic из seaborn."""
    import seaborn as sns
    df = sns.load_dataset("titanic")
    # seaborn titanic: колонки в lowercase
    return df[["pclass", "sex", "age"]].copy()


def create_v1(df: pd.DataFrame, output: str = "data/titanic_v1.csv"):
    """Версия 1: базовый датасет (pclass, sex, age) — с NaN."""
    df.to_csv(output, index=False)
    nan_count = df["age"].isna().sum()
    print(f"[v1] Сохранён: {output}")
    print(f"     Строк: {len(df)}, NaN в Age: {nan_count}")
    return df


def create_v2(df: pd.DataFrame, output: str = "data/titanic_v2.csv"):
    """Версия 2: NaN в Age заполнены средним значением."""
    df = df.copy()
    mean_age = df["age"].mean()
    df["age"] = df["age"].fillna(mean_age)
    df.to_csv(output, index=False)
    print(f"[v2] Сохранён: {output}")
    print(f"     NaN заполнены средним age={mean_age:.2f}")
    return df


def create_v3(df: pd.DataFrame, output: str = "data/titanic_v3.csv"):
    """Версия 3: One-hot encoding для Sex."""
    df = df.copy()
    df = pd.get_dummies(df, columns=["sex"], prefix="sex", dtype=int)
    df.to_csv(output, index=False)
    print(f"[v3] Сохранён: {output}")
    print(f"     Колонки: {list(df.columns)}")
    return df


def main():
    parser = argparse.ArgumentParser(description="Создание версий датасета Titanic")
    parser.add_argument(
        "--version", "-v",
        choices=["1", "2", "3", "all"],
        default="all",
        help="Какую версию создать (1, 2, 3 или all)",
    )
    args = parser.parse_args()

    import os
    os.makedirs("data", exist_ok=True)

    df = load_titanic()
    print(f"Загружен Titanic: {len(df)} строк\n")

    if args.version in ("1", "all"):
        v1 = create_v1(df)
    if args.version in ("2", "all"):
        v2 = create_v2(df)
    if args.version in ("3", "all"):
        v3 = create_v3(df)

    print("\nГотово!")


if __name__ == "__main__":
    main()
