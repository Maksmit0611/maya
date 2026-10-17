# syntax=docker/dockerfile:1
FROM python:3.12-slim AS build
WORKDIR /build
COPY --from=ghcr.io/astral-sh/uv:0.12.23 /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project
COPY app ./app
COPY migrations ./migrations
COPY alembic.ini ./alembic.ini
COPY db ./db

FROM python:3.12-slim AS runtime
WORKDIR /app
RUN addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --ingroup appgroup appuser
COPY --from=build --link --chown=1001:1001 /build/.venv /app/.venv
COPY --from=build --link --chown=1001:1001 /build/app /app/app
COPY --from=build --link --chown=1001:1001 /build/migrations /app/migrations
COPY --from=build --link --chown=1001:1001 /build/alembic.ini /app/alembic.ini
COPY --from=build --link --chown=1001:1001 /build/db /app/db
ENV PATH="/app/.venv/bin:$PATH" PYTHONPATH="/app"
USER 1001:1001
EXPOSE 8000
LABEL org.opencontainers.image.title="MAYA API"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
