"""Тесты качества данных."""

import pandas as pd
import pytest
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

EXPECTED_FEATURES = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo",
]
EXPECTED_GENRES = {"rock", "pop", "hip-hop", "classical", "electronic", "jazz"}

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


@pytest.fixture
def tracks_df():
    return pd.read_csv(DATA_DIR / "tracks.csv")


@pytest.fixture
def train_df():
    return pd.read_csv(DATA_DIR / "train.csv")


@pytest.fixture
def test_df():
    return pd.read_csv(DATA_DIR / "test.csv")


def test_tracks_schema(tracks_df):
    expected_cols = set(EXPECTED_FEATURES + ["genre"])
    assert set(tracks_df.columns) == expected_cols


def test_no_missing_values(tracks_df):
    assert tracks_df.isnull().sum().sum() == 0


def test_no_duplicates(tracks_df):
    assert tracks_df.duplicated().sum() == 0


def test_genre_labels(tracks_df):
    assert set(tracks_df["genre"].unique()) == EXPECTED_GENRES


def test_feature_ranges(tracks_df):
    for feat, (lo, hi) in FEATURE_BOUNDS.items():
        assert tracks_df[feat].min() >= lo, f"{feat} below {lo}"
        assert tracks_df[feat].max() <= hi, f"{feat} above {hi}"


def test_class_balance(tracks_df):
    counts = tracks_df["genre"].value_counts()
    ratio = counts.max() / counts.min()
    assert ratio < 2.0, f"Class imbalance ratio {ratio:.2f} > 2.0"


def test_train_test_sizes(train_df, test_df):
    total = len(train_df) + len(test_df)
    test_ratio = len(test_df) / total
    assert 0.15 < test_ratio < 0.25, f"Test ratio {test_ratio:.2f} out of range"


def test_train_test_no_overlap(train_df, test_df):
    """Проверка что train и test не пересекаются (по набору фичей)."""
    train_set = set(train_df[EXPECTED_FEATURES].apply(tuple, axis=1))
    test_set = set(test_df[EXPECTED_FEATURES].apply(tuple, axis=1))
    overlap = train_set & test_set
    assert len(overlap) == 0, f"{len(overlap)} overlapping samples"
