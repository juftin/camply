ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim-bookworm AS base

RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

FROM base AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_LOCKED=1 \
    VIRTUAL_ENV=/app/.venv

COPY pyproject.toml uv.lock /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-install-project

COPY README.md /app/README.md
COPY src/ /app/src/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-editable

FROM base AS final

COPY --from=builder /app/.venv /app/.venv

ENV PATH=/app/.venv/bin:${PATH}

COPY config/ /app/config/

CMD [
    "gunicorn",
    "--config",
    "/app/config/gunicorn.conf.py",
    "camply_web.app:app"
]
