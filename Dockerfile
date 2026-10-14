FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    ONTOKB_LLM_PROVIDER=codex

# Install system dependencies (ffmpeg is required if using audio/video ingestion)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency definition and source code
COPY pyproject.toml ./
COPY src/ ./src/

# Install the application and core optional extras
RUN pip install --no-cache-dir ".[llm,html]"

# Copy project schemas, rules, and configuration templates
COPY ontology/ ./ontology/
COPY rules/ ./rules/
COPY config/ ./config/

# Ensure runtime directories exist
RUN mkdir -p /app/data /app/vault

# Expose API service port
EXPOSE 8765

# Default entrypoint: run ontoKB API server bound to all interfaces
CMD ["python", "-m", "ontokb.cli", "api", "--host", "0.0.0.0", "--port", "8765"]
