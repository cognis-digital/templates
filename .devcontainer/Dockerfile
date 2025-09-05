# Dev container base image. Ships a current Python plus uv so the workspace is
# ready to `uv pip install -e '.[dev]'` immediately.
ARG PYTHON_VERSION=3.12
FROM mcr.microsoft.com/devcontainers/python:1-${PYTHON_VERSION}-bookworm

# Install uv (fast Python package manager) for all users.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_LINK_MODE=copy \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Pre-install common dev tooling so a fresh container is usable offline.
RUN pip install --no-cache-dir ruff mypy pytest
