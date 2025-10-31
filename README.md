# PredictIA: Sistema Integral de Predicción y Asistencia Inteligente

Proyecto técnico que integra:

1) Ciencia de Datos y ML: pronóstico de demanda (mensual) y clasificación Alpha/Beta.
2) GenAI: Agente asistente para Gestión Humana con enrutamiento a base de conocimiento o consulta a Excel de cesantías.

## Estructura

- `data/`: datos crudos y procesados (no versionados).
- `notebooks/`: análisis exploratorio, modelado y validación.
- `src/`: código productivo (features, modelos, API y scripts).
- `models_artifacts/`: modelos y objetos serializados.
- `reports/`: métricas, gráficos, salidas y documentos.
- `genai/`: POC de agente generativo con herramientas.
- `docker/`: contenedorización (opcional).
- `tests/`: pruebas unitarias.

## Requisitos

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows
# source .venv/bin/activate # Linux/macOS
pip install -r requirements.txt
