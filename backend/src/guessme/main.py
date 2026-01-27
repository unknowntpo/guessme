"""Ray Serve entry point for Guessme backend."""

from ray import serve

from guessme.api.app import create_app
from guessme.predictor.deployment import Predictor


@serve.deployment
@serve.ingress(create_app(Predictor()))
class GuessmeApp:
    """Ray Serve deployment wrapping the FastAPI app."""

    pass


# Entry point for `serve run guessme.main:app`
app = GuessmeApp.bind()
