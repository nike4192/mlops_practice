"""
Генерация синтетического датасета музыкальных жанров.

Создаёт датасет с аудио-характеристиками треков (аналогичными Spotify Audio Features)
для 6 жанров: rock, pop, hip-hop, classical, electronic, jazz.
"""

import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
SAMPLES_PER_GENRE = 500

# Аудио-фичи и их распределения по жанрам (mean, std)
# Основано на реальных распределениях Spotify Audio Features
GENRE_PROFILES = {
    "rock": {
        "danceability": (0.52, 0.12),
        "energy": (0.75, 0.15),
        "loudness": (-7.0, 3.0),
        "speechiness": (0.05, 0.03),
        "acousticness": (0.15, 0.15),
        "instrumentalness": (0.10, 0.15),
        "liveness": (0.18, 0.12),
        "valence": (0.50, 0.20),
        "tempo": (125.0, 20.0),
    },
    "pop": {
        "danceability": (0.68, 0.12),
        "energy": (0.65, 0.15),
        "loudness": (-6.0, 2.5),
        "speechiness": (0.07, 0.05),
        "acousticness": (0.20, 0.18),
        "instrumentalness": (0.02, 0.05),
        "liveness": (0.15, 0.10),
        "valence": (0.55, 0.22),
        "tempo": (118.0, 22.0),
    },
    "hip-hop": {
        "danceability": (0.75, 0.10),
        "energy": (0.65, 0.15),
        "loudness": (-6.5, 2.5),
        "speechiness": (0.18, 0.10),
        "acousticness": (0.12, 0.12),
        "instrumentalness": (0.01, 0.03),
        "liveness": (0.16, 0.10),
        "valence": (0.50, 0.20),
        "tempo": (105.0, 30.0),
    },
    "classical": {
        "danceability": (0.30, 0.12),
        "energy": (0.25, 0.18),
        "loudness": (-18.0, 6.0),
        "speechiness": (0.04, 0.02),
        "acousticness": (0.90, 0.10),
        "instrumentalness": (0.80, 0.20),
        "liveness": (0.12, 0.08),
        "valence": (0.30, 0.18),
        "tempo": (100.0, 35.0),
    },
    "electronic": {
        "danceability": (0.72, 0.12),
        "energy": (0.80, 0.12),
        "loudness": (-5.5, 2.5),
        "speechiness": (0.06, 0.04),
        "acousticness": (0.05, 0.08),
        "instrumentalness": (0.50, 0.30),
        "liveness": (0.14, 0.10),
        "valence": (0.40, 0.22),
        "tempo": (128.0, 15.0),
    },
    "jazz": {
        "danceability": (0.52, 0.15),
        "energy": (0.40, 0.20),
        "loudness": (-12.0, 5.0),
        "speechiness": (0.05, 0.03),
        "acousticness": (0.65, 0.25),
        "instrumentalness": (0.35, 0.30),
        "liveness": (0.20, 0.15),
        "valence": (0.50, 0.22),
        "tempo": (115.0, 30.0),
    },
}

FEATURE_BOUNDS = {
    "danceability": (0.0, 1.0),
    "energy": (0.0, 1.0),
    "loudness": (-60.0, 0.0),
    "speechiness": (0.0, 1.0),
    "acousticness": (0.0, 1.0),
    "instrumentalness": (0.0, 1.0),
    "liveness": (0.0, 1.0),
    "valence": (0.0, 1.0),
    "tempo": (40.0, 220.0),
}


def generate_dataset(
    samples_per_genre: int = SAMPLES_PER_GENRE, seed: int = SEED
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    for genre, features in GENRE_PROFILES.items():
        for _ in range(samples_per_genre):
            row = {"genre": genre}
            for feat, (mean, std) in features.items():
                lo, hi = FEATURE_BOUNDS[feat]
                value = rng.normal(mean, std)
                row[feat] = np.clip(value, lo, hi)
            rows.append(row)

    df = pd.DataFrame(rows)
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)


def main():
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)

    df = generate_dataset()
    output_path = data_dir / "tracks.csv"
    df.to_csv(output_path, index=False)
    print(f"Датасет создан: {output_path} ({len(df)} треков, {df['genre'].nunique()} жанров)")
    print(df["genre"].value_counts().to_string())


if __name__ == "__main__":
    main()
