"""Pydantic schemas for API requests and responses."""

from pydantic import BaseModel


class Point(BaseModel):
    """A point from the canvas."""

    x: float
    y: float


class PredictRequest(BaseModel):
    """Request body for /predict endpoint."""

    points: list[Point]


class PredictResponse(BaseModel):
    """Response body for /predict endpoint."""

    digit: int
    confidence: int  # 0-100
