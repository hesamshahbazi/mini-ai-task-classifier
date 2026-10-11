from fastapi.testclient import TestClient
from ml_classifier import MLTaskClassifier
from api import app


def test_paths_and_persistence(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = tmp_path / "test-model.pkl"
    first = MLTaskClassifier(path)
    assert first.predict("refund request") == "Support"
    assert MLTaskClassifier(path).predict("refund request") == "Support"


def test_api_validation():
    with TestClient(app) as client:
        assert client.get("/health").status_code == 200
        assert client.post("/predict", json={"text":"refund request"}).json()["category"] == "Support"
        for text in ["", "   ", "x" * 10001]:
            assert client.post("/predict", json={"text":text}).status_code == 422
