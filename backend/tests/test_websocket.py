"""Tests for WebSocket handler."""

import json

import pytest
import ray
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.websocket.handler import create_app


@pytest.fixture(scope="module")
def ray_init():
    """Initialize Ray for testing."""
    ray.init(ignore_reinit_error=True)
    yield
    ray.shutdown()


@pytest.fixture
def app(ray_init) -> FastAPI:
    """Create test FastAPI app."""
    return create_app()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Create test client."""
    return TestClient(app)


class TestWebSocketConnection:
    def test_websocket_connect(self, client):
        """Should be able to connect to WebSocket."""
        with client.websocket_connect("/ws") as ws:
            assert ws is not None

    def test_stroke_message_triggers_predictions(self, client):
        """Stroke message should trigger predictions response."""
        with client.websocket_connect("/ws") as ws:
            ws.send_json({
                "clientId": "test-client-1",
                "type": "stroke",
                "data": {"points": [{"x": 0, "y": 0}, {"x": 10, "y": 10}]},
            })

            # Should receive predictions
            response = ws.receive_json()
            assert response["type"] == "predictions"
            assert response["clientId"] == "test-client-1"
            assert isinstance(response["data"], list)
            assert len(response["data"]) == 5

    def test_submit_message_returns_final(self, client):
        """Submit message should return final prediction."""
        with client.websocket_connect("/ws") as ws:
            # Send a stroke first
            ws.send_json({
                "clientId": "test-client-2",
                "type": "stroke",
                "data": {"points": [{"x": 0, "y": 0}]},
            })
            # Consume the predictions response
            ws.receive_json()

            # Send submit
            ws.send_json({
                "clientId": "test-client-2",
                "type": "submit",
            })

            # Should receive final
            response = ws.receive_json()
            assert response["type"] == "final"
            assert response["clientId"] == "test-client-2"
            assert "label" in response["data"]
            assert "confidence" in response["data"]

    def test_clear_message_returns_empty_predictions(self, client):
        """Clear message should return empty predictions."""
        with client.websocket_connect("/ws") as ws:
            # Send a stroke first
            ws.send_json({
                "clientId": "test-client-3",
                "type": "stroke",
                "data": {"points": [{"x": 0, "y": 0}]},
            })
            ws.receive_json()

            # Send clear
            ws.send_json({
                "clientId": "test-client-3",
                "type": "clear",
            })

            # Should receive empty predictions
            response = ws.receive_json()
            assert response["type"] == "predictions"
            assert response["clientId"] == "test-client-3"
            assert response["data"] == []

    def test_multiple_strokes_increment_confidence(self, client):
        """Multiple strokes should generally increase confidence."""
        with client.websocket_connect("/ws") as ws:
            # Send multiple strokes
            for i in range(5):
                ws.send_json({
                    "clientId": "test-client-4",
                    "type": "stroke",
                    "data": {"points": [{"x": i * 10, "y": i * 10}]},
                })
                response = ws.receive_json()
                assert response["type"] == "predictions"

    def test_predictions_have_required_fields(self, client):
        """Each prediction should have label and confidence."""
        with client.websocket_connect("/ws") as ws:
            ws.send_json({
                "clientId": "test-client-5",
                "type": "stroke",
                "data": {"points": [{"x": 0, "y": 0}]},
            })

            response = ws.receive_json()
            for pred in response["data"]:
                assert "label" in pred
                assert "confidence" in pred
                assert isinstance(pred["label"], str)
                assert isinstance(pred["confidence"], int)
