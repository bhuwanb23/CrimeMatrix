FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    # Force TF-IDF fallback in models/embedding.py (no Torch on AppSail)
    EMBEDDING_BACKEND=tfidf

# No build-essential / no Torch — AppSail max 2048 MB RAM
COPY requirements-appsail.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${X_ZOHO_CATALYST_LISTEN_PORT:-8002}"]
