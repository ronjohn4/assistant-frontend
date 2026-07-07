# Use official Python runtime as base image
# docker build -t assistant-frontend .docker build -t assistant-frontend .

FROM python:3.12-slim

# Copy the uv binary from the official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# uv optimization
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Working directory
WORKDIR /app

# Copy project dependency metadata for layer cache
COPY pyproject.toml uv.lock ./

# Install python dependencies using uv
RUN uv venv --python /usr/local/bin/python && uv sync --locked --no-dev --no-install-project

# Install system packages including nginx
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install gunicorn and ensure operating environment uses uv venv
RUN uv pip install gunicorn

# Copy app code
COPY . .

# Env for runtime
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

EXPOSE 5001

# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#     CMD curl --fail http://localhost/ || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "3", "app:app"]
