# Multistage Dockerfile for AI Data Analyst OS Backend Service
FROM python:3.12-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml and install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Copy application source code
COPY backend/ ./backend/

# Expose FastAPI port
EXPOSE 8000

ENV ENVIRONMENT=production
ENV PORT=8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
