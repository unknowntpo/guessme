"""Pydantic models for WebSocket messages."""

from typing import Literal

from pydantic import BaseModel, Field


class Point(BaseModel):
    """A point in the drawing canvas."""

    x: float
    y: float


class Prediction(BaseModel):
    """A prediction result with label and confidence."""

    label: str
    confidence: int  # 0-100


class StrokeData(BaseModel):
    """Data for a stroke message."""

    points: list[Point]


class ClientMessage(BaseModel):
    """Message from client to server."""

    client_id: str = Field(alias="clientId")
    type: Literal["stroke", "submit", "clear"]
    data: StrokeData | None = None

    model_config = {"populate_by_name": True}


class ServerPredictionsMessage(BaseModel):
    """Server message with prediction list."""

    client_id: str = Field(alias="clientId")
    type: Literal["predictions"] = "predictions"
    data: list[Prediction]

    model_config = {"populate_by_name": True}


class ServerFinalMessage(BaseModel):
    """Server message with final result."""

    client_id: str = Field(alias="clientId")
    type: Literal["final"] = "final"
    data: Prediction

    model_config = {"populate_by_name": True}
