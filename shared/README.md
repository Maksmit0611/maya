# Shared API contracts

The FastAPI OpenAPI document is the source of truth at `/api/v1/openapi.json`. The current Vite client uses a small set of hand-typed API response interfaces in `frontend/src/types.ts`. Generate and check in cross-language contracts here when the public API stabilises; generated files must never contain server-only environment names or credentials.
