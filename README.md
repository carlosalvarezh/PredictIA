<!-- markdownlint-disable MD025 MD040 MD004 MD032 MD001 -->
# PredictIA: Sistema Integral de Predicción y Asistencia Inteligente

Proyecto técnico que integra:

1) **Ciencia de Datos y ML**: pronóstico de demanda mensual y **clasificación Alpha/Beta**.  

2) **GenAI**: agente asistente para Gestión Humana con enrutamiento a base de conocimiento o consulta a Excel de cesantías.

---

## Estructura general del repositorio

- `data/`: datos crudos y procesados (no versionados).
- `notebooks/`: EDA, modelado y validación.
- `src/`: código productivo (features, modelos, API, utilidades).
- `models_artifacts/`: artefactos serializados del modelo (p. ej., `clf_alpha_beta_final.joblib`, `inference_config.json`).
- `reports/`: métricas, gráficos y salidas.
- `genai/`: POC de agente generativo (opcional).
- `docker/`: contenedorización (opcional).
- `tests/`: pruebas unitarias.

---

# Punto 3 — API del modelo de Clasificación Alpha/Beta (Entregable solicitado)

Este componente expone un servicio **FastAPI** que:

- Se **ejecuta desde `main.py`** en la raíz del proyecto.
- **Carga** el modelo del punto 2 desde `models_artifacts/`.
- **Recibe** un JSON por `POST /predict` con las variables que usa el modelo.
- **Clasifica** en Alpha/Beta y **devuelve** la respuesta en JSON.

### Requisitos de entorno

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux / macOS
pip install -r requirements.txt
````

### Estructura mínima de la API

```
.
├─ main.py                     # Punto de entrada (uvicorn → FastAPI)
├─ requirements.txt
├─ models_artifacts/
│   ├─ clf_alpha_beta_final.joblib
│   └─ inference_config.json   # {"threshold": 0.57, "classes": ["Alpha","Beta"], "model_artifact": "clf_alpha_beta_final.joblib"}
└─ src/
   └─ api/
      ├─ main.py               # Endpoints FastAPI
      ├─ config.py             # Carga de config/artefactos
      ├─ utils.py              # Función de inferencia local
      └─ schemas.py            # Esquemas de request/response
```

> Nota: el modelo y la configuración provienen del **punto 2** (Alpha/Beta). No es necesario reentrenar para ejecutar la API.

### Ejecutar el servicio

Desde la **raíz** del proyecto:

```bash
python main.py
```

Verás algo como:

```
Uvicorn running on http://127.0.0.1:8000
```

### Probar desde el navegador (Swagger UI)

Abrir:

```
http://127.0.0.1:8000/docs
```

En **POST /predict → Try it out**, pegar el siguiente ejemplo (ajusta los campos a tus variables reales del modelo):

```json
{
  "payload": {
    "SeniorCity": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "Service1": "No",
    "Service2": "No phone service",
    "Security": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "Charges": 29.85,
    "Demand": "29.85"
  }
}
```

Respuesta esperada (ejemplo):

```json
{
  "class_label": "Beta",
  "prob_beta": 0.67,
  "threshold": 0.57,
  "details": {
    "classes": ["Alpha", "Beta"],
    "positive_label": "Beta",
    "missing_filled": [],
    "ignored_extra_fields": []
  }
}
```

### Endpoints disponibles

| Endpoint         | Método | Descripción                                             |
| ---------------- | ------ | ------------------------------------------------------- |
| `/health`        | GET    | Estado del servicio                                     |
| `/schema`        | GET    | Ejemplos de request/response                            |
| `/predict`       | POST   | Inferencia para un único registro                       |
| `/predict/batch` | POST   | Inferencia para múltiples registros (lista de payloads) |

---

## Punto 4 — Inferencia masiva sobre `to_predict.csv` y exportación de resultados

El proyecto incluye un script autónomo que permite ejecutar el modelo Alpha/Beta sobre un conjunto completo de registros almacenados en un archivo CSV y exportar las predicciones.

### Ejecución

Desde la raíz del proyecto:

```bash
python -m src.api.predict_from_csv --input data/raw/to_predict.csv --output reports/predictions_alpha_beta.csv
```

El script:

1. Carga el archivo de entrada (to_predict.csv).

2. Aplica la misma función de inferencia local usada por la API (predict_alpha_beta()).

3. Genera el archivo reports/predictions_alpha_beta.csv con las columnas:

- row_id
- class_label (Alpha / Beta)
- prob_beta
- prob_alpha (complementaria)
- threshold

Ejemplo de salida

En consola:

```bash
Leyendo archivo de entrada: data/raw/to_predict.csv
Registros cargados: 3

--- Resumen de predicciones ---
Alpha :     2 (66.67%)
Beta  :     1 (33.33%)
Total : 3

Archivo de resultados guardado en:
reports/predictions_alpha_beta.csv
```

---

## Notas técnicas de implementación

* La API lee `models_artifacts/inference_config.json` con el siguiente esquema mínimo:

  ```json
  {
    "threshold": 0.57,
    "classes": ["Alpha","Beta"],
    "model_artifact": "clf_alpha_beta_final.joblib"
  }
  ```
  
* La inferencia usa la misma **función local** que el notebook del punto 2 (misma firma), garantizando consistencia entre entrenamiento y servicio.
* Si el preprocesamiento está **incluido en el Pipeline** del modelo, basta con enviar variables crudas (categóricas y numéricas) como en el ejemplo.
  Si está separado, `src/api/config.py` contempla un `preprocessor_path` opcional.

---

## Licencia y créditos

Proyecto desarrollado en el marco de la **Prueba Técnica PredictIA – Argos (2025)**.
