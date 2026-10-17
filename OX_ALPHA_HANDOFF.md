# MAYA AI — handoff to Ox Alpha

**Status:** 2026-10-17. Continue the existing repository at [Maksmit0611/maya](https://github.com/Maksmit0611/maya), branch `main`. The keyless Phase 1 scaffold is implemented. This is an implementation handoff, not a claim that MAYA is deployed or generating finished interior renders.

## Paste this instruction into Ox Alpha

> Open `https://github.com/Maksmit0611/maya` on `main`. Read `OX_ALPHA_HANDOFF.md`, `README.md`, `OX_ALPHA_START_MAYA.md`, `MAYA_OX_ALPHA_IMPLEMENTATION.md`, `MAYA_OX_ALPHA_SKILLS_CATALOG.json`, `MAYA_OX_ALPHA_SKILLS_TOOL_REGISTRY.json`, `MAYA_FREE_STACK_AND_TOOLS.md`, and `docs/skill-decisions.md`. Continue the existing React/FastAPI/Postgres/worker codebase; do not scaffold a new repository or reinstall its reviewed skills. First run the keyless Compose flow and CI checks, then implement the next milestone below in code with tests and a short changed-files/verification report. Keep provider credentials in server or worker secret settings. If the owner has not configured Supabase or a GPU provider, continue developing and testing the mock path. Treat the implementation brief as the target specification and this handoff as the record of what already exists. Do not claim real media generation, RAG, or social publishing until those features work end to end.

## What is already implemented

| Area | Current repository state | Where to start reading |
| --- | --- | --- |
| Backend | Python 3.12 FastAPI API, Pydantic v2 schemas, async SQLAlchemy models, Alembic migration, project membership checks, structured errors with request IDs. Routes cover projects, rooms/assets, briefs, chat planning, jobs, and results. | `backend/app/main.py`, `backend/app/api/v1/`, `backend/app/models/`, `backend/migrations/versions/0001_initial.py` |
| Auth and assets | Supabase JWT verification path; local/test `dev-user` path with no keys. Private Supabase Storage signed upload path when configured, local signed upload path for the mock walkthrough. Supabase RLS policy script exists but has **not** been applied to an owner's Supabase project. | `backend/app/core/auth.py`, `backend/app/api/v1/rooms.py`, `backend/db/rls_policies.sql` |
| Planning | Versioned design-plan prompt, strict `DesignPlan` contract, deterministic mock chat provider, optional Gemini JSON response provider selected by server-side `GEMINI_API_KEY`. | `backend/app/prompts/`, `backend/app/schemas/api.py`, `backend/app/providers/chat/` |
| Jobs and media | Idempotency-Key replay, status/cancel API, provenance, worker claim with PostgreSQL `FOR UPDATE SKIP LOCKED`, stage checks, heartbeat, result persistence. Mock FFmpeg slate clip or placeholder metadata. ComfyUI class is a graceful unavailable stub, even if a URL is supplied. | `backend/app/api/v1/jobs.py`, `worker/main.py`, `backend/app/providers/media/` |
| Frontend | React/TypeScript/Vite login, project workspace, room upload, brief wizard, agent plan, live job polling, results and selection. Responsive initial styling and frontend unit/E2E checks. | `frontend/src/`, `frontend/e2e/happy-path.spec.ts` |
| Local stack and CI | Compose Postgres, API, worker, frontend; migration/seed path. GitHub Actions runs Ruff, mypy, pytest with coverage gate, frontend typecheck/lint/unit/build/secret scan, and Playwright against Compose. | `docker-compose.yml`, `.github/workflows/ci.yml`, `README.md` |
| Skills and tools | Curated catalog and registry, 13 individually reviewed repository-local skills with lock hashes/license record; one skill was skipped for missing declared license. No bulk install is needed. | `.agents/skills/`, `skills-lock.json`, `docs/THIRD_PARTY_SKILLS.md`, `docs/skill-decisions.md`, `skills.sh` |

The latest verified code baseline before this handoff was commit `486fd9ee27a909790ca6a33fc3f98951862ab9c1`: [GitHub Actions CI run 39007933702](https://github.com/Maksmit0611/maya/actions/runs/39007933702) completed successfully for backend, frontend, and Compose E2E. Earlier local backend verification had 23 passing tests and 87.25% coverage. A documentation-only handoff commit may have its own later CI run; check that run before changing code.

## Run it now with zero keys

```sh
git clone https://github.com/Maksmit0611/maya.git
cd maya
cp .env.example .env
docker compose up --build
```

Open `http://localhost:5173`. In local dev mode, create a project and room, upload a photo, complete a brief, request a mock plan, queue a mock job, and select a result. API health is `http://localhost:8000/healthz`; the current FastAPI OpenAPI document is at `http://localhost:8000/openapi.json`. The CI Playwright test covers the same happy path. Run `./skills.sh --discover` to review the catalog; installed copies are already present in `.agents/skills/`.

## What is still missing

- **No production deployment or production auth configuration.** The local/test dev-user mode is enabled by default and Compose explicitly enables it. A production configuration must require real authentication and must never allow dev-user access.
- **No live Supabase project migration/RLS verification.** The migration and policy script exist, but the owner must select a Supabase project and supply its connection/settings through secret managers. Test the policies with multiple real users and private bucket paths before launch.
- **No real media generation.** The FFmpeg output is a placeholder slate. `ComfyUIProvider` currently raises `ProviderUnavailable`; FLUX/SDXL/ControlNet/video workflows, GPU hosting, asset downloads, and real render previews are not implemented.
- **No live Gemini acceptance check.** The adapter exists behind a key, but end-to-end behavior against an owner's account has not been validated. Mock planning is the verified path.
- **No vector memory/RAG, multi-tool autonomous pipeline, music generation, builder-grade exports, social OAuth/publishing, or marketing automation.** These appear in the target brief/catalog as future phases, not completed features.
- **No production hardening claim.** Review upload validation, storage retention, abuse limits, job retries/quotas, cost controls, data isolation, observability, and provider failure handling before opening a public service.

## Next implementation milestones, in order

1. **Harden the Phase 1 boundary without keys.** Refuse startup or authenticated API access when `ENVIRONMENT=production` and Supabase auth is absent; disable `dev-user` in production regardless of `DEV_AUTH_ENABLED`. Add focused auth tests. Review upload validation and ensure signed URLs/paths and secrets are not logged. Preserve the passing mock walkthrough.
2. **Wire a real Supabase test project once the owner provisions it.** Use server-only `DATABASE_URL`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, and the appropriate JWT verification configuration. Apply Alembic and then review/apply `backend/db/rls_policies.sql` to that project, confirm private `maya-assets` bucket, and test cross-project denial with two users. Keep service-role access out of the frontend. Do not run migrations against an unidentified production database.
3. **Build one working media adapter in the worker.** Implement ComfyUI health, fixed versioned workflow input mapping, queue/history polling, cancellation where supported, output retrieval into private storage, normalized errors, provenance and workflow hash. Start with one licensed image model/workflow, a bounded request, and a mock/provider integration test. Expand to conditioning and video only after this path renders and survives failure/retry tests. GPU infrastructure and model licenses must be selected explicitly.
4. **Add project-scoped agent memory and orchestration.** Introduce a reviewed migration for embeddings/vector search (for example pgvector), ingestion/retention controls and tests for project isolation. Plan the stages as brief → storyboard → image → optional video/music → review; persist every tool call, cost/latency, cancellation state and artifact. Cap steps, retries, and spending. User confirmation is required before any external publishing action.
5. **Grow the product and deploy previews.** Complete Room Studio before/after view, builder option board/exports, accessible design tokens, better API state/error UX, rate limits and quotas. Deploy the frontend and API/worker/database only after the selected hosting plan and secrets are configured. Run migrations in a controlled release, smoke-test auth/storage/jobs on the preview, then request owner review for production.

For each milestone: make a small reviewable change, run relevant checks, update docs/skill decisions if skill governance changes, and report what works in mock mode versus real providers. The implementation brief is intentionally broader than the current code; reconcile differences through tested increments instead of declaring features complete from a specification.

## Skills, tools, and secrets

The curated skills, install approvals, free-first APIs, CLIs, MCPs, and provider choices are documented in `MAYA_OX_ALPHA_SKILLS_CATALOG.json`, `MAYA_OX_ALPHA_SKILLS_TOOL_REGISTRY.json`, `MAYA_FREE_STACK_AND_TOOLS.md`/`.json`, and `maya-skills-manifest.json`. The repository already contains reviewed skill copies. New skill additions must be previewed, licensed, approved according to the catalog, installed individually, and recorded in `docs/skill-decisions.md`; never use `--all`.

No real key is required to continue the next keyless milestone. `.env.example` lists variable names and `README.md` maps them to deployment dashboards. Use `.env` only for local noncommitted configuration. Browser code may consume only publishable `VITE_*` values; server/worker API keys and database credentials belong in their respective secret stores. Do not paste secret values into prompts, Git, issues, or the handoff.

## Owner inputs that unlock later work

The agent can proceed through the mock and hardening work now. For live integrations the owner will eventually choose: (1) the Supabase project and hosting region, (2) where the ComfyUI/GPU worker will run and which licensed models to use, (3) whether Gemini or another planning provider is preferred, (4) brand/design examples and the first user workflow to prioritize, and (5) whether publication integrations are in scope. Collect keys only through the chosen service's secret settings, not in chat.

**Guardrails:** Generated designs are visualizations, not certified construction plans. No CAPTCHA, anti-detection, MFA, or rate-limit bypass; no credential harvesting. Future social posting must use official APIs and an explicit per-action user approval. Keep heavy media processing in worker containers.
