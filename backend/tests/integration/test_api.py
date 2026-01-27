"""Integration tests for the API endpoints."""

import pytest
from fastapi.testclient import TestClient

from guessme.api.app import create_app
from guessme.predictor.deployment import Predictor


@pytest.fixture
def client():
    """Create test client with real predictor."""
    predictor = Predictor()
    app = create_app(predictor)
    return TestClient(app)


def test_health_endpoint(client):
    """Health endpoint should return ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_endpoint(client):
    """Predict endpoint should return digit and confidence."""
    response = client.post(
        "/predict", json={"points": [{"x": 14, "y": 14}, {"x": 15, "y": 15}]}
    )

    assert response.status_code == 200
    data = response.json()
    assert "digit" in data
    assert "confidence" in data
    assert 0 <= data["digit"] <= 9
    assert 0 <= data["confidence"] <= 100


def test_predict_endpoint_empty_points(client):
    """Predict endpoint should handle empty points."""
    response = client.post("/predict", json={"points": []})

    assert response.status_code == 200
    data = response.json()
    assert "digit" in data


def test_predict_endpoint_invalid_request(client):
    """Predict endpoint should reject invalid request."""
    response = client.post("/predict", json={"invalid": "data"})
    assert response.status_code == 422  # Validation error
