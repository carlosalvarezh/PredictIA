# src/api/schemas.py
from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    payload: Dict[str, Any] = Field(
        ..., description="Diccionario con las variables crudas requeridas por el modelo."
    )

class PredictResponse(BaseModel):
    class_label: str
    prob_beta: float
    threshold: float
    details: Dict[str, Any]

class BatchPredictRequest(BaseModel):
    records: List[Dict[str, Any]]

class BatchPredictResponse(BaseModel):
    predictions: List[PredictResponse]
