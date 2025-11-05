# Setup del entorno

## Requisitos

- Python 3.11
- Windows 10/11 + PowerShell

## Pasos

1. Crear y activar venv:
py -3.11 -m venv .venv
..venv\Scripts\Activate.ps1

2. Instalar dependencias:
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

3. Verificación rápida en REPL:
import numpy, pandas, sklearn, statsmodels, fastapi, pydantic
print("OK")

Commits:
mkdir docs
ni docs\00_overview.md -ItemType File
ni docs\01_setup.md -ItemType File
git add docs
git commit -m "docs: overview y setup inicial del proyecto"
