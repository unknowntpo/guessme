"""WebSocket handler for the drawing game."""

import ray
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from backend.predictor.actor import PredictorActor
from backend.websocket.messages import (
    ClientMessage,
    Prediction,
    ServerFinalMessage,
    ServerPredictionsMessage,
)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="Guessme API")

    # Create predictor actor (shared across all connections)
    predictor = PredictorActor.remote()

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()

        try:
            while True:
                # Receive message from client
                data = await websocket.receive_json()
                message = ClientMessage.model_validate(data)

                if message.type == "stroke":
                    # Increment stroke count
                    ray.get(predictor.add_stroke.remote(message.client_id))

                    # Get predictions
                    predictions_data = ray.get(predictor.predict.remote(message.client_id))
                    predictions = [
                        Prediction(label=p["label"], confidence=p["confidence"])
                        for p in predictions_data
                    ]

                    # Send predictions response
                    response = ServerPredictionsMessage(
                        client_id=message.client_id,
                        data=predictions,
                    )
                    await websocket.send_json(response.model_dump(by_alias=True))

                elif message.type == "submit":
                    # Get final prediction
                    final_data = ray.get(predictor.get_final.remote(message.client_id))
                    final = Prediction(
                        label=final_data["label"],
                        confidence=final_data["confidence"],
                    )

                    # Send final response
                    response = ServerFinalMessage(
                        client_id=message.client_id,
                        data=final,
                    )
                    await websocket.send_json(response.model_dump(by_alias=True))

                elif message.type == "clear":
                    # Reset stroke count
                    ray.get(predictor.clear.remote(message.client_id))

                    # Send empty predictions
                    response = ServerPredictionsMessage(
                        client_id=message.client_id,
                        data=[],
                    )
                    await websocket.send_json(response.model_dump(by_alias=True))

        except WebSocketDisconnect:
            pass

    return app
