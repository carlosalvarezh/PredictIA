# src/api/predict_from_csv.py
"""
Inferencia masiva sobre un CSV usando el modelo Alpha/Beta ya entrenado.

Uso:
  python -m src.api.predict_from_csv
  python -m src.api.predict_from_csv --input data/raw/to_predict.csv --output reports/predictions_alpha_beta.csv

Genera un CSV con:
- class_label  → Clase predicha (Alpha / Beta)
- prob_beta    → Probabilidad de pertenecer a Beta
- prob_alpha   → Probabilidad complementaria (1 - prob_beta)
- threshold    → Umbral usado para decidir la clase
"""

from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
from .utils import predict_alpha_beta  # función de inferencia local

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inferencia masiva Alpha/Beta desde CSV")
    parser.add_argument("--input", "-i", type=str, default="", help="Ruta al CSV de entrada")
    parser.add_argument("--output", "-o", type=str, default="", help="Ruta del CSV de salida")
    return parser.parse_args()


def resolve_input_path(cli_path: str) -> Path:
    if cli_path:
        path = PROJECT_ROOT / cli_path if not Path(cli_path).is_absolute() else Path(cli_path)
        if path.exists():
            return path.resolve()
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {path}")

    # Intento automático si no se da argumento
    for candidate in [
        PROJECT_ROOT / "data" / "to_predict.csv",
        PROJECT_ROOT / "data" / "raw" / "to_predict.csv",
        PROJECT_ROOT / "to_predict.csv",
    ]:
        if candidate.exists():
            return candidate.resolve()

    raise FileNotFoundError(
        "No se encontró el archivo de entrada (to_predict.csv). "
        "Ejecuta con --input <ruta_al_csv>."
    )


def resolve_output_path(cli_path: str) -> Path:
    if cli_path:
        path = PROJECT_ROOT / cli_path if not Path(cli_path).is_absolute() else Path(cli_path)
    else:
        path = PROJECT_ROOT / "reports" / "predictions_alpha_beta.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path.resolve()


def main() -> None:
    args = parse_args()
    input_path = resolve_input_path(args.input)
    output_path = resolve_output_path(args.output)

    print(f"\nLeyendo archivo de entrada: {input_path}")
    df = pd.read_csv(input_path)
    print(f"Registros cargados: {len(df)}")

    preds = []
    for i, row in df.iterrows():
        payload = row.to_dict()
        res = predict_alpha_beta(payload)
        prob_beta = res["prob_beta"]
        prob_alpha = 1 - prob_beta
        preds.append({
            "row_id": i,
            "class_label": res["class_label"],
            "prob_beta": round(prob_beta, 4),
            "prob_alpha": round(prob_alpha, 4),
            "threshold": res["threshold"],
        })

    pred_df = pd.DataFrame(preds)
    pred_df.to_csv(output_path, index=False)

    # Conteo resumido
    counts = pred_df["class_label"].value_counts().to_dict()
    total = len(pred_df)
    print("\n--- Resumen de predicciones ---")
    for label, n in counts.items():
        pct = (n / total) * 100
        print(f"{label:<6}: {n:>5} ({pct:5.2f}%)")
    print(f"Total : {total}")

    print(f"\nArchivo de resultados guardado en:\n{output_path}\n")


if __name__ == "__main__":
    main()
