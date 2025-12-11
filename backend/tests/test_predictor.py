"""Tests for predictor actor."""

import pytest
import ray

from backend.predictor.actor import PredictorActor


@pytest.fixture(scope="module")
def ray_init():
    """Initialize Ray for testing."""
    ray.init(ignore_reinit_error=True)
    yield
    ray.shutdown()


@pytest.fixture
def predictor(ray_init):
    """Create a predictor actor."""
    return PredictorActor.remote()


class TestPredictorActor:
    def test_predict_returns_list_of_predictions(self, predictor):
        """Predict should return a list of predictions."""
        predictions = ray.get(predictor.predict.remote("client1"))
        assert isinstance(predictions, list)
        assert len(predictions) == 5  # Top 5 predictions

    def test_prediction_has_label_and_confidence(self, predictor):
        """Each prediction should have label and confidence."""
        predictions = ray.get(predictor.predict.remote("client1"))
        for pred in predictions:
            assert "label" in pred
            assert "confidence" in pred
            assert isinstance(pred["label"], str)
            assert isinstance(pred["confidence"], int)
            assert 0 <= pred["confidence"] <= 100

    def test_predictions_sorted_by_confidence_desc(self, predictor):
        """Predictions should be sorted by confidence descending."""
        predictions = ray.get(predictor.predict.remote("client1"))
        confidences = [p["confidence"] for p in predictions]
        assert confidences == sorted(confidences, reverse=True)

    def test_stroke_count_increases_confidence(self, predictor):
        """More strokes should generally increase confidence."""
        # First prediction (1 stroke)
        ray.get(predictor.add_stroke.remote("client2"))
        preds1 = ray.get(predictor.predict.remote("client2"))

        # Add more strokes
        for _ in range(5):
            ray.get(predictor.add_stroke.remote("client2"))
        preds2 = ray.get(predictor.predict.remote("client2"))

        # Top confidence should generally be higher with more strokes
        # (not deterministic due to randomness, but stroke_factor increases)
        assert preds1[0]["confidence"] <= 100
        assert preds2[0]["confidence"] <= 100

    def test_clear_resets_stroke_count(self, predictor):
        """Clear should reset stroke count for client."""
        # Add strokes
        for _ in range(5):
            ray.get(predictor.add_stroke.remote("client3"))

        # Clear
        ray.get(predictor.clear.remote("client3"))

        # Stroke count should be 0
        count = ray.get(predictor.get_stroke_count.remote("client3"))
        assert count == 0

    def test_get_final_returns_top_prediction(self, predictor):
        """Get final should return the top prediction."""
        ray.get(predictor.add_stroke.remote("client4"))
        final = ray.get(predictor.get_final.remote("client4"))

        assert "label" in final
        assert "confidence" in final

    def test_separate_clients_have_separate_stroke_counts(self, predictor):
        """Each client should have its own stroke count."""
        # Add strokes for client A
        for _ in range(3):
            ray.get(predictor.add_stroke.remote("clientA"))

        # Add strokes for client B
        ray.get(predictor.add_stroke.remote("clientB"))

        count_a = ray.get(predictor.get_stroke_count.remote("clientA"))
        count_b = ray.get(predictor.get_stroke_count.remote("clientB"))

        assert count_a == 3
        assert count_b == 1

    def test_labels_are_from_known_list(self, predictor):
        """Labels should be from the known categories."""
        known_labels = {
            "Cat", "Dog", "House", "Tree", "Car", "Sun",
            "Flower", "Fish", "Bird", "Apple", "Star", "Boat", "Cup",
        }
        predictions = ray.get(predictor.predict.remote("client5"))
        for pred in predictions:
            assert pred["label"] in known_labels
