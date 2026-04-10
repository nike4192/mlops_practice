"""
Flask API для классификации музыкальных жанров.
"""

import numpy as np
import joblib
from flask import Flask, jsonify, request
from pathlib import Path

FEATURE_COLS = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo",
]

app = Flask(__name__)

models_dir = Path(__file__).parent.parent / "models"
model = joblib.load(models_dir / "genre_classifier.pkl")
scaler = joblib.load(models_dir / "scaler.pkl")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    missing = [f for f in FEATURE_COLS if f not in data]
    if missing:
        return jsonify({"error": f"Missing features: {missing}"}), 400

    features = np.array([[data[f] for f in FEATURE_COLS]])
    features_scaled = scaler.transform(features)
    genre = model.predict(features_scaled)[0]
    probabilities = dict(zip(model.classes_, model.predict_proba(features_scaled)[0]))

    return jsonify({
        "genre": genre,
        "probabilities": {k: round(float(v), 4) for k, v in probabilities.items()},
    })


@app.route("/batch-predict", methods=["POST"])
def batch_predict():
    data = request.get_json()
    if not data or "tracks" not in data:
        return jsonify({"error": "JSON body with 'tracks' array required"}), 400

    results = []
    for track in data["tracks"]:
        missing = [f for f in FEATURE_COLS if f not in track]
        if missing:
            results.append({"error": f"Missing features: {missing}"})
            continue
        features = np.array([[track[f] for f in FEATURE_COLS]])
        features_scaled = scaler.transform(features)
        genre = model.predict(features_scaled)[0]
        results.append({"genre": genre})

    return jsonify({"predictions": results})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
