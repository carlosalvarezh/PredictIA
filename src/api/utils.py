# src/api/utils.py
from __future__ import annotations
from functools import lru_cache
from typing import Any, Dict, List, Optional, Tuple
import joblib
import json
import numpy as np
import pandas as pd

from .config import load_config, ARTIFACTS_DIR

@lru_cache(maxsize=1)
def load_model():
    cfg = load_config()
    return joblib.load(cfg.model_path)

@lru_cache(maxsize=1)
def load_preprocessor():
    # Si en el futuro se separa el preprocesamiento del Pipeline
    cfg = load_config()
    if getattr(cfg, "preprocessor_path", None):
        return joblib.load(cfg.preprocessor_path)
    return None

@lru_cache(maxsize=1)
def load_feature_list() -> Optional[List[str]]:
    # Opcional: si luego se decide fijar el orden de features crudas con un JSON
    cfg = load_config()
    if getattr(cfg, "feature_list_path", None):
        p = cfg.feature_list_path
        if p and p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    return None

def _prepare_dataframe(payload: Dict[str, Any]) -> Tuple[pd.DataFrame, List[str], List[str]]:
    """
    Construye un DataFrame de una fila respetando un orden de columnas
    si se definió feature_list; si no, usa las claves del payload.
    Devuelve: df, missing_filled, ignored_extra
    """
    feature_list = load_feature_list()
    if feature_list:
        row = {k: payload.get(k, np.nan) for k in feature_list}
        ignored_extra = [k for k in payload.keys() if k not in feature_list]
        missing_filled = [k for k in feature_list if k not in payload]
        df = pd.DataFrame([row], columns=feature_list)
    else:
        df = pd.DataFrame([payload])
        missing_filled, ignored_extra = [], []
    return df, missing_filled, ignored_extra

def predict_alpha_beta(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Función de inferencia local (misma firma que usará la API).
    Entrada: dict con variables crudas del registro.
    Salida: dict con clase y probabilidad para la etiqueta positiva.
    """
    cfg = load_config()
    model = load_model()
    pre = load_preprocessor()

    df, missing_filled, ignored_extra = _prepare_dataframe(payload)
    X = pre.transform(df) if pre is not None else df

    # Índice de la clase positiva según las clases del modelo
    positive = cfg.positive_label
    if hasattr(model, "classes_"):
        # Intentar mapear etiqueta positiva a índice
        try:
            pos_idx = list(model.classes_).index(positive)
        except ValueError:
            # Si el modelo usa {0,1}, se asume 1 como positivo
            pos_idx = 1
        proba_pos = float(model.predict_proba(X)[0][pos_idx])
    else:
        # Modelos sin predict_proba: degradación conservadora
        pred = model.predict(X)[0]
        proba_pos = 1.0 if str(pred) == str(positive) else 0.0

    # Etiquetado final con umbral desde el JSON
    label = positive if proba_pos >= cfg.threshold else (
        [c for c in cfg.classes if c != positive][0] if len(cfg.classes) > 1 else "Alpha"
    )

    # Probabilidad explícita de Beta para el reporte (independiente de cuál sea positive)
    if "Beta" in cfg.classes:
        if hasattr(model, "classes_"):
            try:
                beta_idx = list(model.classes_).index("Beta")
            except ValueError:
                beta_idx = 1
            prob_beta = float(model.predict_proba(X)[0][beta_idx])
        else:
            prob_beta = 1.0 if label == "Beta" else 0.0
    else:
        # Si por alguna razón no está "Beta" en classes, usar proba_pos si positive=="Beta"
        prob_beta = proba_pos if positive == "Beta" else (1.0 - proba_pos)

    return {
        "class_label": label,
        "prob_beta": prob_beta,
        "threshold": float(cfg.threshold),
        "details": {
            "model_version": cfg.model_version or "",
            "classes": cfg.classes,
            "positive_label": positive,
            "missing_filled": missing_filled,
            "ignored_extra_fields": ignored_extra,
        },
    }
