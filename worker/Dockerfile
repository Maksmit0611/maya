# syntax=docker/dockerfile:1
FROM python:3.12-slim AS build
WORKDIR /build
COPY --from=ghcr.io/astral-sh/uv:0.12.23 /uv /uvx /bin/
COPY backend/pyproject.toml backend/uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project
COPY backend/app ./app
COPY worker ./worker

FROM python:3.12-slim AS runtime
WORKDIR /app
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update \
    && apt-get install --no-install-recommends -y ffmpeg \
    && addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --ingroup appgroup appuser \
    && mkdir -p /app/results \
    && chown -R 1001:1001 /app
COPY --from=build --link --chown=1001:1001 /build/.venv /app/backend/.venv
COPY --from=build --link --chown=1001:1001 /build/app /app/backend/app
COPY --from=build --link --chown=1001:1001 /build/worker /app/worker
ENV PATH="/app/backend/.venv/bin:$PATH" PYTHONPATH="/app/backend:/app"
USER 1001:1001
LABEL org.opencontainers.image.title="MAYA media worker"
CMD ["python", "-m", "worker.main"]
