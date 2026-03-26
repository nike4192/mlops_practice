"""Flask-сервис для предсказаний на обученной модели Iris."""

import pickle
import json
import logging
import os
from datetime import datetime
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

MODEL = None
METADATA = None


def load_model():
    """Загрузка модели и метаданных."""
    global MODEL, METADATA

    model_path = 'models/iris_model.pkl'
    metadata_path = 'models/metadata.json'

    if not os.path.exists(model_path):
        logger.error(f"Файл модели не найден: {model_path}")
        return False

    with open(model_path, 'rb') as f:
        MODEL = pickle.load(f)
    logger.info("Модель загружена")

    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            METADATA = json.load(f)
    else:
        METADATA = {'model_name': 'Iris Classifier'}

    return True


@app.route('/health')
def health():
    return jsonify({
        'status': 'ready' if MODEL else 'loading',
        'model_loaded': MODEL is not None
    })


@app.route('/model/info')
def model_info():
    return jsonify(METADATA)


@app.route('/predict', methods=['POST'])
def predict():
    """Предсказание для одного примера."""
    data = request.get_json()
    if not data or 'features' not in data:
        return jsonify({'error': 'Нужно поле "features"'}), 400

    features = data['features']
    if not isinstance(features, list) or len(features) != 4:
        return jsonify({'error': 'features должен содержать 4 числа'}), 400

    try:
        features = [float(f) for f in features]
    except (ValueError, TypeError):
        return jsonify({'error': 'Все значения должны быть числами'}), 400

    prediction = MODEL.predict([features])[0]
    probabilities = MODEL.predict_proba([features])[0]
    class_names = METADATA.get('classes', ['setosa', 'versicolor', 'virginica'])

    return jsonify({
        'prediction': int(prediction),
        'predicted_class': class_names[prediction],
        'probabilities': {class_names[i]: float(p) for i, p in enumerate(probabilities)}
    })


@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    """Батч-предсказание."""
    data = request.get_json()
    if not data or 'batch' not in data:
        return jsonify({'error': 'Нужно поле "batch"'}), 400

    batch = data['batch']
    if not isinstance(batch, list) or len(batch) == 0:
        return jsonify({'error': 'batch должен быть непустым списком'}), 400

    processed = []
    for i, features in enumerate(batch):
        if not isinstance(features, list) or len(features) != 4:
            return jsonify({'error': f'Элемент {i}: нужно 4 числа'}), 400
        try:
            processed.append([float(f) for f in features])
        except (ValueError, TypeError):
            return jsonify({'error': f'Элемент {i}: нечисловые значения'}), 400

    predictions = MODEL.predict(processed)
    probabilities = MODEL.predict_proba(processed)
    class_names = METADATA.get('classes', ['setosa', 'versicolor', 'virginica'])

    results = []
    for i, (pred, probs) in enumerate(zip(predictions, probabilities)):
        results.append({
            'sample_id': i,
            'prediction': int(pred),
            'predicted_class': class_names[pred],
            'probabilities': {class_names[j]: float(p) for j, p in enumerate(probs)}
        })

    return jsonify({'batch_size': len(batch), 'results': results})


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Эндпоинт не найден'}), 404


if __name__ == '__main__':
    if load_model():
        app.run(host='0.0.0.0', port=5000)
    else:
        exit(1)
