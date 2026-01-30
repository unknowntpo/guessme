"""FastAPI application for MNIST prediction."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from guessme.api.schemas import PredictRequest, PredictResponse
from guessme.predictor.deployment import Predictor


def create_app(predictor: Predictor) -> FastAPI:
    """Create FastAPI app with predictor dependency.

    Args:
        predictor: The Ray Serve predictor deployment

    Returns:
        Configured FastAPI app
    """
    app = FastAPI(
        title="Guessme API", description="MNIST digit prediction API", version="0.1.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    async def health() -> dict:
        """Health check endpoint."""
        return {"status": "ok"}

    @app.post("/predict", response_model=PredictResponse)
    async def predict(request: PredictRequest) -> PredictResponse:
        """Predict digit from canvas points.

        Args:
            request: Canvas points

        Returns:
            Predicted digit and confidence
        """
        points = [{"x": p.x, "y": p.y} for p in request.points]
        result = predictor.predict(points)
        return PredictResponse(**result)

    return app
