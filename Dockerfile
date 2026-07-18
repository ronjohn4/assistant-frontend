# Use official Python runtime as base image
# docker build -t ronjohn4/assistant-frontend .

FROM python:3.12-slim

# Copy the uv binary from the official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# uv optimization
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Working directory
WORKDIR /app

# Install build dependencies first (needed for compilation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    python3-dev \
    curl \
    espeak \
    alsa-utils \
    ffmpeg \
    libasound2-dev \
    espeak-ng-data \
    speech-dispatcher \
    speech-dispatcher-espeak \
    espeak-ng \
    libespeak1 \
    && rm -rf /var/lib/apt/lists/*

# Copy project dependency metadata for layer cache
COPY pyproject.toml uv.lock ./

# Install python dependencies using uv
RUN uv venv --python /usr/local/bin/python && uv sync --locked --no-dev --no-install-project

# Install gunicorn and ensure operating environment uses uv venv
RUN uv pip install gunicorn

# Copy app code
COPY . .

# Env for runtime
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

EXPOSE 5002

# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#     CMD curl --fail http://localhost/ || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5002", "--workers", "3", "app:app"]
