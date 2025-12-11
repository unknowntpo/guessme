"""Ray actor for prediction generation."""

import random

import ray


# Known labels for fake predictions (will be replaced by real ML model)
LABELS = [
    "Cat", "Dog", "House", "Tree", "Car", "Sun",
    "Flower", "Fish", "Bird", "Apple", "Star", "Boat", "Cup",
]


@ray.remote
class PredictorActor:
    """Ray actor that generates predictions for drawings.

    Currently generates fake random predictions.
    Will be replaced with real ML model inference later.
    """

    def __init__(self):
        self._stroke_counts: dict[str, int] = {}

    def add_stroke(self, client_id: str) -> None:
        """Increment stroke count for a client."""
        self._stroke_counts[client_id] = self._stroke_counts.get(client_id, 0) + 1

    def get_stroke_count(self, client_id: str) -> int:
        """Get current stroke count for a client."""
        return self._stroke_counts.get(client_id, 0)

    def clear(self, client_id: str) -> None:
        """Reset stroke count for a client."""
        self._stroke_counts[client_id] = 0

    def predict(self, client_id: str) -> list[dict]:
        """Generate predictions based on current stroke count.

        Returns top 5 predictions sorted by confidence descending.
        Confidence increases with stroke count (more strokes = more confident).
        """
        stroke_count = self._stroke_counts.get(client_id, 0)
        stroke_factor = min(stroke_count / 5, 1.0)  # Caps at 5 strokes

        # Generate predictions for random labels
        predictions = []
        used_labels = set()

        while len(predictions) < 5:
            label = random.choice(LABELS)
            if label in used_labels:
                continue
            used_labels.add(label)

            # Confidence formula matching mock-server:
            # Math.round(Math.random() * 60 * strokeFactor + Math.random() * 20)
            confidence = round(random.random() * 60 * stroke_factor + random.random() * 20)
            confidence = min(confidence, 100)  # Cap at 100

            predictions.append({"label": label, "confidence": confidence})

        # Sort by confidence descending
        predictions.sort(key=lambda p: p["confidence"], reverse=True)
        return predictions

    def get_final(self, client_id: str) -> dict:
        """Get the final (top) prediction for a client."""
        predictions = self.predict(client_id)
        return predictions[0] if predictions else {"label": "Unknown", "confidence": 0}
