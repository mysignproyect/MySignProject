# Dockerfile para My Sign Backend (FastAPI)

# =============================================================================
# STAGE 1: Base
# =============================================================================
FROM python:3.11-slim as base

# Metadata
LABEL maintainer="Juan Esteban Acevedo Patiño"
LABEL description="Backend API para My Sign - Servicios Accesibles LSC"
LABEL version="1.0.0"

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Directorio de trabajo
WORKDIR /app

# =============================================================================
# STAGE 2: Dependencies
# =============================================================================
FROM base as dependencies

# Copiar solo requirements para aprovechar cache de Docker
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# =============================================================================
# STAGE 3: Production
# =============================================================================
FROM base as production

# Copiar dependencias instaladas desde stage anterior
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Copiar código de la aplicación
COPY app/ /app/app/
COPY data/ /app/data/
COPY main.py /app/

# Crear usuario no-root por seguridad
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Cambiar a usuario no-root
USER appuser

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/')" || exit 1

# Comando para iniciar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]