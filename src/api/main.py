# src/api/main.py
from __future__ import annotations
from typing import List
from fastapi import FastAPI
from .schemas import (
    PredictRequest, PredictResponse,
    BatchPredictRequest, BatchPredictResponse
)
from .utils import predict_alpha_beta
from .config import load_config

app = FastAPI(title="Alpha/Beta Classifier API", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/schema")
def schema():
    cfg = load_config()
    return {
        "request_example": {
            "payload": {
                "customer": "C123",
                "material": "MAT45",
                "supplier": "S001",
                "region": "Norte",
                "month": "2022-05",
                "lead_time_days": 12,
                "safety_stock": 30,
                "demand_forecast": 245.0,
                "some_binary_flag": 1
            }
        },
        "response_example": {
            "class_label": "Beta",
            "prob_beta": 0.612,
            "threshold": cfg.threshold,
            "details": {
                "model_version": cfg.model_version or "",
                "classes": cfg.classes
            }
        }
    }

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    result = predict_alpha_beta(req.payload)
    return PredictResponse(**result)

@app.post("/predict/batch", response_model=BatchPredictResponse)
def predict_batch(req: BatchPredictRequest):
    outputs: List[PredictResponse] = []
    for record in req.records:
        outputs.append(PredictResponse(**predict_alpha_beta(record)))
    return BatchPredictResponse(predictions=outputs)
