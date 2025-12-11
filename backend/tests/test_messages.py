"""Tests for WebSocket message models."""

import pytest
from backend.websocket.messages import (
    Point,
    Prediction,
    ClientMessage,
    ServerPredictionsMessage,
    ServerFinalMessage,
)


class TestPoint:
    def test_create_point(self):
        point = Point(x=10, y=20)
        assert point.x == 10
        assert point.y == 20

    def test_point_from_dict(self):
        point = Point.model_validate({"x": 5.5, "y": 10.5})
        assert point.x == 5.5
        assert point.y == 10.5


class TestPrediction:
    def test_create_prediction(self):
        pred = Prediction(label="Cat", confidence=87)
        assert pred.label == "Cat"
        assert pred.confidence == 87

    def test_prediction_from_dict(self):
        pred = Prediction.model_validate({"label": "Dog", "confidence": 92})
        assert pred.label == "Dog"
        assert pred.confidence == 92


class TestClientMessage:
    def test_stroke_message(self):
        msg = ClientMessage.model_validate({
            "clientId": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
            "type": "stroke",
            "data": {"points": [{"x": 0, "y": 0}, {"x": 10, "y": 10}]},
        })
        assert msg.client_id == "01ARZ3NDEKTSV4RRFFQ69G5FAV"
        assert msg.type == "stroke"
        assert msg.data is not None
        assert len(msg.data.points) == 2
        assert msg.data.points[0].x == 0

    def test_submit_message(self):
        msg = ClientMessage.model_validate({
            "clientId": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
            "type": "submit",
        })
        assert msg.type == "submit"
        assert msg.data is None

    def test_clear_message(self):
        msg = ClientMessage.model_validate({
            "clientId": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
            "type": "clear",
        })
        assert msg.type == "clear"
        assert msg.data is None

    def test_invalid_type_raises(self):
        with pytest.raises(ValueError):
            ClientMessage.model_validate({
                "clientId": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
                "type": "invalid",
            })


class TestServerPredictionsMessage:
    def test_create_predictions_message(self):
        msg = ServerPredictionsMessage(
            client_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            data=[
                Prediction(label="Cat", confidence=87),
                Prediction(label="Dog", confidence=65),
            ],
        )
        assert msg.type == "predictions"
        assert len(msg.data) == 2
        assert msg.data[0].label == "Cat"

    def test_serialize_predictions_message(self):
        msg = ServerPredictionsMessage(
            client_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            data=[Prediction(label="Cat", confidence=87)],
        )
        json_dict = msg.model_dump(by_alias=True)
        assert json_dict["clientId"] == "01ARZ3NDEKTSV4RRFFQ69G5FAV"
        assert json_dict["type"] == "predictions"
        assert json_dict["data"][0]["label"] == "Cat"


class TestServerFinalMessage:
    def test_create_final_message(self):
        msg = ServerFinalMessage(
            client_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            data=Prediction(label="Cat", confidence=87),
        )
        assert msg.type == "final"
        assert msg.data.label == "Cat"

    def test_serialize_final_message(self):
        msg = ServerFinalMessage(
            client_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            data=Prediction(label="Dog", confidence=92),
        )
        json_dict = msg.model_dump(by_alias=True)
        assert json_dict["clientId"] == "01ARZ3NDEKTSV4RRFFQ69G5FAV"
        assert json_dict["type"] == "final"
        assert json_dict["data"]["label"] == "Dog"
