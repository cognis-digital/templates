# Multi-stage, non-root, slim Python image template.
#
# Build:   docker build -t cognis-app -f docker/Dockerfile .
# Run:     docker run --rm -p 8000:8000 cognis-app
#
# Adjust APP_MODULE / the CMD to match your project's entry point.

# ---- builder ---------------------------------------------------------------
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install build deps into an isolated venv so the runtime stage stays lean.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy only dependency metadata first to maximize layer caching.
COPY pyproject.toml ./
COPY README.md ./
COPY src ./src

RUN pip install --upgrade pip && pip install .

# ---- runtime ---------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Create an unprivileged user to run the app.
RUN groupadd --system app && useradd --system --gid app --create-home app

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

USER app

EXPOSE 8000

# Lightweight liveness probe; replace with an app-specific check.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Replace with your real entry point (console script or module).
CMD ["cognis-tool", "greet", "--name", "Docker"]
