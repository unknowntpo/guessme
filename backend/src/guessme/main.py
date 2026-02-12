"""FastAPI entry point for Guessme backend."""

from guessme.api.app import create_app
from guessme.predictor.deployment import Predictor

app = create_app(Predictor())
