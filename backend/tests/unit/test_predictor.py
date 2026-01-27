"""Unit tests for Predictor."""

import pytest

from guessme.predictor.deployment import Predictor


@pytest.fixture
def predictor():
    """Create a predictor instance."""
    return Predictor()


def test_predictor_init(predictor):
    """Predictor should load model and weights."""
    assert predictor.model is not None
    assert predictor.device is not None


def test_predictor_predict_returns_dict(predictor):
    """Predict should return dict with digit and confidence."""
    points = [{"x": 14, "y": 14}, {"x": 15, "y": 15}]
    result = predictor.predict(points)

    assert "digit" in result
    assert "confidence" in result
    assert isinstance(result["digit"], int)
    assert isinstance(result["confidence"], int)
    assert 0 <= result["digit"] <= 9
    assert 0 <= result["confidence"] <= 100


def test_predictor_predict_empty_points(predictor):
    """Predict should handle empty points list."""
    result = predictor.predict([])

    assert "digit" in result
    assert "confidence" in result
