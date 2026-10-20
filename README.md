# MAYA AI

MAYA is an interior-design visualisation workspace: users organise projects and rooms, capture a structured brief, receive a validated design plan, and run media-generation jobs through replaceable providers. Phase 1 is mock-first and runs without API keys. Generated concepts are visualisations, not construction documents or guarantees of product availability, price, or code compliance.

## Monorepo

```text
backend/   FastAPI API, SQLAlchemy/Alembic, prompts, tests, providers
frontend/  React + TypeScript + Vite workspace
worker/    Python job consumer and FFmpeg media stages
docs/      governance decisions
.agents/   individually reviewed repository-local agent skills
shared/    reserved for generated cross-client contracts
.github/   GitHub Actions CI
```

## Quickstart (zero keys)

```sh
cp .env.example .env
docker compose up --build
```

Open the frontend at http://localhost:5173. Use the clearly labelled local dev-user mode, create a project, add a room and brief, request a mock plan, then enqueue a mock media job. The API is at http://localhost:8000 and health check at `/healthz`. No external model, Supabase, or GPU call is made in mock mode. If Docker is unavailable, run the API locally with `cd backend && uv sync --extra dev && uv run uvicorn app.main:app --reload`; use the SQLite default in `.env`.

## Where real secrets belong

| Variable | Put it in | Scope |
|---|---|---|
| `VITE_SUPABASE_URL`, `VITE_SUPABASE_PUBLISHABLE_KEY` | Frontend deployment settings (Cloudflare Pages/Vercel) | Publishable only; browser-visible |
| `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_JWT_SECRET` | API service secret manager (e.g. Cloudflare Worker/Container or hosting dashboard) | Server only; never `VITE_*` |
| `DATABASE_URL` | API and worker secret settings | Server only; use a Supabase Postgres pooler connection string if choosing hosted Postgres |
| `GEMINI_API_KEY` | API service secret manager | Server only; optional |
| `COMFYUI_BASE_URL`, `COMFYUI_API_TOKEN`, `HF_TOKEN` | Private worker deployment secrets | Worker only; never browser/serverless |
| `CLOUDFLARE_API_TOKEN`, `VERCEL_CRON_SECRET` | GitHub Actions secrets or the relevant deployment dashboard | CI/deployment only |

Never paste secret values into issues, chat, source files, or `.env.example`. `.env` is ignored by Git.

Set `ENVIRONMENT=production` in deployed API and worker environments. The API refuses to start in production without `SUPABASE_URL`; production never uses the local `dev-user`, even when `DEV_AUTH_ENABLED=true`. Keep `DEV_AUTH_ENABLED=true` only for local/CI use without Supabase.

`SUPABASE_URL` is the Auth/Storage API endpoint, not a PostgreSQL connection string; hosted database connections need a separate `DATABASE_URL`. Compose deliberately uses its local Postgres service. Apply `backend/db/rls_policies.sql` and create/verify the private `maya-assets` bucket only in the intended Supabase project.

## Governance files

- `OX_ALPHA_START_MAYA.md` — required agent boot order and reporting contract.
- `MAYA_OX_ALPHA_IMPLEMENTATION.md` — architecture, safety, and phased implementation brief.
- `MAYA_OX_ALPHA_SKILLS_CATALOG.md` and `.json` — skills guidance and approved install set.
- `MAYA_OX_ALPHA_SKILLS_TOOL_REGISTRY.md` and `.json` — discovery and tool-use governance.
- `MAYA_FREE_STACK_AND_TOOLS.md` and `.json` — free-first dependencies, MCPs, and secrets.
- `maya-skills-manifest.json` — machine-readable project scope.
- `.agents/skills/` and `skills-lock.json` — individually approved skill copies and integrity hashes.
- `docs/THIRD_PARTY_SKILLS.md` and `docs/third_party_licenses/` — upstream revisions, licenses, and notices for copied skills.
- `docs/skill-decisions.md` — append-only skill/governance decisions.
- `skills.sh` — validates the governance package and prints discovery guidance.

## Prohibited capabilities

This project must not implement CAPTCHA bypass, anti-detection, MFA bypass, credential harvesting, or rate-limit evasion. Social publishing is out of Phase 1; any future publishing requires official APIs and explicit per-action user approval. Heavy media processing belongs in worker containers, never serverless request handlers.
