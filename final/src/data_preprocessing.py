"""
Предобработка данных: нормализация, разделение на train/test.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path

FEATURE_COLS = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo",
]
TARGET_COL = "genre"
TEST_SIZE = 0.2
SEED = 42


def preprocess(input_path: Path, output_dir: Path):
    df = pd.read_csv(input_path)

    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=SEED, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train), columns=FEATURE_COLS, index=X_train.index
    )
    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test), columns=FEATURE_COLS, index=X_test.index
    )

    output_dir.mkdir(exist_ok=True)
    X_train_scaled.assign(genre=y_train).to_csv(output_dir / "train.csv", index=False)
    X_test_scaled.assign(genre=y_test).to_csv(output_dir / "test.csv", index=False)

    models_dir = Path(__file__).parent.parent / "models"
    models_dir.mkdir(exist_ok=True)
    joblib.dump(scaler, models_dir / "scaler.pkl")

    print(f"Train: {len(X_train_scaled)}, Test: {len(X_test_scaled)}")
    print(f"Scaler сохранён: {models_dir / 'scaler.pkl'}")


def main():
    base = Path(__file__).parent.parent
    preprocess(base / "data" / "tracks.csv", base / "data")


if __name__ == "__main__":
    main()
