"""
FastAPI endpoint for model inference.
"""


import asyncio
import time
import logging
import logging.config
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import uvicorn

try:
    from logger.logger_config import LOGGING_CONFIG
    from src.predict import ModelPredictor
    from src.pydantic_models import PredictionInput, PredictionResponse
except ImportError:
    from mloptiflow.templates.demo_tabular_classification.logger.logger_config import (
        LOGGING_CONFIG,
    )
    from mloptiflow.templates.demo_tabular_classification.src.predict import (
        ModelPredictor,
    )
    from mloptiflow.templates.demo_tabular_classification.src.pydantic_models import (
        PredictionInput,
        PredictionResponse,
    )


logging.config.dictConfig(LOGGING_CONFIG)

predictor = ModelPredictor()

app = FastAPI(title="Demo Tabular Classification Inference API", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    allow_origin_regex=None,
    max_age=600,
)


@app.get("/")
async def get_all_routes():
    logging.info("Retrieving all routes")
    routes = [{"path": route.path, "name": route.name} for route in app.routes]
    logging.info(f"Found {len(routes)} routes")
    return routes


@app.get("/health")
async def health():
    return Response(status_code=200, content="Ready")


@app.get("/metronome")
async def metronome():
    last_tick = time.time()
    while True:
        await asyncio.sleep(0.2)
        now = time.time()
        print(now - last_tick)
        last_tick = now
    return Response(status_code=200)


@app.post("/predict", response_model=PredictionResponse)
async def predict(input_data: PredictionInput) -> Dict[str, Any]:
    try:
        model_input = input_data.features
        result = predictor.predict_single(model_input)
        return {
            "predicted_class": int(result["prediction"]),
            "class_probabilities": result["probability"].tolist(),
            "classes": result["classes"].tolist(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def main():
    print("API is running at http://localhost:8000")
    print("Documentation is available at http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
