"""
Обучение модели классификации музыкальных жанров.
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
from pathlib import Path

FEATURE_COLS = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo",
]
TARGET_COL = "genre"
SEED = 42


def train_model(train_path: Path, test_path: Path, model_dir: Path):
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    X_train = train_df[FEATURE_COLS]
    y_train = train_df[TARGET_COL]
    X_test = test_df[FEATURE_COLS]
    y_test = test_df[TARGET_COL]

    model = RandomForestClassifier(
        n_estimators=100, max_depth=10, random_state=SEED, n_jobs=-1
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    model_dir.mkdir(exist_ok=True)
    model_path = model_dir / "genre_classifier.pkl"
    joblib.dump(model, model_path)
    print(f"Модель сохранена: {model_path}")


def main():
    base = Path(__file__).parent.parent
    train_model(
        base / "data" / "train.csv",
        base / "data" / "test.csv",
        base / "models",
    )


if __name__ == "__main__":
    main()
