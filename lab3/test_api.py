"""Тесты для Flask API (запускать при работающем сервере)."""

import requests
import sys
import time

BASE_URL = "http://localhost:5000"


def test_health():
    r = requests.get(f"{BASE_URL}/health", timeout=5)
    assert r.status_code == 200
    assert r.json()['status'] == 'ready'
    print("[OK] Health check")


def test_model_info():
    r = requests.get(f"{BASE_URL}/model/info", timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert 'model_name' in data
    print(f"[OK] Model info: {data['model_name']}")


def test_predict(features, expected_class):
    r = requests.post(f"{BASE_URL}/predict", json={"features": features}, timeout=5)
    assert r.status_code == 200
    predicted = r.json()['predicted_class']
    status = "OK" if predicted == expected_class else "FAIL"
    print(f"[{status}] Predict {expected_class}: got {predicted}")


def test_batch():
    payload = {"batch": [[5.1, 3.5, 1.4, 0.2], [7.0, 3.2, 4.7, 1.4], [6.3, 3.3, 6.0, 2.5]]}
    r = requests.post(f"{BASE_URL}/predict/batch", json=payload, timeout=5)
    assert r.status_code == 200
    assert r.json()['batch_size'] == 3
    print("[OK] Batch prediction")


def test_invalid_input():
    r = requests.post(f"{BASE_URL}/predict", json={}, timeout=5)
    assert r.status_code == 400
    r = requests.post(f"{BASE_URL}/predict", json={"features": [1.0, 2.0]}, timeout=5)
    assert r.status_code == 400
    print("[OK] Invalid input handling")


def main():
    print(f"\nТестирование API: {BASE_URL}\n")

    # Ждём запуска сервера
    for i in range(10):
        try:
            requests.get(f"{BASE_URL}/health", timeout=2)
            break
        except requests.exceptions.ConnectionError:
            print(f"Ожидание сервера... ({i+1}/10)")
            time.sleep(2)
    else:
        print("Сервер не отвечает!")
        return 1

    test_health()
    test_model_info()
    test_predict([5.1, 3.5, 1.4, 0.2], "setosa")
    test_predict([7.0, 3.2, 4.7, 1.4], "versicolor")
    test_predict([6.3, 3.3, 6.0, 2.5], "virginica")
    test_batch()
    test_invalid_input()

    print("\nВсе тесты пройдены!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
