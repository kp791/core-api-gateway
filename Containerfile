# syntax=docker/dockerfile:1

FROM python:3.13.3-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Copy dependency file first for layer caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy FastAPI app source
COPY ./app /app/app

# Copy local certs (optional dev-only)
# Production deployments should mount secrets instead of COPY
COPY ./certs /certs

# Expose HTTPS development port
EXPOSE 8443

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8443", \
     "--ssl-keyfile", "/certs/key.pem", "--ssl-certfile", "/certs/cert.pem"]

