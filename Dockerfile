# Imagen base ligera
FROM python:3.11-slim

# Evitar bytecode y forzar log en stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Crear usuario no-root
RUN useradd -m appuser

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (si hicieran falta en el futuro)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential && \
#     rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar código y artefactos del modelo
COPY src /app/src
COPY main.py /app/main.py
COPY models_artifacts /app/models_artifacts

# Exponer puerto del servicio
EXPOSE 8000

# Cambiar a usuario no-root
USER appuser

# Comando por defecto: levantar la API
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
