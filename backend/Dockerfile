# ── Backend image ──────────────────────────────────────
FROM python:3.13-slim

# Evitar archivos .pyc y habilitar logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias primero (caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

EXPOSE 5000

# Producción: gunicorn | Desarrollo: flask run
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "run:app"]
