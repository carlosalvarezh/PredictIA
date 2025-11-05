# src/api/config.py
from __future__ import annotations
from pathlib import Path
from functools import lru_cache
import json
from typing import Any, Dict, List, Optional

# Estructura: .../<repo>/src/api/config.py  → raíz = parents[2]
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = PROJECT_ROOT / "models_artifacts"
CONFIG_PATH = ARTIFACTS_DIR / "inference_config.json"

class InferenceConfig:
    def __init__(self, d: Dict[str, Any]) -> None:
        # Claves según el JSON
        # - model_artifact: nombre del .joblib dentro de models_artifacts/
        # - classes: orden de clases, p. ej. ["Alpha","Beta"]
        # - threshold: umbral de decisión
        self.model_path: Path = ARTIFACTS_DIR / d.get("model_artifact", "clf_alpha_beta_final.joblib")
        self.classes: List[str] = list(d.get("classes", ["Alpha", "Beta"]))
        self.threshold: float = float(d.get("threshold", 0.5))

        # Etiqueta positiva: por defecto "Beta" si existe en classes; si no, la última
        self.positive_label: str = d.get(
            "positive_label",
            "Beta" if "Beta" in self.classes else (self.classes[-1] if self.classes else "Beta")
        )

        # Opcionales
        self.feature_list_path: Optional[Path] = None  # si más adelante se quiere fijar orden de features
        self.preprocessor_path: Optional[Path] = None  # si el modelo NO incluye preproc en el Pipeline
        self.model_version: str = d.get("model_version", "")
        self.extra: Dict[str, Any] = d

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_artifact": str(self.model_path.name),
            "classes": self.classes,
            "threshold": self.threshold,
            "positive_label": self.positive_label,
            "model_version": self.model_version or "",
        }

@lru_cache(maxsize=1)
def load_config() -> InferenceConfig:
    if not CONFIG_PATH.exists():
        # Fallback: si el archivo no existe, usa defaults compatibles con el actual esquema
        data = {
            "threshold": 0.5,
            "classes": ["Alpha","Beta"],
            "model_artifact": "clf_alpha_beta_final.joblib"
        }
        return InferenceConfig(data)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return InferenceConfig(data)
