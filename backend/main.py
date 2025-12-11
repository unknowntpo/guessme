"""Ray Serve deployment for Guessme backend."""

import ray
from ray import serve

from backend.websocket.handler import create_app


@serve.deployment
@serve.ingress(create_app())
class GuessmeApp:
    """Ray Serve deployment wrapping the FastAPI app."""

    pass


# Entry point for `serve run backend.main:app`
app = GuessmeApp.bind()
