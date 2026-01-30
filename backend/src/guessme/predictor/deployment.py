"""Ray Serve deployment for MNIST prediction with MLflow tracing."""

from pathlib import Path

import mlflow
import torch
import torch.nn.functional as F
from ray import serve

from guessme.model.cnn import MNISTNet
from guessme.model.preprocess import canvas_to_tensor, tensor_to_ascii

# Configure MLflow
_backend_dir = Path(__file__).resolve().parent.parent.parent.parent
mlflow.set_tracking_uri(f"sqlite:///{_backend_dir / 'mlflow.db'}")
mlflow.set_experiment("mnist-inference")


class Predictor:
    """Core predictor logic - testable without Ray Serve."""

    def __init__(self, weights_path: Path | None = None) -> None:
        """Load the trained model.

        Args:
            weights_path: Path to model weights. If None, uses default path.
        """
        # Device selection
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")

        # Load model
        self.model = MNISTNet().to(self.device)

        # Load weights
        if weights_path is None:
            weights_path = (
                Path(__file__).parent.parent / "model" / "weights" / "mnist_cnn.pt"
            )

        if weights_path.exists():
            self.model.load_state_dict(
                torch.load(weights_path, map_location=self.device, weights_only=True)
            )
            print(f"Loaded weights from {weights_path}")
        else:
            print(f"Warning: No weights found at {weights_path}, using random weights")

        self.model.eval()

    @mlflow.trace(name="predict", span_type="CHAIN")
    def predict(self, points: list[dict]) -> dict:
        """Predict digit from canvas points.

        Args:
            points: List of {"x": float, "y": float} from canvas

        Returns:
            {"digit": int, "confidence": int}
        """
        # Preprocess (traced)
        tensor = self._preprocess(points)

        # Inference (traced)
        result = self._inference(tensor)

        return result

    @mlflow.trace(name="preprocess", span_type="PARSER")
    def _preprocess(self, points: list[dict]) -> torch.Tensor:
        """Preprocess canvas points to tensor."""
        tensor = canvas_to_tensor(points)

        # Log ASCII visualization to trace for debugging
        ascii_art = tensor_to_ascii(tensor)
        span = mlflow.get_current_active_span()
        if span:
            span.set_attribute("input_ascii", ascii_art)

        # Normalize like MNIST (mean=0.1307, std=0.3081)
        tensor = (tensor - 0.1307) / 0.3081

        # Add batch dimension: (1, 28, 28) -> (1, 1, 28, 28)
        tensor = tensor.unsqueeze(0).to(self.device)

        return tensor

    @mlflow.trace(name="inference", span_type="LLM")
    def _inference(self, tensor: torch.Tensor) -> dict:
        """Run model inference."""
        with torch.no_grad():
            logits = self.model(tensor)
            probs = F.softmax(logits, dim=1)
            confidence, digit = torch.max(probs, dim=1)

        return {"digit": digit.item(), "confidence": int(confidence.item() * 100)}


@serve.deployment
class PredictorDeployment(Predictor):
    """Ray Serve deployment wrapper."""

    pass
