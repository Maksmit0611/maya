# MAYA AI — offline implementation pack for Ox Alpha

## Read this first

This is a complete offline handoff. Ox Alpha does not need web access, links, GitHub access, or external documentation to begin. Read this file from top to bottom and implement the instructions in the existing project directory. If the project directory is empty, scaffold the repository described here. If source code is present, inspect it and preserve working behavior.

Do not wait for external links. Do not invent a new architecture. Do not claim an integration is live until it works with tests. Work in small milestones, run checks after each milestone, and report changed files, commands, tests, mock-provider behavior, real-provider behavior, and blockers.

## Latest implementation status — 20 October 2026

**Milestone 1, production-auth boundary, is implemented in the current code excerpt at the end of this file.** Production app startup now fails if Supabase Auth is not configured. Local `dev-user` authentication is only permitted outside production when no Supabase URL is configured; setting `DEV_AUTH_ENABLED=true` cannot override that production boundary. The zero-key local and CI workflow remains available. Backend checks passed: Ruff, mypy, 26 pytest tests at 87.33% coverage, Alembic upgrade, and seed. Read the exact current files and tests at the end of this pack. This section supersedes older embedded handoffs that say Milestone 1 is still pending.

**Next work:** connect and verify an owner-provisioned Supabase test project, private Storage, RLS, and two-user isolation. Do not apply migrations to an unidentified production database. Then implement one real ComfyUI image workflow and proceed to RAG/orchestration and product/deployment milestones.

## Mission

Build MAYA AI, a multi-user interior-design visualization agent for homeowners, builders, and designers. It accepts room photos and structured briefs, creates validated design plans, generates visual concepts through replaceable providers, records provenance, and gives users a reviewable workspace. Designs are visualizations and planning aids; they are not certified construction documents, structural advice, code approvals, or guaranteed product/price claims.

## Immediate implementation task — completed

1. Production startup requires a configured `SUPABASE_URL`.
2. `dev-user` is blocked in production even when `DEV_AUTH_ENABLED=true`.
3. The zero-key local/CI path remains enabled when configured for development or tests.
4. Focused production-auth tests are in `backend/tests/test_api.py`.
5. The current code and verified checks are reproduced at the end of this file.

Then continue in this order: real Supabase migration/storage/RLS and two-user isolation; one real ComfyUI image workflow in the worker; project-scoped vector memory/RAG; bounded agent orchestration; Room Studio and builder exports; accessibility, quotas, observability, preview deployment; and only then official social APIs with explicit per-action approval.

## Current verified state

- React + TypeScript + Vite frontend with login, projects, rooms, uploads, brief wizard, plan panel, job polling, and result selection.
- Python 3.12 FastAPI backend with Pydantic v2, async SQLAlchemy, Alembic, typed routes, structured errors, and project membership checks.
- PostgreSQL worker with `FOR UPDATE SKIP LOCKED`, idempotency, cancellation, heartbeat, provenance, and mock FFmpeg slate/metadata.
- Deterministic mock chat, optional Gemini JSON provider, mock media provider, and ComfyUI unavailable stub.
- Database migration and separate Supabase RLS policy SQL.
- Compose Postgres/API/worker/frontend stack with keyless development.
- CI for backend, frontend, secret scanning, migration/seed, and Playwright E2E. Latest known application CI passed; local auth milestone checks also pass as recorded above.
- Thirteen individually reviewed local skills with lock hashes and license decisions.

## Not yet complete

Production deployment, live Supabase RLS verification, real ComfyUI image/video generation, live Gemini acceptance, vector memory/RAG, autonomous multi-tool chaining, music generation, builder exports, social OAuth/publishing, marketing automation, quotas, abuse controls, retention, observability, cost controls, and public-service hardening are future work. The production-auth boundary is implemented, but live production auth is not yet accepted against an owner's Supabase project.

## Zero-key acceptance flow

Copy `.env.example` to `.env`, start the Compose stack, and open `localhost:5173`. Use local dev-user mode to create a project and room, upload a photo, submit a brief, request a mock plan, enqueue a mock job, and select a result. API health is `localhost:8000/healthz`; OpenAPI is `localhost:8000/openapi.json`. No external API key or GPU is required.

## Required principles

Keep routers thin and business rules in services. Validate all provider output with Pydantic. Keep prompts versioned and persist prompt/model/workflow/seed/source/timestamp provenance. Use idempotency keys, bounded retries, cancellation checks, and worker heartbeats. Keep uploads private and project-scoped with short-lived signed URLs. Keep credentials out of browser bundles, logs, prompts, issues, and commits. Provide loading/empty/retry/error/focus/reduced-motion states. Run heavy media work in workers. Retain the mock path and add tests for every change.

## Security boundaries

Server/worker-only variables: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_JWT_SECRET`, `DATABASE_URL`, `GEMINI_API_KEY`, `COMFYUI_BASE_URL`, `COMFYUI_API_TOKEN`, `HF_TOKEN`.

Browser-safe variables: only publishable `VITE_*` values such as `VITE_SUPABASE_URL`, `VITE_SUPABASE_PUBLISHABLE_KEY`, and `VITE_API_BASE_URL`.

Never implement CAPTCHA bypass, anti-detection, MFA bypass, credential harvesting, rate-limit evasion, uncontrolled shell execution, unsafe SQL construction, or publication without explicit approval. Future social publishing must use official APIs, minimum scopes, signed webhooks, deduplication, secure refresh-token storage, and one approval per external action.

## Repository tree

```text
backend/                 FastAPI API, models, schemas, services, providers, prompts, tests
backend/app/api/v1/      projects, rooms/assets, briefs, chat, jobs, results
backend/app/core/        config, database, auth, structured errors
backend/app/models/      SQLAlchemy entities
backend/app/schemas/     Pydantic contracts
backend/app/providers/   chat/media adapters and workflow files
backend/app/services/    access, providers, provenance
backend/migrations/      Alembic migration
backend/db/              RLS policy SQL
frontend/src/            React application and typed API client
frontend/e2e/            Playwright happy path
worker/                  queue consumer and media stages
.agents/skills/          reviewed local skills
.github/workflows/       CI
```

## Offline fallback

If a provider, package, license, model, or service cannot be reached, implement the interface, configuration, mock provider, deterministic fixtures, validation, and tests. Record the integration as unavailable. Do not silently replace it with an unsafe or unlicensed dependency.

## Embedded project material

The sections below are copied from the project handoff, implementation brief, skills catalog, tool registry, free-stack guidance, environment files, CI configuration, governance records, and the reviewed skill instructions. They are included so Ox Alpha can work without links or web access.


---

## Complete prior handoff

# MAYA AI — complete handoff for Ox Alpha

## How to use this file

This is the single handoff file for continuing MAYA AI. Give this entire file to Ox Alpha together with access to the repository:

- Repository: [external address omitted in offline package]
- Branch: `main`
- Handoff commit: `ea547fe8dc47e4d88c52d8dd16c5bec75a30c098`
- Latest verified CI run: [external address omitted in offline package]

Read the instruction below first. Then inspect the repository. The repository is the source of truth for implementation; the documents embedded after the instruction are the complete project brief, skills catalog, tools registry, free stack, environment rules, and governance records used to build it.

## Instruction to Ox Alpha

Continue building the existing MAYA AI interior-design agent in the repository above. Do not create a new project, replace the current architecture, or restart Phase 1. Read this whole handoff and then inspect the code. Start with the first next milestone: harden production authentication without breaking the zero-key mock workflow.

Your first implementation task is:

1. When `ENVIRONMENT=production`, reject local `dev-user` authentication even if `DEV_AUTH_ENABLED=true`.
2. Require configured Supabase authentication for production API access.
3. Preserve the zero-key local and CI mock workflow.
4. Add focused backend tests for production authentication boundaries.
5. Run the backend checks and report changed files, commands, passing tests, and remaining blockers.

After that, continue in this order:

1. Connect and test a real Supabase project, including Alembic migration, private Storage bucket, RLS policies, and cross-user isolation.
2. Implement one real ComfyUI image workflow in the worker with bounded inputs, queue/polling, private output storage, cancellation, failures, retries, provenance, and mock fallback.
3. Add project-scoped vector memory/RAG and bounded agent orchestration: brief → storyboard → image → optional video/music → review.
4. Improve Room Studio, before/after comparison, builder exports, accessibility, quotas, observability, and preview deployment.
5. Only use official social APIs and explicit approval for any future publishing action.

Do not claim a feature is complete until it works end to end and has tests. Keep API keys, database credentials, service-role keys, Gemini keys, ComfyUI tokens, and Hugging Face tokens in server/worker secret settings only. Never expose them to browser code or commit them. Never use CAPTCHA bypass, anti-detection, MFA bypass, credential harvesting, or rate-limit evasion. Generated designs are visualizations, not certified construction plans.

## Current implementation status

### Already implemented

- React + TypeScript + Vite frontend.
- FastAPI + Python 3.12 backend with Pydantic v2, async SQLAlchemy, Alembic, and structured error envelopes.
- Projects, project members, rooms, assets, briefs, agent messages, generation jobs, and results data models.
- Supabase JWT verification path and clearly labelled local/test `dev-user` mode.
- Private signed asset upload path for Supabase and local signed upload path for mock development.
- Versioned prompt templates and strict `DesignPlan` validation.
- Deterministic mock chat provider and optional Gemini JSON provider behind a server-only key.
- Idempotent generation jobs through `Idempotency-Key`, status polling, cancellation requests, heartbeat, provenance, and worker claiming with PostgreSQL `FOR UPDATE SKIP LOCKED`.
- Mock FFmpeg slate clip or placeholder metadata. The ComfyUI provider is currently a graceful unavailable stub.
- React login, projects, room upload, brief wizard, agent plan panel, job polling, and result selection.
- Docker Compose services for local Postgres, API, worker, and frontend.
- GitHub Actions backend checks, frontend checks, secret scan, and Playwright Compose E2E.
- Thirteen individually reviewed repository-local skills under `.agents/skills/`, with hashes and license decisions recorded.

### Verified checks

The latest CI run passed backend, frontend, and E2E jobs. It validated the keyless flow: upload → brief → mock plan → mock job → result. Earlier local backend checks reported 23 passing tests and 87.25% coverage. A new documentation-only commit may trigger another CI run; check GitHub before changing code.

### Still missing

- Production deployment and production authentication hardening.
- Applying and testing Supabase RLS in the owner's project.
- Real ComfyUI image/video generation and licensed model workflows.
- Live Gemini acceptance testing with an owner's key.
- Vector memory/RAG, multi-tool agent orchestration, music generation, builder-grade exports, social OAuth/publishing, and marketing automation.
- Production quotas, abuse controls, upload retention, observability, cost controls, retries, and public-service hardening.

## Zero-key quickstart

```sh
git clone [external address omitted in offline package]
cd maya
cp .env.example .env
docker compose up --build
```

Open `[external address omitted in offline package]`. Create a project and room, upload a photo, submit a brief, request a mock plan, queue a mock job, and select the result. API health is `[external address omitted in offline package]`; OpenAPI is `[external address omitted in offline package]`. Run `./skills.sh --discover` to inspect the reviewed skill catalog. No external model, Supabase, or GPU call is required for this walkthrough.

## Repository layout

```text
backend/       FastAPI API, models, migrations, prompts, providers, tests
frontend/      React + TypeScript + Vite workspace and Playwright tests
worker/        Python job consumer and FFmpeg media stage
docs/          skill decisions, licenses, and governance
.agents/skills/ reviewed repository-local skills
.github/       GitHub Actions CI
```

## Important secret rules

- Browser code may use only publishable `VITE_*` values.
- `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_JWT_SECRET`, `DATABASE_URL`, `GEMINI_API_KEY`, `COMFYUI_API_TOKEN`, and `HF_TOKEN` are server/worker secrets.
- Never paste secret values in this file, chat, Git, issues, logs, or generated prompts.
- `.env` is for local configuration and must remain ignored by Git.
- In production, Supabase authentication must be required and local dev-user mode must be disabled.

## Embedded project documents

The remainder of this file contains the documents already created for the project. Each section keeps the original file path and content so Ox Alpha can read one file while still knowing where each document belongs in the repository.



---

## Source document: `OX_ALPHA_HANDOFF.md`

# MAYA AI — handoff to Ox Alpha

**Status:** 2026-10-17. Continue the existing repository at Maksmit0611/maya, branch `main`. The keyless Phase 1 scaffold is implemented. This is an implementation handoff, not a claim that MAYA is deployed or generating finished interior renders.

## Paste this instruction into Ox Alpha

> Open `[external address omitted in offline package]` on `main`. Read `OX_ALPHA_HANDOFF.md`, `README.md`, `OX_ALPHA_START_MAYA.md`, `MAYA_OX_ALPHA_IMPLEMENTATION.md`, `MAYA_OX_ALPHA_SKILLS_CATALOG.json`, `MAYA_OX_ALPHA_SKILLS_TOOL_REGISTRY.json`, `MAYA_FREE_STACK_AND_TOOLS.md`, and `docs/skill-decisions.md`. Continue the existing React/FastAPI/Postgres/worker codebase; do not scaffold a new repository or reinstall its reviewed skills. First run the keyless Compose flow and CI checks, then implement the next milestone below in code with tests and a short changed-files/verification report. Keep provider credentials in server or worker secret settings. If the owner has not configured Supabase or a GPU provider, continue developing and testing the mock path. Treat the implementation brief as the target specification and this handoff as the record of what already exists. Do not claim real media generation, RAG, or social publishing until those features work end to end.

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

The latest verified code baseline before this handoff was commit `486fd9ee27a909790ca6a33fc3f98951862ab9c1`: GitHub Actions CI run 39007933702 completed successfully for backend, frontend, and Compose E2E. Earlier local backend verification had 23 passing tests and 87.25% coverage. A documentation-only handoff commit may have its own later CI run; check that run before changing code.

## Run it now with zero keys

```sh
git clone [external address omitted in offline package]
cd maya
cp .env.example .env
docker compose up --build
```

Open `[external address omitted in offline package]`. In local dev mode, create a project and room, upload a photo, complete a brief, request a mock plan, queue a mock job, and select a result. API health is `[external address omitted in offline package]`; the current FastAPI OpenAPI document is at `[external address omitted in offline package]`. The CI Playwright test covers the same happy path. Run `./skills.sh --discover` to review the catalog; installed copies are already present in `.agents/skills/`.

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



---

## Source document: `OX_ALPHA_START_MAYA.md`

# Paste This into Ox Alpha

**Current continuation:** Phase 1 has been scaffolded and verified in this repository. Read `OX_ALPHA_HANDOFF.md` first for the implemented state, CI baseline, and next milestone. Continue the existing code; do not recreate Phase 1.

You are implementing MAYA AI, a cloud-hosted interior-design visualisation agent for homeowners, builders, and designers.

Read these files in order:

1. `skills.sh` — run `./skills.sh` and `./skills.sh --discover`.
2. `MAYA_OX_ALPHA_IMPLEMENTATION.md` — full implementation requirements.
3. `MAYA_OX_ALPHA_SKILLS_CATALOG.md` and `MAYA_OX_ALPHA_SKILLS_CATALOG.json` — curated skills.
4. `MAYA_OX_ALPHA_SKILLS_TOOL_REGISTRY.md` and JSON — live discovery and tool governance.
5. `MAYA_FREE_STACK_AND_TOOLS.md` and JSON — free-first tools, secrets, MCPs, and phase order.

Preserve existing repository conventions. If the repository is empty, create a monorepo with React + TypeScript frontend and FastAPI Python backend. Otherwise use `OX_ALPHA_HANDOFF.md` to continue from the current implementation.

Required Phase 1 outcomes:

- Supabase-backed Auth, PostgreSQL schema/migrations, RLS, and private asset storage.
- Responsive React project workspace, room upload, design brief wizard, job history, and option selection UI.
- Typed FastAPI routes/services/Pydantic schemas; background job model with idempotency, provenance, status, cancellation, and errors.
- `MockChatProvider` and `MockMediaProvider`, so the user flow works with no paid API, GPU, or secret configured.
- Optional `GeminiChatProvider` guarded by `GEMINI_API_KEY`; validate design-plan JSON before persistence.
- Versioned prompt templates, ComfyUI workflow placeholders, provider interfaces, and graceful unavailable-provider states.
- Docker/Compose for API/worker development; lint/type/test/Playwright CI; Cloudflare preview-ready frontend configuration.
- `.env.example`, README setup guide, migrations, seed/test fixtures, and no credentials in Git.

Security requirements:

- Keep service-role/API tokens server-side only; use RLS and project membership on all project data.
- Start Supabase MCP read-only and project-scoped. Use Playwright only for MAYA test/allowed domains.
- No browser cookies, CAPTCHA bypass, anti-detection, credential harvesting, uncontrolled shell/SQL, or external publishing without explicit user approval.

Do not stop at a plan. Continue the next unimplemented milestone, run tests, and report the files changed, commands run, tests passing/failing, and the exact secret variable names the owner must place in deployment settings. Never request or print secret values in chat.



---

## Source document: `README.md`

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

Open the frontend at [external address omitted in offline package] Use the clearly labelled local dev-user mode, create a project, add a room and brief, request a mock plan, then enqueue a mock media job. The API is at [external address omitted in offline package] and health check at `/healthz`. No external model, Supabase, or GPU call is made in mock mode. If Docker is unavailable, run the API locally with `cd backend && uv sync --extra dev && uv run uvicorn app.main:app --reload`; use the SQLite default in `.env`.

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



---

## Source document: `MAYA_OX_ALPHA_IMPLEMENTATION.md`

# MAYA AI — Ox Alpha Implementation Brief

## Mission

Build **MAYA AI**, a production-ready interior-design enhancement agent for homeowners, builders, and design teams. It must convert a user's room photos, drawings, requirements, and budget into visual concepts, edit instructions, material suggestions, cost-aware options, and a traceable project workspace.

Implement the skills below in the listed priority order. Do not build placeholders where a working open-source or free-tier implementation is practical. Make every AI/model integration replaceable through environment variables and provider adapters.

## Phase 1 repository baseline

The Phase 1 API is mounted at `/api/v1` and runs with zero keys through local SQLite (tests) or the Compose Postgres service. `SUPABASE_URL` is an Auth/Storage API URL, not a database URI; hosted Postgres requires a separate server-only `DATABASE_URL`. The initial Alembic migration is `backend/migrations/versions/0001_initial.py`; review `backend/db/rls_policies.sql` and run it only in the intended Supabase project. `DesignPlan` is strictly validated and contains `style`, `palette`, `camera_moves`, `scene_beats`, `narration`, and `constraints`. Heavy media processing is delegated to `worker/`, and the frontend must remain usable without provider credentials.

## 1. Frontend Skill: React Component Generation

### Required stack

- React + TypeScript + Vite (or Next.js App Router if the existing project already uses Next.js).
- Tailwind CSS, shadcn/ui-compatible primitives, Lucide icons, Framer Motion.
- TanStack Query for API state, Zustand for transient client state, React Hook Form + Zod for forms.
- Accessible keyboard navigation, responsive layout, loading, empty, error, and retry states for every async screen.

### Build these screens and components

1. **Landing / onboarding**: role choice (`homeowner`, `builder`, `designer`), sample room gallery, clear privacy explanation.
2. **Project workspace**: project switcher, room list, uploads, chat/brief panel, generation history, export panel.
3. **Room Studio**: image canvas, before/after comparison slider, generated alternatives, selection controls, prompt editor, regenerate button.
4. **Design Brief Wizard**: room type, dimensions, preferred style, materials, budget, occupants, accessibility needs, climate, builder notes.
5. **Builder Mode**: client-facing option board, finish schedule, revisions, approvals, estimate/export summary. Do not present AI output as construction-certified drawings.
6. **Model Settings**: provider, model, quality, aspect ratio, seed, ControlNet/reference strength, and cost/queue indicators.

### Component rules

- Organize by feature: `features/projects`, `features/studio`, `features/briefs`, `features/generation`, `components/ui`.
- Use typed API clients and reusable `ApiResult<T>` handling. Never put fetch calls directly inside presentational components.
- Preserve original uploads and generation provenance: model, model version, prompt version, seed, source assets, settings, time, and user selection.
- Use optimistic UI only for reversible actions. Confirm destructive actions such as deleting a project or asset.

## 2. Backend Skill: FastAPI / Python Architecture

### Required architecture

- Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2 async, Alembic, PostgreSQL/Supabase, Redis-compatible queue/cache.
- Package layout:

```text
backend/
  app/
    api/v1/            # routers only
    core/              # settings, security, logging, errors
    db/                # models, session, migrations
    schemas/           # Pydantic request/response types
    services/          # business workflows
    providers/         # LLM/image/video provider adapters
    workers/           # long-running generation jobs
    prompts/           # versioned system/template prompts
    tests/
```

### Implement

- JWT/session-auth middleware compatible with Supabase Auth; enforce owner/project membership on every route.
- Typed REST API under `/api/v1`; OpenAPI tags and stable response schemas.
- Background job flow for image/video generation: create job → queue → poll or websocket/SSE updates → persist result/provenance → notify UI.
- Idempotency keys for generation requests. Rate limits per authenticated user/project.
- Storage adapter for Supabase Storage or S3-compatible object storage; upload signed URLs, virus/file-type validation, image dimension limits.
- Structured logs with request IDs; no secret, prompt upload, or signed URL leakage in logs.
- Provider interfaces, so models can be changed without modifying API routes:

```python
class ImageGenerationProvider(Protocol):
    async def generate(self, request: ImageGenerationRequest) -> GenerationResult: ...

class VideoGenerationProvider(Protocol):
    async def generate(self, request: VideoGenerationRequest) -> GenerationResult: ...

class ChatProvider(Protocol):
    async def respond(self, messages: list[ChatMessage], tools: list[Tool]) -> ChatResult: ...
```

### Initial API endpoints

- `POST /projects`, `GET /projects`, `GET/PATCH/DELETE /projects/{id}`
- `POST /projects/{id}/rooms`, `POST /assets/upload-url`, `POST /assets/complete`
- `POST /briefs`, `PATCH /briefs/{id}`, `POST /briefs/{id}/enhance`
- `POST /generations/image`, `POST /generations/video`, `GET /jobs/{id}`, `POST /jobs/{id}/cancel`
- `GET /projects/{id}/generations`, `POST /generations/{id}/select`
- `POST /agent/chat`, `GET /exports/{project_id}/finish-schedule`

## 3. Prompt-Engineering Skill: MAYA Enhancement Engine

### Prompt system

- Keep prompts in versioned files, never inline in route handlers.
- Build prompts from structured fields, not an unbounded chat history.
- Store `prompt_template_version`, rendered prompt hash, safety decision, and model response metadata with each run.
- Use a strict JSON output schema for planning tasks and validate/repair once if output is invalid.

### Core system prompt behaviour

MAYA is a helpful interior-design visualisation and planning assistant. It asks only for missing information that materially affects the result. It distinguishes aesthetic suggestions from structural, electrical, plumbing, fire, accessibility, and building-code decisions. It must recommend consultation with a qualified local professional whenever work requires certification, approvals, or safety judgment. It must not invent dimensions, product availability, prices, or compliance claims.

### Enhancement pipeline

1. Normalize the brief and uploaded asset metadata.
2. Extract room elements and constraints (opening positions, dimensions provided by user, lighting, fixed elements, user budget).
3. Produce a concise `DesignPlan` JSON: style direction, palette, layout assumptions, materials, exclusions, and image-generation prompt.
4. Run safety/feasibility guardrails.
5. Generate one or more images/videos using selected provider settings.
6. Return explanation, assumptions, editable prompt, suggested next decisions, and limitations.

### Required output contracts

```json
{
  "summary": "string",
  "assumptions": ["string"],
  "style_tags": ["string"],
  "palette": [{"name":"string","hex":"#000000","role":"string"}],
  "materials": [{"category":"string","suggestion":"string","notes":"string"}],
  "layout_notes": ["string"],
  "image_prompt": "string",
  "negative_prompt": "string",
  "safety_notes": ["string"],
  "follow_up_questions": ["string"]
}
```

## 4. AI Image / Video Skill

### Provider adapters to support

Implement the adapters and UI capabilities below. A provider may be disabled when its credentials or self-hosted endpoint are absent; the rest of the app must still work.

| Capability | Preferred free/self-hostable route | Required controls |
|---|---|---|
| Text/image to image | FLUX.1 or SDXL via ComfyUI API | prompt, negative prompt, seed, aspect ratio, steps, guidance |
| Spatial conditioning | ControlNet via ComfyUI | reference, depth/canny/lineart mode, strength |
| Image-to-video | Stable Video Diffusion or LTX-Video via ComfyUI/API | source image, duration, motion, FPS, aspect ratio |
| Planning/chat | any OpenAI-compatible local endpoint such as Ollama | system prompt, JSON mode, temperature, context limit |

### Important rules

- Use ComfyUI workflow JSON files stored in `backend/app/providers/comfyui/workflows/`; fill only named input fields. Do not construct unsafe arbitrary graph payloads from user input.
- Add a `ComfyUIProvider` with health check, queue submit, history polling, asset download, cancellation where supported, and normalized errors.
- Treat GPU/model hosting as separate infrastructure. The web app must never attempt to run GPU inference in the browser or API process.
- Persist an immutable copy/version hash of each workflow used for a generation.
- Validate images for safe file types and cap file size before dispatching to models.
- Always identify renders as AI visualisations. Do not claim they are construction-ready drawings or guaranteed product matches.

## 5. Database Skill: Supabase/PostgreSQL Design

### Core tables

```text
profiles(id PK -> auth.users.id, display_name, role, created_at)
projects(id UUID PK, owner_id FK, name, client_name nullable, status, created_at, updated_at)
project_members(project_id FK, user_id FK, role, UNIQUE(project_id,user_id))
rooms(id UUID PK, project_id FK, name, room_type, dimensions_jsonb, created_at)
assets(id UUID PK, project_id FK, room_id nullable, owner_id FK, storage_path, mime_type, width, height, bytes, kind, created_at)
design_briefs(id UUID PK, project_id FK, room_id nullable, version, brief_jsonb, created_by, created_at)
generation_jobs(id UUID PK, project_id FK, room_id nullable, requested_by, kind, provider, model, status, input_jsonb, idempotency_key, created_at, started_at, completed_at, error_code nullable)
generation_results(id UUID PK, job_id FK, asset_id FK nullable, prompt_version, prompt_hash, workflow_hash nullable, seed nullable, output_jsonb, created_at)
design_options(id UUID PK, project_id FK, generation_result_id FK, name, selected_by nullable, selected_at nullable)
agent_conversations(id UUID PK, project_id FK, user_id FK, created_at)
agent_messages(id UUID PK, conversation_id FK, role, content, structured_jsonb nullable, created_at)
audit_events(id UUID PK, project_id FK nullable, actor_id nullable, action, entity_type, entity_id, metadata_jsonb, created_at)
```

### Database and security requirements

- UUID primary keys, UTC timestamps, foreign keys, indexes on every common filter/FK, soft delete only where recovery is needed.
- Use PostgreSQL Row Level Security. A user may read/write only projects they own or belong to; asset and generation policies must inherit project membership.
- Never expose the Supabase service role key to frontend clients.
- Store files in private buckets with short-lived signed URLs. Storage object paths must be project-scoped: `{project_id}/{room_id}/{asset_id}`.
- Write SQL migrations and an `RLS_POLICY_NOTES.md` that explains each policy.

## 6. UI/UX Design System Skill

### Required token hierarchy

- Define and document three layers: primitive tokens (base values), semantic tokens (meaning/context), and component tokens (specific component usage).
- Tokens must cover colour roles, typography, spacing, sizing, radii, borders, shadows, elevation, z-index, breakpoints, focus rings, transition duration/easing, and dark mode.
- Export CSS custom properties and map them into Tailwind. Components may not introduce raw colours, arbitrary spacing, or one-off type sizes unless a documented token is added first.

### MAYA visual system rules

- Use a calm, professional studio aesthetic suitable for client presentations; keep the primary action and current design decision visually dominant.
- Define semantic typography roles: `display`, `h1`, `h2`, `h3`, `body`, `body-sm`, `label`, `caption`, and `mono`. Load web fonts efficiently with fallbacks that prevent layout shift.
- Every interactive component must specify default, hover, focus-visible, active, disabled, loading, error, and empty states where applicable.
- Meet WCAG AA contrast, keyboard navigation, visible focus, target-size, and reduced-motion requirements.
- Before extending an existing frontend, extract and reuse its current tokens and component patterns rather than creating competing systems.

## 7. API Integration, OAuth, and Social Skill

### Identity and OAuth requirements

- Use Supabase Auth for first-party identity. For OAuth/OIDC social sign-in and third-party connections use authorisation code flow with PKCE.
- Perform token exchange and refresh only on trusted server-side components. Encrypt refresh tokens at rest; never put them in browser storage, URLs, logs, generated files, or chat context.
- Implement minimum scopes, explicit connection consent, account selection, expiry/refresh state, disconnect/revocation, and audit events.
- Verify webhook signatures/timestamps, deduplicate deliveries using provider event IDs, and process webhooks asynchronously.

### Provider adapter boundary

```python
class ExternalIntegrationProvider(Protocol):
    async def create_authorization_url(self, state: str) -> str: ...
    async def exchange_callback(self, code: str, state: str) -> ConnectedAccount: ...
    async def revoke(self, connection_id: UUID) -> None: ...
```

- Social/marketing APIs are optional. They must never block the core design workspace, receive client assets by default, or be called from the browser with secrets.

## 8. Video Editing and Post-production Skill

### Architecture

- Treat video conversion/editing as a worker job, not a frontend or synchronous API task.
- Inspect each input using `ffprobe`; validate allowed formats, duration, streams, codecs, dimensions, frame rate, and size before queueing.
- Create a typed, versioned `VideoEditRecipe` (trim, crop, scale, audio, captions, overlay, transitions). Generate FFmpeg filter graphs server-side from validated fields; never run user-provided shell commands.
- Preserve the original asset. Every derivative records source asset IDs, recipe version/hash, FFmpeg/MoviePy version, output checksum, duration, dimensions, and job ID.
- Use MoviePy only for short, deterministic overlay/composition jobs. Use FFmpeg for robust transforms and rendering. Use queued GPU providers for SVD/LTX/ComfyUI generative clips.
- Render factual text, labels, material names, prices, and captions as post-production overlays, never as model-generated in-frame text.

## 9. Vector Database, RAG, and Memory Skill

### Use cases and boundaries

- Start with structured project data and versioned markdown instructions. Add RAG only for owner-authorised content: uploaded documents, product/material catalogues, project briefs, and approved reference sources.
- Prefer PostgreSQL + pgvector in the existing Supabase data boundary. Evaluate Chroma/Qdrant/Weaviate/Milvus/Pinecone only if retrieval scale, isolation, or latency makes pgvector unsuitable.
- Keep four stores separate: user preferences, project decisions, conversation messages, and retrieved documents. Chat history alone is not durable memory.

### Required RAG schema and controls

```text
knowledge_documents(id, project_id, asset_id nullable, title, source_uri nullable, version, content_hash, status, created_at)
knowledge_chunks(id, document_id, project_id, ordinal, text, embedding, embedding_model, metadata_jsonb, created_at)
memory_items(id, owner_id, project_id nullable, kind, content, facts_jsonb, confidence, source_message_id nullable, expires_at nullable, created_at, updated_at)
retrieval_events(id, project_id, user_id, query_hash, result_ids_jsonb, model, created_at)
```

- Apply project/user authorization and RLS before retrieval and similarity ranking; no cross-project embedding search.
- Store source citation/chunk IDs with every RAG answer. Support document deletion, memory correction, expiry, and re-embedding on model change.
- Do not store sensitive personal data or client documentation in external vector/memory providers without explicit consent, retention limits, and a documented deletion path.

## 10. Testing, Containers, and Deployment Skill

### Required verification

- Frontend: lint, type check, unit/component tests, accessibility tests, and browser E2E tests.
- Backend: Ruff/format/type checks, Pytest, API-contract tests, authorization/RLS tests, migration tests, queue retry/cancellation tests, and provider-error tests.
- AI: prompt JSON-schema tests, retrieval evaluation set, generation input validation, and provenance persistence tests.
- CI must run all applicable checks on pull requests. Do not promote a deployment after failing checks.

### Deployment boundaries

- Dockerise API and worker services using multi-stage builds, non-root runtime users, pinned base images, `.dockerignore`, health checks, and no secrets embedded in images.
- Vercel is suitable for the React/Next frontend and preview deployments. Use preview-first workflow; production promotion needs an explicit owner decision.
- Deploy FastAPI, queues, object storage, and GPU workers as independent services. Do not run ComfyUI or video rendering inside a Vercel function.
- Hugging Face Spaces may host public demos or bounded experiments. Never use a public Space as the private production data store or expose service keys there.
- Document rollback, database-migration order, environment variable ownership, and health/monitoring checks.

## 11. Agentic AI, Tool Calling, and Orchestration Skill

- Build a durable state machine: `brief_validated → storyboard_planned → image_jobs → video_jobs → audio_jobs → preview_ready → publish_pending_approval → published | failed | cancelled`.
- Persist workflow and step records containing idempotency key, typed input/output, source assets, provider/model/workflow version, tool, retry count, actor, cost estimate, state, and error.
- Tools must have JSON schemas and a permission classification: `read`, `write_reversible`, `write_external`, or `destructive`. Recover safely after worker restarts; retry only idempotent steps.
- MAYA can autonomously plan, storyboard, and generate internal previews. It must pause for final user approval before posting externally, spending money, modifying connected accounts, deleting resources, or another irreversible side effect.
- Never execute raw LLM-provided shell, SQL, browser selector/URL, or ComfyUI graph input. Use server-side schemas, allowlists, and trusted adapters.

## 12. Performance Optimization Skill

- Define budgets for LCP, INP, CLS, JS bundle, image payload, API p95, database query time, queue wait, and media-render duration. Run Lighthouse in CI and monitor representative production metrics.
- Optimise Room Studio with responsive AVIF/WebP assets, thumbnails, lazy-loaded editing tools, canvas/list virtualisation, cancelled stale requests, and paginated generation history.
- Profile FastAPI, PostgreSQL, cache, queue, and workers with representative project sizes. Add indexes, batching, caching, or concurrency only where measured evidence identifies a bottleneck and invalidation is clear.

## 13. SEO and Marketing Automation Skill

- Keep public SEO pages separate from authenticated workspaces. Public pages need accurate metadata, canonical URLs, sitemap, robots controls, accessible content, and truthful structured data.
- Automations may research, analyse, create drafts, prepare editorial calendars, and compile reports. A human must approve external copy, client-facing claims, pricing, testimonials, competitor statements, paid campaigns, and publication.
- Connect Search Console, GA4, Bing, advertising, email, and social accounts only after explicit owner OAuth authorisation with minimal scopes and revocation. Keep analytics optional and separate from core workspace data.

## 14. Data Visualization and Chart.js Skill

- Use Chart.js for standard MAYA dashboards; use D3 only where a required interaction/layout cannot be expressed cleanly with Chart.js.
- Every chart requires a stated question, accurate units/time range, labels, accessible description, colour-safe encoding, tooltips, and text/table alternative.
- Build reusable charts for budget vs estimate, material quantities, generation status/duration, option comparisons, revision history, and marketing funnels. Apply project/role filters before aggregation.

## 15. Web Scraping and Browser Automation Skill

- Prefer official platform APIs. Use Playwright/browser automation only for MAYA E2E tests or a platform-permitted, user-authorised workflow.
- Run browser tasks in a separate worker with an allowed domain/route/action policy and no database-admin access. Do not store passwords, session cookies, or browser profiles in app tables or logs.
- Never bypass CAPTCHAs, anti-bot controls, MFA, rate limits, login restrictions, or platform terms.
- Before publishing through a browser/API, show the account, media, caption, tags, audience/visibility, and schedule for final confirmation; store an audit event plus outcome URL/ID.

## 16. Universal Skills and Tools Discovery

- Before beginning a major new capability, consult `MAYA_OX_ALPHA_SKILLS_TOOL_REGISTRY.md` and select the relevant live discovery queries.
- Use the Skills CLI to search and preview candidates. Review every skill before installing it; install only individual approved skills and keep the generated lockfile plus a decision record in source control.
- Every skill, MCP server, CLI, API, model provider, or worker must have a tool record describing purpose, source/version, data classification, permissions, credential owner, approval, audit events, and rollback.
- Do not enable CAPTCHA bypass, anti-detection, MFA bypass, credential harvesting, rate-limit evasion, or any other mechanism intended to evade platform controls.

## 17. Free-First Build Configuration

- Follow `MAYA_FREE_STACK_AND_TOOLS.md` for the approved free-first APIs, CLIs, MCPs, secret boundaries, and phase order.
- The Phase 1 build must work with mock chat/media providers and no paid API or GPU. Gemini is optional for structured planning; ComfyUI/ZeroGPU is a limited prototype adapter only.
- Use Supabase for initial database/auth/storage, Cloudflare for frontend preview/deployment, and server-side secrets only.

## Environment Variables

Create `.env.example` without secrets:

```dotenv
APP_ENV=development
DATABASE_URL=
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
SUPABASE_STORAGE_BUCKET=maya-assets
REDIS_URL=
COMFYUI_BASE_URL=
OLLAMA_BASE_URL=
OLLAMA_MODEL=
JWT_AUDIENCE=authenticated
SENTRY_DSN=
MAX_UPLOAD_MB=20
```

## Quality Gate / Definition of Done

- TypeScript and Python type checks pass; linting and tests pass in CI.
- A signed-in user can create a project, upload a room image, submit a brief, start a generation job, see live job status, view/save a result, and select an option.
- A user cannot read another user's project, asset, brief, or generation by changing an ID in the URL/API request.
- Failures from missing GPU/provider, invalid asset, timeout, and queue overload are gracefully explained and retained in job history.
- Mobile and desktop layouts are usable; key actions are keyboard-accessible.
- README contains local setup, Supabase setup, ComfyUI/self-hosted GPU setup, migrations, tests, and deployment variables.

## Implementation Order

1. Inspect the existing repo and preserve its conventions.
2. Add environment schema, database migrations, RLS, authentication, and storage.
3. Build typed FastAPI API and job queue with mocked provider tests.
4. Add ComfyUI/Ollama adapters and versioned prompt/workflow files.
5. Build the React workspace, studio, and job-status UI.
6. Test the full upload → brief → generation → result → selection path; document deployment.

Do not commit credentials, model weights, generated private uploads, or Supabase service-role keys.



---

## Source document: `MAYA_OX_ALPHA_SKILLS_CATALOG.md`

# MAYA AI — skills.sh Skill Catalogue for Ox Alpha

## Purpose

This file is the curated skills.sh integration plan for **MAYA AI**: an interior-design visualisation and enhancement platform for homeowners, builders, and designers. Ox Alpha must read this file together with `MAYA_OX_ALPHA_IMPLEMENTATION.md` before changing the repository.

This is deliberately **not** a bulk copy of the skills.sh directory. skills.sh is a large community registry; importing every skill would create duplicate instructions, conflicting architecture, unreviewed dependencies, and unnecessary security risk. Use only the entries selected here, review their source before installation, and preserve the existing repository's conventions.

## Owner-approved Phase 1 installs

These are the only skills approved for installation in this execution. Preview each skill first, then install one at a time. Record a successful install in `docs/skill-decisions.md`; if a source is unavailable, record the skip and continue.

| Source | Skill names |
|---|---|
| `vercel-labs/agent-skills` | `vercel-react-best-practices`, `vercel-composition-patterns`, `web-design-guidelines` |
| `fastapi-practices/skills` | `fba` |
| `supabase/agent-skills` | `supabase`, `supabase-postgres-best-practices` |
| `wshobson/agents` | `prompt-engineering-patterns`, `design-system-patterns`, `rag-implementation` |
| `anthropics/skills` | `webapp-testing`, `mcp-builder` |
| `docker/skills` | `docker-project-foundations`, `docker-build-strategies` |
| `addyosmani/web-quality-skills` | `performance` |

Review-only: `openai/codex-plugin-cc` → `gpt-5-4-prompting`; it is not approved for installation.

Policy: preview before install; record decision in docs/skill-decisions.md; never --all

## How Ox Alpha must use this catalogue

1. Inspect the project first (`README`, package manifests, backend configuration, existing agent instructions, CI, and deployment files).
2. Treat the **Core** rows as guidance to apply during implementation. Do not blindly install them if equivalent instructions already exist.
3. Install a skill only after reviewing its `SKILL.md`, repository licence, security-audit status, required tools, and any scripts it executes.
4. Never install a skill that requests credentials, modifies cloud resources, installs model weights, or exposes a public endpoint without explicit project-owner approval.
5. Keep skills in a versioned project-owned directory such as `.agents/skills/` when the target agent supports it; otherwise preserve this file as the source-of-truth implementation guide.
6. Pin project dependencies independently of skills. A skill is procedural guidance, not an approved production dependency.

## Core Skills — use now

| Area | skills.sh source | Install command | Apply to MAYA AI |
|---|---|---|---|
| React performance | `vercel-labs/agent-skills` → `vercel-react-best-practices` | `npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices` | Prevent waterfalls, unnecessary client code/re-renders, and excessive bundles in Room Studio and project dashboards. |
| Component architecture | `vercel-labs/agent-skills` → `vercel-composition-patterns` | `npx skills add vercel-labs/agent-skills --skill vercel-composition-patterns` | Build composable workspace, canvas toolbar, option-card, modal, and form component APIs. |
| UI library | `shadcn/ui` → `shadcn` | `npx skills add shadcn/ui --skill shadcn` | Use accessible, themeable primitives with Tailwind for the interior-design workspace. |
| React testing | `anthropics/skills` → `webapp-testing` | `npx skills add anthropics/skills --skill webapp-testing` | Add component, integration, and end-to-end coverage for upload, brief, generation, and selection flows. |
| FastAPI layering | `fastapi-practices/skills` → `fba` | `npx skills add fastapi-practices/skills --skill fba` | Keep routers, services, CRUD/data access, schemas, models, tests, and plugins separate. |
| FastAPI implementation | `janjaszczak/cursor` → `python-backend-fastapi` | `npx skills add janjaszczak/cursor --skill python-backend-fastapi` | Use Pydantic v2 contracts, Alembic migrations, request tracing, and verifiable endpoint work. |
| Supabase platform | `supabase/agent-skills` → `supabase` | `npx skills add supabase/agent-skills --skill supabase` | Auth, private storage, migrations, client use, realtime status, and Supabase CLI/MCP integration. |
| Supabase/Postgres design | `supabase/agent-skills` → `supabase-postgres-best-practices` | `npx skills add supabase/agent-skills --skill supabase-postgres-best-practices` | Schema, indexing, connection handling, query performance, and Row Level Security (RLS). |
| Prompt contracts | `openai/codex-plugin-cc` → `gpt-5-4-prompting` | `npx skills add openai/codex-plugin-cc --skill gpt-5-4-prompting` | Write concise versioned prompts with explicit task, output schema, grounding, and verification rules. |
| Prompt reliability | `wshobson/agents` → `prompt-engineering-patterns` | `npx skills add wshobson/agents --skill prompt-engineering-patterns` | Build MAYA's brief-to-design-plan workflow, prompt tests, fallbacks, metrics, and context limits. |
| Typed LLM outputs | `sickn33/agentic-awesome-skills` → `llm-structured-output` | `npx skills add sickn33/agentic-awesome-skills --skill llm-structured-output` | Enforce JSON Schema/Pydantic validation for design plans; retry a failed output at most once. |
| ComfyUI workflow integration | `comfy-org/comfy-skills` → `comfy` | `npx skills add comfy-org/comfy-skills --skill comfy` | Use workflow templates, named input overrides, async generation jobs, and signed-result handling. |

## Optional Skills — use only when the feature is scheduled

| Feature trigger | skills.sh source | Install command | Boundary |
|---|---|---|---|
| Detailed React component work | `axross/skills` → `react-component-development` | `npx skills add axross/skills --skill react-component-development` | Component contracts, state placement, loading/error states, and testability. Do not let it override repository style. |
| Full frontend review | `borghei/claude-skills` → `senior-frontend` | `npx skills add borghei/claude-skills --skill senior-frontend` | Use for UI architecture/performance audits, not routine styling changes. |
| FastAPI + React baseline | `vanducng/skills` → `fastreact` | `npx skills add vanducng/skills --skill fastreact` | Reference only if scaffolding a fresh app; do not replace MAYA's chosen architecture. |
| Prompt template design | `oakoss/agent-skills` → `prompt-engineering` | `npx skills add oakoss/agent-skills --skill prompt-engineering` | Use for multimodal prompt templates, agent loops, and prompt evaluation. |
| Context/memory design | `sickn33/agentic-awesome-skills` → `context-engineering` | `npx skills add sickn33/agentic-awesome-skills --skill context-engineering` | Use when adding project memory/RAG; define retention, provenance, and deletion rules first. |
| SDXL and ControlNet prompting | `inbharatai/claude-skills` → `stable-diffusion-helper` | `npx skills add inbharatai/claude-skills --skill stable-diffusion-helper` | Use for SDXL, LoRA, ControlNet, and ComfyUI prompt/workflow design. |
| Advanced local ComfyUI | `g1joshi/agent-skills` → `comfyui` | `npx skills add g1joshi/agent-skills --skill comfyui` | Use only after a reviewed self-hosted GPU/ComfyUI endpoint exists. |
| LTX Video | `digitalsamba/claude-code-video-toolkit` → `ltx2` | `npx skills add digitalsamba/claude-code-video-toolkit --skill ltx2` | Use only for the image-to-video feature. Queue jobs asynchronously and retain provenance. |
| Video generation | `tippyentertainment/skills` → `comfyui-video-generator` | `npx skills add tippyentertainment/skills --skill comfyui-video-generator` | Use only for verified ComfyUI video workflows; cap duration and GPU budget. |
| Schema QA | `vanman2024/ai-dev-marketplace` → `schema-validation` | `npx skills add vanman2024/ai-dev-marketplace --skill schema-validation` | Run before deploying Supabase/Postgres migrations and RLS changes. |
| Backend test expansion | `supercent-io/skills-template` → `backend-testing` | `npx skills add supercent-io/skills-template --skill backend-testing` | Add API, database, authorization, queue, and failure-path tests. |

## High-value Expansion — add when the capability is scheduled

### 6. UI/UX design-system skills

| Skills.sh source | Install command | Apply to MAYA AI |
|---|---|---|
| `vercel-labs/agent-skills` → `web-design-guidelines` | `npx skills add vercel-labs/agent-skills --skill web-design-guidelines` | Enforce usable web-interface spacing, typography, interactions, keyboard access, and visual hierarchy. |
| `wshobson/agents` → `design-system-patterns` | `npx skills add wshobson/agents --skill design-system-patterns` | Build primitive → semantic → component tokens, light/dark themes, and scalable component variants. |
| `supercent-io/skills-template` → `frontend-design-system` | `npx skills add supercent-io/skills-template --skill frontend-design-system` | Define responsive layout, token, motion, and accessibility handoff rules. |
| `jacob-balslev/skills` → `typography-system` | `npx skills add jacob-balslev/skills --skill typography-system` | Create a restrained type scale, semantic typography tokens, WOFF2 loading, and layout-shift-safe font fallbacks. |
| `arvindrk/extract-design-system` → `extract-design-system` | `npx skills add arvindrk/extract-design-system --skill extract-design-system` | Extract existing project tokens/components before introducing a second visual language. |
| `pbakaus/impeccable` → `critique` and `polish` | `npx skills add pbakaus/impeccable --skill critique --skill polish` | Use only as a final visual review pass after functional and accessibility tests pass. |

### 7. API integration, OAuth, and social APIs

| Skills.sh source | Install command | Apply to MAYA AI |
|---|---|---|
| `supercent-io/skills-template` → `authentication-setup` | `npx skills add supercent-io/skills-template --skill authentication-setup` | Implement OAuth 2.0/OIDC, sessions/JWT, refresh-token rotation, RBAC, audit logs, and social sign-in rules. |
| `secondsky/claude-skills` → `api-authentication` | `npx skills add secondsky/claude-skills --skill api-authentication` | Review API authentication choices and server-to-server API-key handling. |
| `thedaviddias/ux-patterns-for-developers` → `social-login` | `npx skills add thedaviddias/ux-patterns-for-developers --skill social-login` | Add Google/Apple/GitHub sign-in only where it improves onboarding; retain email/password or magic-link fallback when needed. |
| `facebook/agentic-tools` → `api-integration` | `npx skills add facebook/agentic-tools --skill api-integration` | Optional Meta/Instagram/WhatsApp integration via a dedicated backend adapter. |
| `facebook/agentic-tools` → `webhook-setup` and `search-docs` | `npx skills add facebook/agentic-tools --skill webhook-setup --skill search-docs` | Optional verified webhook handling and current Meta-platform documentation lookup. |
| `fetcher-sh/fetcher-skills` → `fetcher` | `npx skills add fetcher-sh/fetcher-skills --skill fetcher` | Optional separate data-collection provider; do not use it for personal data without terms, privacy, and legal review. |

### 8. Video editing, FFmpeg, and MoviePy

| Skills.sh source | Install command | Apply to MAYA AI |
|---|---|---|
| `bryanwhl/ffmpeg-video-editor` → `ffmpeg-video-editor` | `npx skills add bryanwhl/ffmpeg-video-editor --skill ffmpeg-video-editor` | Probe video first, then perform server-side trim, transcode, crop, concatenate, audio, and thumbnail jobs with FFmpeg. |
| `digitalsamba/claude-code-video-toolkit` → `moviepy` | `npx skills add digitalsamba/claude-code-video-toolkit --skill moviepy` | Add deterministic captions, labels, materials, and price overlays after AI generation; do not render factual text inside diffusion generations. |
| `digitalsamba/claude-code-video-toolkit` → `ltx2` | `npx skills add digitalsamba/claude-code-video-toolkit --skill ltx2` | Generate short image-to-video concept clips only through queued GPU jobs. |
| `tippyentertainment/skills` → `comfyui-video-generator` | `npx skills add tippyentertainment/skills --skill comfyui-video-generator` | Use reviewed ComfyUI video workflows, duration limits, and generation provenance. |
| `supadata-ai/skills` → `supadata` | `npx skills add supadata-ai/skills --skill supadata` | Optional video transcript/metadata ingestion; assess pricing and third-party data terms first. |

### 9. Vector database, RAG, and memory

| Skills.sh source | Install command | Apply to MAYA AI |
|---|---|---|
| `wshobson/agents` → `rag-implementation` | `npx skills add wshobson/agents --skill rag-implementation` | Build document ingestion, metadata filters, hybrid retrieval, evaluation, and a pgvector-first option. |
| `borghei/claude-skills` → `rag-architect` | `npx skills add borghei/claude-skills --skill rag-architect` | Choose pgvector, Chroma, Qdrant, Weaviate, Milvus, or Pinecone only after scale/latency/privacy comparison. |
| `muratcankoylan/agent-skills-for-context-engineering` → `memory-systems` | `npx skills add muratcankoylan/agent-skills-for-context-engineering --skill memory-systems` | Design short-term context, project memory, user preferences, retrieval, expiry, and correction flows. |
| `terminalskills/skills` → `agent-memory` | `npx skills add terminalskills/skills --skill agent-memory` | Use repository `AGENTS.md` and small reviewable memory before building semantic/vector memory. |
| `t4sh/skills4sh` → `agent-memory` | `npx skills add t4sh/skills4sh --skill agent-memory` | Optional Git-tracked `.agent-memory/` for durable decisions, open work, and implementation history. |
| `nousresearch/hermes-agent` → `chroma` | `npx skills add nousresearch/hermes-agent --skill chroma` | Optional self-hosted vector store only if PostgreSQL/pgvector is insufficient. |

### 10. Testing and deployment

| Skills.sh source | Install command | Apply to MAYA AI |
|---|---|---|
| `anthropics/skills` → `webapp-testing` | `npx skills add anthropics/skills --skill webapp-testing` | Maintain browser/unit/integration coverage for the React experience. |
| `supercent-io/skills-template` → `backend-testing` | `npx skills add supercent-io/skills-template --skill backend-testing` | Test FastAPI API contracts, database authorization, and provider failure paths. |
| `dhruvanbhalara/skills` → `ci-cd` | `npx skills add dhruvanbhalara/skills --skill ci-cd` | GitHub Actions quality gates: lint, type checks, tests, build, migration checks, and security scan. |
| `docker/skills` → `docker-project-foundations` | `npx skills add docker/skills --skill docker-project-foundations` | Dockerise web, API, worker, and local dependencies; establish safe `.dockerignore` rules. |
| `docker/skills` → `docker-build-strategies` | `npx skills add docker/skills --skill docker-build-strategies` | Use multi-stage, small, reproducible production images and build cache safely. |
| `vercel-labs/agent-skills` → `deploy-to-vercel` | `npx skills add vercel-labs/agent-skills --skill deploy-to-vercel` | Deploy the frontend as previews first; promote only after user approval and green checks. |
| `openai/plugins` → `deployments-cicd` | `npx skills add openai/plugins --skill deployments-cicd` | Add Vercel deploy/inspect/promote/rollback and Git-based deployment practices. |
| `huggingface/skills` → `huggingface-spaces` | `npx skills add huggingface/skills --skill huggingface-spaces` | Use for public demos or bounded GPU experiments, never as the primary private production datastore. |

## High-value implementation rules

### UI/UX tokens

- Define primitive tokens (base colour, spacing, type, radius, shadow), semantic tokens (surface, text, action, feedback), then component tokens. Components must consume semantic/component tokens rather than raw hex values or one-off spacing.
- Publish tokens as CSS custom properties plus Tailwind mappings. Include a type scale, line heights, letter spacing, responsive breakpoints, focus rings, motion durations/easing, and dark mode from the start.
- Run visual review only after the layout has all loading, empty, error, invalid, focus, and disabled states.

### OAuth and external APIs

- Use OAuth 2.0/OIDC authorisation code flow with PKCE for browser clients. Handle callbacks and token exchange on the backend; encrypt refresh tokens at rest and never log or return them to the browser.
- Scope every integration to the minimum permissions, retain consent/audit events, support disconnect/revocation, validate webhook signatures, and deduplicate webhook events.
- Implement social providers behind `SocialProvider` adapters. They are optional integrations, never requirements for core MAYA workspaces.

### Video processing

- Run `ffprobe` metadata inspection before any FFmpeg command. Construct FFmpeg filter graphs from typed server-side options; never pass a user string directly to a shell command.
- Keep original media immutable and use queued, versioned derivative jobs. Include source asset IDs, edit recipe, tool version, duration, output dimensions, and checksum in provenance.
- MoviePy is suitable for deterministic overlays; large or multi-clip jobs belong in FFmpeg/worker infrastructure.

### RAG and memory

- Start with project instructions and structured PostgreSQL records. Add RAG only for approved documents such as product catalogues, uploaded briefs, standards that the user is authorised to use, and material guidance.
- Use project/user metadata filters and RLS before vector similarity ranking. Store document/version/chunk/embedding model/citation provenance; support deletion and re-embedding.
- Separate durable user preferences, project decisions, chat history, and retrieved reference documents. Add retention periods, consent, correction, and deletion controls before storing personal information.

### Testing and deployment

- CI must run formatting, linting, type checks, unit/integration tests, migration/RLS tests, dependency security checks, and a build. Preview deployments are mandatory before production promotion.
- Use Docker images for API/worker reproducibility. Vercel is appropriate for the frontend; deploy GPU/media workers separately. Hugging Face Spaces are optional demonstration or experiment environments only.
- Never deploy a database migration, production token, or cloud resource change from an unreviewed skill or agent action.

### 11. Agentic AI, tool-calling, and orchestration

| Skills.sh source | Install command | Apply to MAYA AI |
|---|---|---|
| `inngest/inngest-skills` → `inngest-agents` | `npx skills add inngest/inngest-skills --skill inngest-agents` | Durable multi-step tool calls, retries, waits, approvals, and realtime progress. |
| `dannymac180/skills` → `codex-dynamic-workflows` | `npx skills add dannymac180/skills --skill codex-dynamic-workflows` | Supervised orchestration plans and verification artifacts. |
| `obra/superpowers` → `writing-plans`, `executing-plans`, `verification-before-completion` | `npx skills add obra/superpowers --skill writing-plans --skill executing-plans --skill verification-before-completion` | Plan, run, and verify complex agent workflows. |

### 12. Performance optimization

| Skills.sh source | Install command | Apply to MAYA AI |
|---|---|---|
| `addyosmani/web-quality-skills` → `performance` | `npx skills add addyosmani/web-quality-skills --skill performance` | Lighthouse/Core Web Vitals budgets, rendering, image/font, cache, and script optimisation. |
| `cloudflare/skills` → `web-perf` | `npx skills add cloudflare/skills --skill web-perf` | Diagnose network chains, rendering blocks, layout shift, caching, and field metrics. |
| `openai/plugins` → `web-perf` | `npx skills add openai/plugins --skill web-perf` | Web performance review and metric interpretation. |
| `olehsvyrydov/ai-development-team` → `performance-engineer` | `npx skills add olehsvyrydov/ai-development-team --skill performance-engineer` | Frontend, API, database, cache, load-test, and CI-budget tuning. |
| `stareezy-1/frontend-architecture-skill` → `frontend-lighthouse` | `npx skills add stareezy-1/frontend-architecture-skill --skill frontend-lighthouse` | CI performance gate. |

### 13. SEO and marketing automation

| Skills.sh source | Install command | Apply to MAYA AI |
|---|---|---|
| `aaron-he-zhu/aaron-marketing-skills` → `technical-seo-checker` | `npx skills add aaron-he-zhu/aaron-marketing-skills --skill technical-seo-checker` | Crawl, indexing, structured-data, mobile, security, and SEO audit. |
| `reason-machines/marketing-skills` → `seo-content-marketing-skill-suite` | `npx skills add reason-machines/marketing-skills --skill seo-content-marketing-skill-suite` | Optional keyword, SERP, content-audit, brief, and editorial-calendar workflows. |
| `reason-machines/data-skills` → `web-analytics-agent-skill` | `npx skills add reason-machines/data-skills --skill web-analytics-agent-skill` | Optional authorised Search Console, GA4, and Bing reporting. |
| `i-onlabs/claude-code-skills` → `marketing-demand-acquisition` | `npx skills add i-onlabs/claude-code-skills --skill marketing-demand-acquisition` | Optional growth/campaign/lead workflow planning. |

### 14. Data visualization and Chart.js

| Skills.sh source | Install command | Apply to MAYA AI |
|---|---|---|
| `nickcrew/claude-cortex` → `chart-builder` | `npx skills add nickcrew/claude-cortex --skill chart-builder` | Chart.js/Python chart selection and configuration. |
| `anthropics/knowledge-work-plugins` → `data-visualization` | `npx skills add anthropics/knowledge-work-plugins --skill data-visualization` | Accessible chart-selection and data-storytelling rules. |
| `claude-office-skills/skills` → `chart-designer` | `npx skills add claude-office-skills/skills --skill chart-designer` | Chart.js/ECharts configuration. |
| `openai/plugins` → `d3-data-visualization` | `npx skills add openai/plugins --skill d3-data-visualization` | Bespoke interactive visualisations only when Chart.js cannot express them. |

### 15. Web scraping and browser automation

| Skills.sh source | Install command | Apply to MAYA AI |
|---|---|---|
| `lackeyjb/playwright-skill` → `playwright-skill` | `npx skills add lackeyjb/playwright-skill --skill playwright-skill` | Focused Playwright scripts for MAYA E2E tests and authorised workflows. |
| `openai/plugins` → `agent-browser` | `npx skills add openai/plugins --skill agent-browser` | Reviewed browser automation with explicit allowed domains/actions. |
| `vercel-labs/agent-browser` → `agent-browser` | `npx skills add vercel-labs/agent-browser --skill agent-browser` | Optional browser QA and permitted action workflows. |
| `github/awesome-copilot` → `webapp-testing` | `npx skills add github/awesome-copilot --skill webapp-testing` | Playwright test/debug, responsive, console, network, and screenshot workflows. |
| `sickn33/agentic-awesome-skills` → `browser-automation` | `npx skills add sickn33/agentic-awesome-skills --skill browser-automation` | Choose Playwright/Puppeteer/Selenium by authorised use case. |

## Ultimate-level implementation rules

### Agent tool calling and orchestration

- Implement a durable state machine: `brief_validated → storyboard_planned → image_jobs → video_jobs → audio_jobs → preview_ready → publish_pending_approval → published/failed`.
- Persist typed tool inputs/outputs, idempotency key, model/workflow version, source IDs, attempts, actor, cost estimate, and error. Each step must be independently resumable.
- Classify tools as `read`, `write_reversible`, `write_external`, or `destructive`. The agent may prepare drafts/previews autonomously, but requires explicit final approval before external publishing, payments, connected-account changes, or irreversible actions.
- Never execute raw LLM-provided shell, SQL, browser selectors/URLs, or ComfyUI graphs; apply server-side schemas and allowlists.

### Performance, SEO, charts, and browser automation

- Set budgets for LCP, INP, CLS, JS/image payload, API p95, query time, queue wait, and render time. Use Lighthouse CI plus representative production monitoring.
- Keep public marketing/SEO pages separate from authenticated workspaces. Marketing automation creates drafts/reports only; a human must approve external claims and publication.
- Charts require correct units, labels, accessible descriptions, colour-safe encoding, and a text/table alternative. Filter data by authorised project/role before aggregation.
- Prefer official social APIs. Browser automation is for MAYA E2E testing or platform-permitted, user-authorised flows only. Never bypass CAPTCHAs, MFA, anti-bot controls, rate limits, login restrictions, or platform terms; never store passwords/cookies in application data.
- For any publish action, show account, media, caption, tags, visibility, and schedule for confirmation, then retain an audit event and returned URL/ID.

## Review-only Skills — never auto-install

For every major capability phase, use `MAYA_OX_ALPHA_SKILLS_TOOL_REGISTRY.md` and its JSON counterpart to perform live skills.sh discovery. It covers product, agent, frontend, design, backend, AI, media, social, security, observability, deployment, and growth-tool searches plus a tool-permission policy.

| Source | Why it is useful | Required review before use |
|---|---|---|
| `reason-machines/mcp-skills` → `comfyui-mcp-agent` | Broad MCP control plane for ComfyUI, models, workflows, custom nodes, and media tools. | It exposes many powerful operations. Inspect every tool, disable installation/model-management permissions by default, restrict it to a dedicated generation service, and never grant production credentials to an agent automatically. |
| `reason-machines/security-skills` → `supabase-pentest-skills` | Can audit RLS, IDOR, storage, and auth configuration. | Security testing only in an authorised non-production environment; do not use routines that collect credentials or attack systems outside the project's control. |
| `thinkfleetai/thinkfleet-engine` → `fal-api` | Provider abstraction for hosted FLUX/SDXL/video. | Not a free self-hosted route; use only after the owner accepts provider pricing, terms, and data-handling conditions. |
| `lijingpan/video-uploader` → `video-uploader` | Playwright-based social video uploading. | Do not use anti-detection or bypass platform rules; prefer official APIs and an explicit pre-publish approval flow. |

## MAYA implementation rules derived from the skills

### Frontend

- React + TypeScript, Tailwind, accessible UI primitives, typed API client, TanStack Query for server state, and clear pending/error/retry states.
- Do not fetch inside visual components. Preserve original assets and generation provenance in the UI.
- Keep the builder-facing option board separate from technical/certification claims.

### Backend and data

- FastAPI API routes stay thin; services orchestrate business actions; database access is isolated; Pydantic v2 governs API and LLM contracts.
- Use Supabase Auth and private Storage; enforce PostgreSQL RLS on every project-scoped table and object path.
- Generation is always an idempotent background job with persistent status and safe cancellation.

### Prompt and AI generation

- Version prompt templates and ComfyUI workflow JSON. Persist prompt version/hash, workflow hash, model, seed, inputs, outputs, safety notes, and owner/project.
- Design-plan responses must validate against JSON Schema before any database write or generation dispatch.
- Flux, SDXL, ControlNet, SVD, and LTX-Video run behind provider adapters. The app must keep working when a provider or GPU endpoint is unavailable.
- Renders must be labelled AI visualisations, not construction-certified drawings or guaranteed product matches.

### Security and operational limits

- No service-role key in the browser, no secrets/model weights/private uploads in Git, no arbitrary user-supplied ComfyUI graph execution.
- Require short-lived signed upload/download URLs, file validation, rate limits, per-project authorization, structured logs with request IDs, and an audit trail.
- Keep the web/API service separate from GPU workers and restrict worker permissions.
- Use PKCE, minimum OAuth scopes, encrypted refresh tokens, webhook signature verification, and integration revocation for all third-party APIs.
- Do not send private project assets, client briefs, or user preferences to social, vector, or hosted-media providers without explicit informed consent and documented retention rules.

## Acceptance checklist for Ox Alpha

- [ ] Existing repository conventions were inspected and preserved.
- [ ] Every imported skill has a recorded source, version/commit, licence check, and owner approval.
- [ ] Upload → design brief → validated plan → queued generation → result → selected option works end-to-end.
- [ ] A user cannot access another user's project/assets/briefs/jobs by changing an identifier.
- [ ] Provider timeout, invalid file, queue overload, and unavailable GPU display recoverable user messages.
- [ ] Tests cover RLS/authorization, API contracts, job idempotency, prompt-schema validation, and the core browser flow.
- [ ] Design tokens cover typography, spacing, colour roles, radii, shadows, motion, responsive breakpoints, dark mode, and focus/error/disabled states.
- [ ] OAuth tokens, API secrets, social webhooks, and revoked connections are handled only server-side and covered by tests.
- [ ] Video jobs probe inputs, use validated typed edit recipes, preserve originals, and store output provenance.
- [ ] RAG/memory uses project-scoped filtering, citations, retention/deletion controls, and no cross-user retrieval.
- [ ] CI builds reproducible Docker images and blocks production deployment until preview checks pass.
- [ ] Agent workflows are durable, idempotent, observable, and require approval before external publishing or irreversible actions.
- [ ] Performance budgets/Lighthouse CI cover Room Studio, public pages, APIs, queues, and GPU workers.
- [ ] SEO/marketing has human review gates and authorised analytics connections.
- [ ] Charts are accessible, accurate, and scoped to authorised data.
- [ ] Browser automation has an allowed-domain/action policy and never bypasses platform security.
- [ ] README documents exact installation, environment variables, migrations, provider setup, test commands, and deployment.

## Project information still required for direct implementation

To apply this inside Ox Alpha rather than provide it as a package, provide one of the following:

1. the Ox Alpha project/repository URL with access, or
2. a ZIP export of the project, or
3. the project root files: `README`, `package.json`, backend dependency file, database/schema files, `.env.example`, and any existing `AGENTS.md`/skill instructions.

Also provide the desired deployment target if already chosen. The current documented direction is cloud-hosted, low-cost/free where practical, with GPU generation hosted separately from the web application.

For the exact free-first APIs, CLIs, MCPs, secret list, and initial build sequence, read `MAYA_FREE_STACK_AND_TOOLS.md`.



---

## Source document: `MAYA_OX_ALPHA_SKILLS_CATALOG.json`

{
  "$schema": "[external address omitted in offline package]
  "name": "maya-ox-alpha-skills-catalog",
  "version": "2026-10-17",
  "approved_install": [
    {"source":"vercel-labs/agent-skills","skills":["vercel-react-best-practices","vercel-composition-patterns","web-design-guidelines"]},
    {"source":"fastapi-practices/skills","skills":["fba"]},
    {"source":"supabase/agent-skills","skills":["supabase","supabase-postgres-best-practices"]},
    {"source":"wshobson/agents","skills":["prompt-engineering-patterns","design-system-patterns","rag-implementation"]},
    {"source":"anthropics/skills","skills":["webapp-testing","mcp-builder"]},
    {"source":"docker/skills","skills":["docker-project-foundations","docker-build-strategies"]},
    {"source":"addyosmani/web-quality-skills","skills":["performance"]}
  ],
  "review_only": [{"source":"openai/codex-plugin-cc","skills":["gpt-5-4-prompting"]}],
  "policy": "preview before install; record decision in docs/skill-decisions.md; never --all",
  "project": {
    "name": "MAYA AI",
    "purpose": "Interior-design visualisation and enhancement platform for homeowners, builders, and designers",
    "constraints": [
      "cloud-hosted",
      "prefer low-cost or free infrastructure where practical",
      "keep GPU generation separate from the web/API service",
      "do not commit credentials, private assets, or model weights"
    ]
  },
  "usage_policy": {
    "read_markdown_catalog_first": true,
    "review_skill_before_install": true,
    "record_source_version_and_license": true,
    "never_auto_install_review_only": true,
    "preserve_existing_repository_conventions": true
  },
  "live_discovery_registry": {
    "markdown": "MAYA_OX_ALPHA_SKILLS_TOOL_REGISTRY.md",
    "json": "MAYA_OX_ALPHA_SKILLS_TOOL_REGISTRY.json",
    "required_before_major_capability": true,
    "install_policy": "search, preview, review, record decision, then install one approved skill"
  },
  "free_first_stack": {
    "markdown": "MAYA_FREE_STACK_AND_TOOLS.md",
    "json": "MAYA_FREE_STACK_AND_TOOLS.json",
    "starter_prompt": "OX_ALPHA_START_MAYA.md"
  },
  "core_skills": [
    {"source":"vercel-labs/agent-skills","skill":"vercel-react-best-practices","area":"frontend-performance"},
    {"source":"vercel-labs/agent-skills","skill":"vercel-composition-patterns","area":"component-architecture"},
    {"source":"shadcn/ui","skill":"shadcn","area":"ui-primitives"},
    {"source":"anthropics/skills","skill":"webapp-testing","area":"frontend-testing"},
    {"source":"fastapi-practices/skills","skill":"fba","area":"fastapi-architecture"},
    {"source":"janjaszczak/cursor","skill":"python-backend-fastapi","area":"fastapi-implementation"},
    {"source":"supabase/agent-skills","skill":"supabase","area":"auth-storage-migrations"},
    {"source":"supabase/agent-skills","skill":"supabase-postgres-best-practices","area":"schema-rls-performance"},
    {"source":"openai/codex-plugin-cc","skill":"gpt-5-4-prompting","area":"prompt-contracts"},
    {"source":"wshobson/agents","skill":"prompt-engineering-patterns","area":"prompt-reliability"},
    {"source":"sickn33/agentic-awesome-skills","skill":"llm-structured-output","area":"typed-llm-output"},
    {"source":"comfy-org/comfy-skills","skill":"comfy","area":"comfyui-workflows"}
  ],
  "optional_skills": [
    {"source":"axross/skills","skill":"react-component-development","trigger":"component feature or refactor"},
    {"source":"borghei/claude-skills","skill":"senior-frontend","trigger":"frontend architecture review"},
    {"source":"vanducng/skills","skill":"fastreact","trigger":"fresh FastAPI and React application scaffold"},
    {"source":"oakoss/agent-skills","skill":"prompt-engineering","trigger":"multimodal prompt templates and evaluation"},
    {"source":"sickn33/agentic-awesome-skills","skill":"context-engineering","trigger":"memory or RAG feature"},
    {"source":"inbharatai/claude-skills","skill":"stable-diffusion-helper","trigger":"SDXL or ControlNet workflow work"},
    {"source":"g1joshi/agent-skills","skill":"comfyui","trigger":"self-hosted advanced ComfyUI"},
    {"source":"digitalsamba/claude-code-video-toolkit","skill":"ltx2","trigger":"LTX video feature"},
    {"source":"tippyentertainment/skills","skill":"comfyui-video-generator","trigger":"verified ComfyUI video workflow"},
    {"source":"vanman2024/ai-dev-marketplace","skill":"schema-validation","trigger":"before database migration deployment"},
    {"source":"supercent-io/skills-template","skill":"backend-testing","trigger":"backend test expansion"}
  ],
  "high_value_skill_sets": {
    "ui_ux_design_system": [
      {"source":"vercel-labs/agent-skills","skill":"web-design-guidelines","purpose":"web interface spacing, typography, interaction, and accessibility"},
      {"source":"wshobson/agents","skill":"design-system-patterns","purpose":"primitive, semantic, and component token architecture"},
      {"source":"supercent-io/skills-template","skill":"frontend-design-system","purpose":"tokens, layout, motion, and WCAG checks"},
      {"source":"jacob-balslev/skills","skill":"typography-system","purpose":"semantic type scale and reliable web font delivery"},
      {"source":"arvindrk/extract-design-system","skill":"extract-design-system","purpose":"extract existing repository design tokens before extending the UI"},
      {"source":"pbakaus/impeccable","skill":"critique","purpose":"final visual review"},
      {"source":"pbakaus/impeccable","skill":"polish","purpose":"final visual refinement"}
    ],
    "api_oauth_social": [
      {"source":"supercent-io/skills-template","skill":"authentication-setup","purpose":"OAuth/OIDC, sessions, RBAC, refresh-token lifecycle"},
      {"source":"secondsky/claude-skills","skill":"api-authentication","purpose":"secure API authentication patterns"},
      {"source":"thedaviddias/ux-patterns-for-developers","skill":"social-login","purpose":"OAuth social sign-in user experience"},
      {"source":"facebook/agentic-tools","skill":"api-integration","purpose":"optional Instagram and WhatsApp backend integration"},
      {"source":"facebook/agentic-tools","skill":"webhook-setup","purpose":"optional signed social webhook processing"},
      {"source":"facebook/agentic-tools","skill":"search-docs","purpose":"current Meta developer documentation lookup"}
    ],
    "video_editing": [
      {"source":"bryanwhl/ffmpeg-video-editor","skill":"ffmpeg-video-editor","purpose":"server-side probing and deterministic media edits"},
      {"source":"digitalsamba/claude-code-video-toolkit","skill":"moviepy","purpose":"deterministic overlays and short Python media jobs"},
      {"source":"digitalsamba/claude-code-video-toolkit","skill":"ltx2","purpose":"queued image-to-video generation"},
      {"source":"tippyentertainment/skills","skill":"comfyui-video-generator","purpose":"reviewed ComfyUI video generation workflows"}
    ],
    "rag_memory": [
      {"source":"wshobson/agents","skill":"rag-implementation","purpose":"document ingestion, retrieval, evaluation, and vector-store options"},
      {"source":"borghei/claude-skills","skill":"rag-architect","purpose":"vector store selection by cost, scale, privacy, and latency"},
      {"source":"muratcankoylan/agent-skills-for-context-engineering","skill":"memory-systems","purpose":"layered persistent agent memory design"},
      {"source":"terminalskills/skills","skill":"agent-memory","purpose":"instruction-file-first memory strategy"},
      {"source":"t4sh/skills4sh","skill":"agent-memory","purpose":"reviewable git-tracked project memory"},
      {"source":"nousresearch/hermes-agent","skill":"chroma","purpose":"optional self-hosted vector database"}
    ],
    "testing_deployment": [
      {"source":"dhruvanbhalara/skills","skill":"ci-cd","purpose":"GitHub Actions CI/CD quality gates"},
      {"source":"docker/skills","skill":"docker-project-foundations","purpose":"safe project Dockerisation"},
      {"source":"docker/skills","skill":"docker-build-strategies","purpose":"reproducible production image builds"},
      {"source":"vercel-labs/agent-skills","skill":"deploy-to-vercel","purpose":"preview-first Vercel deployment"},
      {"source":"openai/plugins","skill":"deployments-cicd","purpose":"Vercel promotion, rollback, inspect, and CI/CD"},
      {"source":"huggingface/skills","skill":"huggingface-spaces","purpose":"Hugging Face Space demos and bounded GPU experiments"}
    ],
    "agentic_orchestration": [
      {"source":"inngest/inngest-skills","skill":"inngest-agents","purpose":"durable multi-step tool calls, retries, approvals, and realtime progress"},
      {"source":"dannymac180/skills","skill":"codex-dynamic-workflows","purpose":"supervised orchestration workflow artifacts"},
      {"source":"obra/superpowers","skill":"writing-plans","purpose":"structured plan before complex execution"},
      {"source":"obra/superpowers","skill":"executing-plans","purpose":"checkpointed plan execution"},
      {"source":"obra/superpowers","skill":"verification-before-completion","purpose":"evidence gate before completion"}
    ],
    "performance_optimization": [
      {"source":"addyosmani/web-quality-skills","skill":"performance","purpose":"Core Web Vitals and Lighthouse budget optimisation"},
      {"source":"cloudflare/skills","skill":"web-perf","purpose":"render, network, cache, and layout-shift diagnosis"},
      {"source":"openai/plugins","skill":"web-perf","purpose":"web performance review"},
      {"source":"olehsvyrydov/ai-development-team","skill":"performance-engineer","purpose":"frontend, API, database, cache, and load-test optimisation"},
      {"source":"stareezy-1/frontend-architecture-skill","skill":"frontend-lighthouse","purpose":"CI performance gate"}
    ],
    "seo_marketing_automation": [
      {"source":"aaron-he-zhu/aaron-marketing-skills","skill":"technical-seo-checker","purpose":"crawlability, indexing, schema, mobile, and SEO audit"},
      {"source":"reason-machines/marketing-skills","skill":"seo-content-marketing-skill-suite","purpose":"keyword, content, SERP, and editorial workflow"},
      {"source":"reason-machines/data-skills","skill":"web-analytics-agent-skill","purpose":"authorised Search Console, GA4, and Bing reporting"},
      {"source":"i-onlabs/claude-code-skills","skill":"marketing-demand-acquisition","purpose":"growth and demand-acquisition planning"}
    ],
    "data_visualization": [
      {"source":"nickcrew/claude-cortex","skill":"chart-builder","purpose":"Chart.js/Python chart design and configuration"},
      {"source":"anthropics/knowledge-work-plugins","skill":"data-visualization","purpose":"accessible chart selection and storytelling"},
      {"source":"claude-office-skills/skills","skill":"chart-designer","purpose":"Chart.js/ECharts configuration"},
      {"source":"openai/plugins","skill":"d3-data-visualization","purpose":"bespoke interactive data visualisations"}
    ],
    "browser_automation": [
      {"source":"lackeyjb/playwright-skill","skill":"playwright-skill","purpose":"authorised Playwright test and operational scripts"},
      {"source":"openai/plugins","skill":"agent-browser","purpose":"reviewed browser automation"},
      {"source":"vercel-labs/agent-browser","skill":"agent-browser","purpose":"browser QA and allowed action workflows"},
      {"source":"github/awesome-copilot","skill":"webapp-testing","purpose":"Playwright test/debug workflows"},
      {"source":"sickn33/agentic-awesome-skills","skill":"browser-automation","purpose":"browser automation framework selection"}
    ]
  },
  "review_only_skills": [
    {"source":"reason-machines/mcp-skills","skill":"comfyui-mcp-agent","reason":"broad model, node, workflow, and MCP tool permissions"},
    {"source":"reason-machines/security-skills","skill":"supabase-pentest-skills","reason":"authorised non-production security testing only"},
    {"source":"thinkfleetai/thinkfleet-engine","skill":"fal-api","reason":"paid hosted provider and data-handling review required"}
    ,{"source":"reason-machines/ai-agent-skills","skill":"agentmemory-persistent-memory","reason":"external persistent-memory integration requires privacy, retention, and provider security review"}
    ,{"source":"rohitg00/agentmemory","skill":"agentmemory-mcp-tools","reason":"security audit result needs review and its broad memory/MCP tool access must be restricted"}
    ,{"source":"fetcher-sh/fetcher-skills","skill":"fetcher","reason":"third-party data collection requires provider terms, privacy, and user-consent review"}
    ,{"source":"lijingpan/video-uploader","skill":"video-uploader","reason":"social publishing must not use anti-detection or bypass platform rules; prefer official APIs and user confirmation"}
  ],
  "ox_alpha_instruction": "Read MAYA_OX_ALPHA_SKILLS_CATALOG.md and MAYA_OX_ALPHA_IMPLEMENTATION.md. Apply core skills as implementation guidance, install only reviewed owner-approved skills, and complete the acceptance checklist."
}



---

## Source document: `MAYA_OX_ALPHA_SKILLS_TOOL_REGISTRY.md`

# MAYA AI — Universal Skills and Tools Discovery Registry

## Purpose

This registry gives Ox Alpha a safe way to discover **all relevant current skills and tools** from skills.sh at implementation time. It complements the curated `MAYA_OX_ALPHA_SKILLS_CATALOG.md` rather than copying a changing public directory into this repository.

The curated catalogue is the approved starting set. This registry expands discovery across every project capability, records an approval decision, and prevents unsafe skills from becoming dependencies simply because they are popular.

## Required discovery workflow

1. Inspect the project and task. Select only relevant queries from `MAYA_OX_ALPHA_SKILLS_TOOL_REGISTRY.json`.
2. Search live: `npx skills find "<query>"`.
3. Preview a candidate without installing it: `npx skills use <owner/repo>@<skill>`.
4. Review its `SKILL.md`, licence, maintenance, required commands/services, security signal, data flows, and permissions.
5. Record the decision in `docs/skill-decisions.md` with source, commit/version, purpose, risk, owner approval, and rollback/removal procedure.
6. Install only the approved individual skill: `npx skills add <owner/repo> --skill <skill>`.
7. Verify the installed inventory: `npx skills list --json`. Update deliberately with `npx skills update`.

Never use `--all`, never install every search result, and never grant an agent a credential/tool solely because a skill suggests it.

## Capability and tool map

| Domain | Skills/tool searches | MAYA tool boundary |
|---|---|---|
| Product planning | `product`, `requirements`, `architecture`, `repo plan`, `documentation` | Read repository/project data; write versioned plans only. |
| Agent orchestration | `agent`, `tool calling`, `orchestration`, `workflow`, `human in the loop`, `MCP` | Typed tools; durable state; approval before external writes. |
| Frontend | `react`, `nextjs`, `typescript`, `tailwind`, `shadcn`, `forms`, `accessibility`, `i18n` | Browser-facing UI only; no service secrets. |
| Design system | `design system`, `tokens`, `typography`, `spacing`, `motion`, `UX`, `Figma` | Versioned design tokens and component documentation. |
| Backend/API | `fastapi`, `python`, `openapi`, `REST`, `webhook`, `background jobs`, `rate limit` | Typed API/service/worker boundaries. |
| Auth/integrations | `OAuth`, `OIDC`, `social login`, `API authentication`, `webhooks`, `email` | Server-side token handling; minimum scope, consent, revocation. |
| Database/data | `Postgres`, `Supabase`, `SQLAlchemy`, `Alembic`, `Redis`, `ETL`, `CSV` | RLS, migrations, project isolation, backups. |
| AI/LLM | `prompt engineering`, `structured output`, `LLM evals`, `embeddings`, `RAG`, `memory`, `Ollama` | Versioned prompts, evaluation, citations, retention/deletion. |
| Image/video/audio | `ComfyUI`, `FLUX`, `SDXL`, `ControlNet`, `SVD`, `LTX`, `FFmpeg`, `MoviePy`, `Remotion`, `music generation`, `TTS` | Separate GPU/media workers; immutable source assets/provenance. |
| Social/publishing | `Instagram API`, `TikTok API`, `YouTube API`, `publish`, `social media`, `content scheduling` | Official APIs first; explicit pre-publish confirmation. |
| Browser automation | `Playwright`, `agent browser`, `browser automation`, `web scraping`, `testing` | Allowed domains/actions; no CAPTCHA/MFA/anti-bot bypass. |
| Quality | `testing`, `TDD`, `Playwright`, `contract testing`, `security`, `accessibility`, `code review` | CI gates, authorisation tests, source review. |
| Performance | `performance`, `Core Web Vitals`, `Lighthouse`, `load testing`, `caching`, `profiling` | Budget measurements and evidence-based changes. |
| Observability | `observability`, `OpenTelemetry`, `tracing`, `Sentry`, `Grafana`, `logging` | Redacted telemetry, error tracking, metrics, alerting. |
| Deployment | `Docker`, `CI/CD`, `GitHub Actions`, `Vercel`, `Cloudflare`, `Hugging Face Spaces`, `rollback` | Preview first; separate web/API/GPU services; owner approval for production. |
| Growth/analytics | `SEO`, `Search Console`, `GA4`, `marketing`, `analytics`, `Chart.js`, `data visualization` | Human-reviewed claims/publication; project-safe aggregation. |
| Security/cost | `security hardening`, `threat model`, `secrets`, `dependency audit`, `cost optimization` | No credential exfiltration; least privilege; per-job cost limits. |

## Additional curated tool skills discovered

| Source | Skill | Use only when |
|---|---|---|
| `anthropics/skills` | `mcp-builder` | MAYA needs a new internal MCP server; expose a minimal typed tool surface and authorization model. |
| `addyosmani/agent-skills` | `security-and-hardening` | Reviewing application security, headers, authentication, dependency risks, and production hardening. |
| `addyosmani/agent-skills` | `observability-and-instrumentation` | Adding redacted logs, metrics, tracing, error diagnosis, and performance telemetry. |
| `wshobson/agents` | `python-observability` and `distributed-tracing` | FastAPI/worker tracing needs a Python-specific design. |
| `remotion-dev/skills` | `remotion-best-practices`, `remotion-render`, `remotion-captions` | MAYA needs templated, branded, data-driven video composition beyond FFmpeg/MoviePy. |
| `grafana/skills` | `app-observability` | A Grafana-backed monitoring stack is selected and approved. |

## Tool permission policy

| Tool class | Examples | Default | Requirement to enable |
|---|---|---|---|
| Read-only internal | Project/brief/query/report lookup | Allowed with RLS | Project membership. |
| Reversible internal write | Save brief, draft storyboard, queue job, update a draft | Allowed with audit | Typed schema + project membership. |
| External write | Social publish, send email/webhook, create cloud resource | Disabled | Explicit user confirmation per action plus scoped credentials. |
| Destructive or privileged | Delete project, rotate secret, change billing, bulk export | Disabled | Explicit confirmation, elevated role, audit record, safe recovery plan. |
| Prohibited | CAPTCHA bypass, anti-detection, MFA bypass, credential harvesting, rate-limit evasion | Never enable | No exception. |

## Tool records Ox Alpha must maintain

Every installed skill, MCP server, CLI, API, browser integration, or model provider needs a record with:

```json
{
  "id": "string",
  "category": "skill|mcp|cli|api|model|worker",
  "source": "owner/repository or provider",
  "version_or_commit": "string",
  "purpose": "string",
  "data_classification": ["public|project-private|sensitive"],
  "permissions": ["read|write_reversible|write_external|destructive"],
  "credential_owner": "server_only|user_oauth|none",
  "approval_required": true,
  "audit_events": ["string"],
  "rollback": "string",
  "status": "proposed|approved|installed|disabled|removed"
}
```

## Completion criteria

- Every relevant domain has been searched with the discovery queries before a major implementation phase.
- Only reviewed, versioned, owner-approved skills are installed.
- Every tool is recorded, scoped, and auditable.
- No prohibited browser/security-evasion tool exists in the project.
- `skills-lock.json` and `docs/skill-decisions.md` are committed after any approved change.



---

## Source document: `MAYA_OX_ALPHA_SKILLS_TOOL_REGISTRY.json`

{
  "name": "maya-ox-alpha-skills-tool-registry",
  "version": "2026-10-17",
  "purpose": "Live skills.sh discovery and secure tool governance for MAYA AI",
  "cli_workflow": {
    "search": "npx skills find <query>",
    "preview": "npx skills use <owner/repo>@<skill>",
    "install_one": "npx skills add <owner/repo> --skill <skill>",
    "inventory": "npx skills list --json",
    "update": "npx skills update",
    "forbidden": ["npx skills add --all", "bulk installation without review"]
  },
  "discovery_queries": {
    "product": ["product", "requirements", "architecture", "repo plan", "documentation"],
    "agentic": ["agent", "tool calling", "orchestration", "workflow", "human in the loop", "MCP"],
    "frontend": ["react", "nextjs", "typescript", "tailwind", "shadcn", "forms", "accessibility", "i18n"],
    "design": ["design system", "tokens", "typography", "spacing", "motion", "UX", "Figma"],
    "backend": ["fastapi", "python", "openapi", "REST", "webhook", "background jobs", "rate limit"],
    "identity_integrations": ["OAuth", "OIDC", "social login", "API authentication", "webhooks", "email"],
    "data": ["Postgres", "Supabase", "SQLAlchemy", "Alembic", "Redis", "ETL", "CSV"],
    "ai": ["prompt engineering", "structured output", "LLM evals", "embeddings", "RAG", "memory", "Ollama"],
    "media": ["ComfyUI", "FLUX", "SDXL", "ControlNet", "SVD", "LTX", "FFmpeg", "MoviePy", "Remotion", "music generation", "TTS"],
    "social": ["Instagram API", "TikTok API", "YouTube API", "publish", "social media", "content scheduling"],
    "browser": ["Playwright", "agent browser", "browser automation", "web scraping", "testing"],
    "quality": ["testing", "TDD", "contract testing", "security", "accessibility", "code review"],
    "performance": ["performance", "Core Web Vitals", "Lighthouse", "load testing", "caching", "profiling"],
    "observability": ["observability", "OpenTelemetry", "tracing", "Sentry", "Grafana", "logging"],
    "deployment": ["Docker", "CI/CD", "GitHub Actions", "Vercel", "Cloudflare", "Hugging Face Spaces", "rollback"],
    "growth": ["SEO", "Search Console", "GA4", "marketing", "analytics", "Chart.js", "data visualization"],
    "security_cost": ["security hardening", "threat model", "secrets", "dependency audit", "cost optimization"]
  },
  "extra_discovered_skills": [
    {"source":"anthropics/skills","skill":"mcp-builder","category":"mcp"},
    {"source":"addyosmani/agent-skills","skill":"security-and-hardening","category":"security"},
    {"source":"addyosmani/agent-skills","skill":"observability-and-instrumentation","category":"observability"},
    {"source":"wshobson/agents","skill":"python-observability","category":"observability"},
    {"source":"wshobson/agents","skill":"distributed-tracing","category":"observability"},
    {"source":"remotion-dev/skills","skill":"remotion-best-practices","category":"media"},
    {"source":"remotion-dev/skills","skill":"remotion-render","category":"media"},
    {"source":"remotion-dev/skills","skill":"remotion-captions","category":"media"},
    {"source":"grafana/skills","skill":"app-observability","category":"observability"}
  ],
  "permission_classes": ["read", "write_reversible", "write_external", "destructive"],
  "prohibited_capabilities": ["CAPTCHA bypass", "anti-detection", "MFA bypass", "credential harvesting", "rate-limit evasion"],
  "required_tool_record_fields": ["id", "category", "source", "version_or_commit", "purpose", "data_classification", "permissions", "credential_owner", "approval_required", "audit_events", "rollback", "status"]
}



---

## Source document: `MAYA_FREE_STACK_AND_TOOLS.md`

# MAYA AI — Free-First APIs, CLIs, and MCPs for Ox Alpha

## Start with this stack

| Need | Use first | Cost posture | Give Ox Alpha |
|---|---|---|---|
| Database, Auth, Storage, Realtime | Supabase | Free plan for prototyping | `SUPABASE_URL`, `SUPABASE_PUBLISHABLE_KEY`; keep service-role key server-only. |
| Web frontend/API edge helpers | Cloudflare Pages + Workers | Workers Free for early use | Cloudflare account/project only; create a least-privilege deployment token later. |
| Planning/chat model | Gemini Developer API | Free tier available, quota/data-use limits apply | `GEMINI_API_KEY` server-side only; use for structured design-plan drafts, not client-private documents unless you accept free-tier data handling. |
| Image/video prototype GPU | Hugging Face ZeroGPU Space | Free but daily quota and queues | Use only for demo/prototype jobs; never treat it as a guaranteed production GPU service. |
| Image/video production architecture | ComfyUI provider adapter | Software is free/open source; hosting GPU is not reliably free | Start with `MockMediaProvider`; add `COMFYUI_BASE_URL` only after choosing an authorised GPU host. |
| Source control and CI | GitHub + GitHub Actions | Free start depends on repository/account limits | Repository access; do not give personal tokens to frontend code. |

## Reality check: free image/video generation

There is no dependable unlimited free cloud API for FLUX, SDXL, ControlNet, SVD, or LTX-Video suitable for a production app. Build the provider interface, queue, provenance, UI, and mock provider now. Use a ZeroGPU demo only for limited validation; add a paid/self-hosted GPU endpoint later when real user demand exists.

## API keys and credentials to create now

Create only these initial secrets, then enter them into Ox Alpha's **server-side** environment configuration. Do not paste secrets into the prompt, source files, browser variables, or GitHub.

```dotenv
# Required for the first working version
SUPABASE_URL=
SUPABASE_PUBLISHABLE_KEY=
SUPABASE_SERVICE_ROLE_KEY=            # server/worker only
GEMINI_API_KEY=                       # server/worker only; optional until AI planning is switched on

# Add after deployment is selected
CLOUDFLARE_API_TOKEN=                 # least-privilege deploy token, never browser-visible
CLOUDFLARE_ACCOUNT_ID=

# Keep empty at first: mock provider must work without these
COMFYUI_BASE_URL=
COMFYUI_API_TOKEN=
HF_TOKEN=
```

### What not to create yet

- No paid model-provider key, social API token, marketing account, or browser cookie is needed for phase 1.
- Do not grant an AI agent a general cloud-admin key, GitHub personal access token, database superuser credential, or permanent Supabase service-role key.

## Free/open CLIs Ox Alpha may install

| CLI | Purpose | Install/use |
|---|---|---|
| Node.js + `npx` | React tooling, Skills CLI, Playwright, MCP launchers | Install Node LTS in the build environment. |
| `uv` | Fast Python environments and dependency management | `pip install uv` or platform package manager. |
| `ruff`, `pytest`, `mypy` | Python lint, tests, type checks | Add to backend dev dependencies, not global requirement. |
| Supabase CLI | Local migrations, types, functions, local MCP | `npx supabase --help` or official CLI install. |
| Wrangler | Cloudflare Workers/Pages development and deploy | `npx wrangler --help`; authenticate interactively only when deploying. |
| Docker + Compose | Reproducible FastAPI/worker/local service environment | Install only where container builds run. |
| FFmpeg/FFprobe | Deterministic media processing and input validation | Install in the media-worker image, not browser. |
| Playwright | Browser E2E tests and authorised browser automation | Add as a dev dependency; run browsers in CI/worker. |
| GitHub CLI (`gh`) | Repository, PR, issue, Actions workflow operations | Authenticate with least privileges in interactive developer environment. |
| Hugging Face CLI (`hf`) | Optional Space model/demo management | Add only when ZeroGPU/Spaces are actually used. |
| Skills CLI | Find/preview/review individual skills | `npx skills find <query>`; never bulk-install. |

## MCP servers to give Ox Alpha

MCPs help the coding agent build and inspect the project. They are not the runtime APIs that end users of MAYA call.

| MCP | Start status | Safe configuration |
|---|---|---|
| Supabase MCP | Recommended after creating one Supabase project | Scope to one project; start with `read_only=true` and docs/database features only. Enable migrations only after review. |
| Playwright MCP | Recommended for app E2E tests | Local/test environment; allow only MAYA localhost/preview domains; disable arbitrary-JS capability unless a trusted operator requires it. |
| GitHub MCP | Optional after repository connection | OAuth connection with repo-specific access; use for issues/PRs/repo context, not broad organisation administration. |
| Cloudflare MCP | Optional after Cloudflare project exists | Scope to the selected account/project; start read-only where available; deploy only after owner approval. |
| MAYA internal MCP | Later, not phase 1 | Build on Supabase Edge Functions with Supabase Auth/RLS; expose only user-authorised MAYA tools. |

### Recommended MCP configuration principles

- Scope every server to the smallest project/account.
- Start read-only. Enable a write feature only for a precise task, then return to read-only.
- Do not configure a browser MCP with a personal everyday browser profile or saved credentials.
- Never enable a tool that can execute arbitrary code for an untrusted agent client.

## Skills to install first

Ox Alpha should use the local package files first, then consider these focused skills:

```bash
npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices --skill vercel-composition-patterns --skill web-design-guidelines
npx skills add fastapi-practices/skills --skill fba
npx skills add supabase/agent-skills --skill supabase --skill supabase-postgres-best-practices
npx skills add openai/codex-plugin-cc --skill gpt-5-4-prompting
npx skills add wshobson/agents --skill prompt-engineering-patterns --skill design-system-patterns --skill rag-implementation
npx skills add anthropics/skills --skill webapp-testing --skill mcp-builder
npx skills add docker/skills --skill docker-project-foundations --skill docker-build-strategies
npx skills add addyosmani/web-quality-skills --skill performance
```

Before installing an entry, preview and record its source/version/licence decision. The curated skill catalogue remains the source of truth for optional and review-only skills.

## Phase 1 build order — no paid API required

1. Create the React + TypeScript frontend and FastAPI backend with typed contracts.
2. Create Supabase tables, private Storage bucket, RLS, Auth, migrations, and local test fixtures.
3. Implement project, room, upload, brief, agent chat, generation-job, and result APIs.
4. Implement `MockChatProvider` and `MockMediaProvider` so the whole workspace works without keys or GPU.
5. Add Gemini as an optional `ChatProvider` for validated `DesignPlan` JSON.
6. Add local Docker/Compose, CI, Playwright E2E, tests, observability, and Cloudflare preview deployment.
7. Add a ComfyUI/ZeroGPU provider only as a limited prototype adapter; keep its absence graceful.

## What to give Ox Alpha immediately

- The files in this MAYA package, especially `skills.sh`, `MAYA_OX_ALPHA_IMPLEMENTATION.md`, `MAYA_OX_ALPHA_SKILLS_CATALOG.md`, and this file.
- Your GitHub/Ox Alpha repository URL or export.
- A new Supabase project URL + publishable key (and service-role key only through the deployment-secret interface).
- Optionally, a Gemini API key stored only in backend/deployment secrets.

Do not provide any personal browser profile, social credentials, cloud-root credential, or payment/billing key.



---

## Source document: `MAYA_FREE_STACK_AND_TOOLS.json`

{
  "name": "maya-free-first-stack-and-tools",
  "version": "2026-10-17",
  "phase_1_requires_paid_api": false,
  "recommended_stack": {
    "database_auth_storage": {"provider":"Supabase","required_env":["SUPABASE_URL","VITE_SUPABASE_PUBLISHABLE_KEY","SUPABASE_SERVICE_ROLE_KEY","SUPABASE_JWT_SECRET","DATABASE_URL"],"service_role_scope":"server_or_worker_only","database_note":"SUPABASE_URL is not a Postgres connection string; DATABASE_URL is a distinct server-side secret"},
    "frontend_edge": {"provider":"Cloudflare Pages and Workers","required_env":["CLOUDFLARE_API_TOKEN","CLOUDFLARE_ACCOUNT_ID"],"phase":"deploy_only"},
    "planning_llm": {"provider":"Gemini Developer API","required_env":["GEMINI_API_KEY"],"phase":"optional","policy":"server_only; do not send client-private data to a free tier unless the owner accepts its data-use terms"},
    "media_generation": {"provider":"MockMediaProvider first; ComfyUI adapter later","required_env":["COMFYUI_BASE_URL","COMFYUI_API_TOKEN"],"phase":"prototype_after_core","policy":"no unlimited free production GPU assumption"},
    "prototype_gpu": {"provider":"Hugging Face ZeroGPU","required_env":["HF_TOKEN"],"phase":"optional_limited_demo"}
  },
  "clis": [
    {"name":"npx","purpose":"web tooling, Skills CLI, MCP launchers"},
    {"name":"uv","purpose":"Python environments and dependencies"},
    {"name":"Supabase CLI","purpose":"migrations, local development, functions"},
    {"name":"Wrangler","purpose":"Cloudflare development and deployment"},
    {"name":"Docker Compose","purpose":"reproducible API and worker services"},
    {"name":"FFmpeg and FFprobe","purpose":"media worker validation and rendering"},
    {"name":"Playwright","purpose":"E2E tests and authorised browser automation"},
    {"name":"gh","purpose":"repository, pull request, and CI workflow operations"},
    {"name":"hf","purpose":"optional Hugging Face Space management"},
    {"name":"skills","purpose":"find, preview, install, inventory, and update individual agent skills"}
  ],
  "mcps": [
    {"name":"Supabase MCP","phase":"after_project_creation","mode":"project-scoped read-only first","write_enablement":"reviewed migration/development task only"},
    {"name":"Playwright MCP","phase":"test_and_qa","mode":"localhost and preview allowlist","write_enablement":"user-authorised workflow only"},
    {"name":"GitHub MCP","phase":"after_repo_connection","mode":"repo-scoped OAuth","write_enablement":"reviewed issues and pull requests only"},
    {"name":"Cloudflare MCP","phase":"after_cloudflare_project","mode":"account/project scoped","write_enablement":"owner-approved deployment only"},
    {"name":"MAYA internal MCP","phase":"later","mode":"Supabase Auth plus RLS","write_enablement":"tool-specific user authorisation"}
  ],
  "initial_provider_adapters": ["MockChatProvider","MockMediaProvider","GeminiChatProvider","ComfyUIProvider"],
  "prohibited_inputs": ["browser cookies", "browser profiles", "personal social credentials", "cloud root credentials", "payment or billing keys", "frontend service-role keys"],
  "phase_1_order": ["scaffold frontend/backend", "Supabase schema/RLS/storage", "typed APIs", "mock providers", "optional Gemini", "tests/CI/preview", "optional limited GPU adapter"]
}



---

## Source document: `maya-skills-manifest.json`

{
  "name": "maya-ai-implementation-skills",
  "version": "1.0.0",
  "target": "Ox Alpha",
  "project": "MAYA AI",
  "priority": [
    "react_frontend",
    "fastapi_backend",
    "prompt_engineering",
    "image_video_generation",
    "supabase_postgres",
    "ui_ux_design_system",
    "api_oauth_social_integrations",
    "video_editing",
    "rag_memory_system",
    "testing_containers_deployment",
    "agentic_tool_orchestration",
    "performance_optimization",
    "seo_marketing_automation",
    "data_visualization",
    "browser_automation",
    "universal_skill_tool_discovery",
    "free_first_build_stack"
  ],
  "skills": {
    "react_frontend": {
      "stack": ["React", "TypeScript", "Tailwind CSS", "TanStack Query", "Zustand", "Zod", "Framer Motion"],
      "features": ["onboarding", "project workspace", "room studio", "brief wizard", "builder mode", "model settings"],
      "requirements": ["responsive", "accessible", "typed API client", "generation provenance"]
    },
    "fastapi_backend": {
      "stack": ["Python 3.12", "FastAPI", "Pydantic v2", "SQLAlchemy async", "Alembic", "PostgreSQL", "Redis queue"],
      "requirements": ["JWT auth", "RLS-compatible authorization", "background jobs", "idempotency", "signed uploads", "provider adapters"]
    },
    "prompt_engineering": {
      "requirements": ["versioned templates", "structured brief context", "JSON schema output", "assumptions", "safety boundaries", "prompt provenance"],
      "engine": "MAYA Enhancement Engine"
    },
    "image_video_generation": {
      "image_models": ["FLUX.1", "SDXL", "ControlNet"],
      "video_models": ["Stable Video Diffusion", "LTX-Video"],
      "integration": "ComfyUI provider adapter with versioned workflow JSON"
    },
    "supabase_postgres": {
      "requirements": ["UUID keys", "RLS", "private object storage", "project-scoped paths", "migrations", "audit events"],
      "entities": ["profiles", "projects", "rooms", "assets", "design_briefs", "generation_jobs", "generation_results", "design_options", "agent_messages"]
    },
    "ui_ux_design_system": {
      "requirements": ["primitive-semantic-component token hierarchy", "typography scale", "spacing scale", "responsive tokens", "dark mode", "WCAG AA", "reduced motion"],
      "skills_catalog_group": "ui_ux_design_system"
    },
    "api_oauth_social_integrations": {
      "requirements": ["OAuth 2.0/OIDC authorization code plus PKCE", "server-side token exchange", "encrypted refresh tokens", "minimum scopes", "webhook verification", "revocation"],
      "skills_catalog_group": "api_oauth_social"
    },
    "video_editing": {
      "requirements": ["ffprobe validation", "typed FFmpeg recipes", "immutable original assets", "worker jobs", "MoviePy overlays", "provenance"],
      "skills_catalog_group": "video_editing"
    },
    "rag_memory_system": {
      "requirements": ["pgvector-first evaluation", "project-scoped retrieval", "source citations", "retention/deletion", "separate memory classes", "re-embedding"],
      "skills_catalog_group": "rag_memory"
    },
    "testing_containers_deployment": {
      "requirements": ["CI quality gates", "RLS and authorization tests", "Docker multi-stage builds", "preview-first Vercel", "separate GPU workers", "documented rollback"],
      "skills_catalog_group": "testing_deployment"
    },
    "agentic_tool_orchestration": {
      "requirements": ["durable state machine", "typed tools", "idempotency", "retries", "workflow provenance", "explicit final publish approval"],
      "skills_catalog_group": "agentic_orchestration"
    },
    "performance_optimization": {
      "requirements": ["Core Web Vitals budgets", "Lighthouse CI", "API/database profiling", "queue/render metrics", "regression baselines"],
      "skills_catalog_group": "performance_optimization"
    },
    "seo_marketing_automation": {
      "requirements": ["public/private site boundary", "truthful structured data", "human-reviewed external content", "minimum OAuth scopes", "revocation"],
      "skills_catalog_group": "seo_marketing_automation"
    },
    "data_visualization": {
      "requirements": ["Chart.js-first", "accessible labels and table alternatives", "role/project-filtered aggregates", "accurate units and time ranges"],
      "skills_catalog_group": "data_visualization"
    },
    "browser_automation": {
      "requirements": ["official APIs preferred", "allowed domain/action policy", "separate worker", "no CAPTCHA/MFA bypass", "pre-publish confirmation", "audit event"],
      "skills_catalog_group": "browser_automation"
    },
    "universal_skill_tool_discovery": {
      "requirements": ["live skills search", "preview before install", "source/version/license review", "tool permission record", "skills lockfile", "decision log", "prohibited capability policy"],
      "registry": "MAYA_OX_ALPHA_SKILLS_TOOL_REGISTRY.json"
    },
    "free_first_build_stack": {
      "requirements": ["Supabase free-first", "Cloudflare deployment", "mock providers", "optional Gemini planning", "limited prototype GPU", "server-side secret management"],
      "registry": "MAYA_FREE_STACK_AND_TOOLS.json"
    }
  },
  "acceptance_command": "Follow MAYA_OX_ALPHA_IMPLEMENTATION.md as the source of truth; implement all quality-gate items before marking the task complete."
}



---

## Source document: `skills-lock.json`

{
  "version": 1,
  "skills": {
    "design-system-patterns": {
      "source": "wshobson/agents",
      "sourceType": "github",
      "skillPath": "plugins/ui-design/skills/design-system-patterns/SKILL.md",
      "computedHash": "e1d2631eab1a7113fb60e6df3ace05aac0ddce6207bceec87721119a8e1a1c78"
    },
    "docker-build-strategies": {
      "source": "docker/skills",
      "sourceType": "github",
      "skillPath": "skills/docker-build-strategies/SKILL.md",
      "computedHash": "e6a297d613873cf74b030655ee8405ca4434980cfb0dfd412ac5aa4e213d3d5c"
    },
    "docker-project-foundations": {
      "source": "docker/skills",
      "sourceType": "github",
      "skillPath": "skills/docker-project-foundations/SKILL.md",
      "computedHash": "6b2334b2c24910d177e1f80a0cc1f5135f2a9b33b722673873435736de36128f"
    },
    "fba": {
      "source": "fastapi-practices/skills",
      "sourceType": "github",
      "skillPath": "skills/fastapi-best-architecture/SKILL.md",
      "computedHash": "6040ad4cc1db89d01682193e5edb5178d96642a27a0a4db5046f23221d315ae6"
    },
    "mcp-builder": {
      "source": "anthropics/skills",
      "sourceType": "github",
      "skillPath": "skills/mcp-builder/SKILL.md",
      "computedHash": "826e46adf81e1372282e205c34e1a2ee876e72148007726e4a2512599d2fef7b"
    },
    "performance": {
      "source": "addyosmani/web-quality-skills",
      "sourceType": "github",
      "skillPath": "skills/performance/SKILL.md",
      "computedHash": "ce9d36f139a1b2a6a8ac2cb222698963b8076d2dd8b41685e8e8ae589cdcf1e4"
    },
    "prompt-engineering-patterns": {
      "source": "wshobson/agents",
      "sourceType": "github",
      "skillPath": "plugins/llm-application-dev/skills/prompt-engineering-patterns/SKILL.md",
      "computedHash": "6a8cf3a5e9120641c1c1953c870c156377c57be4a806e1df6fc5f073a41cc639"
    },
    "rag-implementation": {
      "source": "wshobson/agents",
      "sourceType": "github",
      "skillPath": "plugins/llm-application-dev/skills/rag-implementation/SKILL.md",
      "computedHash": "595e221310222b991452ac6d850097b466fbda46860c9ce933ddd56a0998dac9"
    },
    "supabase": {
      "source": "supabase/agent-skills",
      "sourceType": "github",
      "skillPath": "skills/supabase/SKILL.md",
      "computedHash": "211141fd078b4b3645803868528d54221bc7755d24d5c8af45a366785c151dba"
    },
    "supabase-postgres-best-practices": {
      "source": "supabase/agent-skills",
      "sourceType": "github",
      "skillPath": "skills/supabase-postgres-best-practices/SKILL.md",
      "computedHash": "e14e276241805c97dbcfe40dcbea1a3035269cc7293cac4b1832dda41a835e60"
    },
    "vercel-composition-patterns": {
      "source": "vercel-labs/agent-skills",
      "sourceType": "github",
      "skillPath": "skills/composition-patterns/SKILL.md",
      "computedHash": "f98931159fa9c7fed043bcd18a891a46dcf89ababa38df13a4c5b7b30dc0ce07"
    },
    "vercel-react-best-practices": {
      "source": "vercel-labs/agent-skills",
      "sourceType": "github",
      "skillPath": "skills/react-best-practices/SKILL.md",
      "computedHash": "3219a1944e404ffc14d1d9d6aef6dd2e3855b81387ee0a044ccbfe14d34c2357"
    },
    "webapp-testing": {
      "source": "anthropics/skills",
      "sourceType": "github",
      "skillPath": "skills/webapp-testing/SKILL.md",
      "computedHash": "ad5b1fc52807e9afa4635e59218a026b164dc58b6c3f41b0f7c644dcd6ccf572"
    }
  }
}



---

## Source document: `skills.sh`

#!/usr/bin/env bash
# MAYA AI skill entrypoint for Ox Alpha.
# Read MAYA_OX_ALPHA_IMPLEMENTATION.md before making changes.
# This script is intentionally safe: it validates the paired manifest and
# prints the required implementation order. It makes no network calls, creates
# no credentials, and does not modify the project.

set -euo pipefail

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
SPEC_FILE="$ROOT_DIR/MAYA_OX_ALPHA_IMPLEMENTATION.md"
MANIFEST_FILE="$ROOT_DIR/maya-skills-manifest.json"
CATALOG_FILE="$ROOT_DIR/MAYA_OX_ALPHA_SKILLS_CATALOG.md"
CATALOG_MANIFEST_FILE="$ROOT_DIR/MAYA_OX_ALPHA_SKILLS_CATALOG.json"
TOOL_REGISTRY_FILE="$ROOT_DIR/MAYA_OX_ALPHA_SKILLS_TOOL_REGISTRY.md"
TOOL_REGISTRY_MANIFEST_FILE="$ROOT_DIR/MAYA_OX_ALPHA_SKILLS_TOOL_REGISTRY.json"
FREE_STACK_FILE="$ROOT_DIR/MAYA_FREE_STACK_AND_TOOLS.md"
FREE_STACK_MANIFEST_FILE="$ROOT_DIR/MAYA_FREE_STACK_AND_TOOLS.json"
STARTER_FILE="$ROOT_DIR/OX_ALPHA_START_MAYA.md"

if [ ! -f "$SPEC_FILE" ] || [ ! -f "$MANIFEST_FILE" ] || [ ! -f "$CATALOG_FILE" ] || [ ! -f "$CATALOG_MANIFEST_FILE" ] || [ ! -f "$TOOL_REGISTRY_FILE" ] || [ ! -f "$TOOL_REGISTRY_MANIFEST_FILE" ] || [ ! -f "$FREE_STACK_FILE" ] || [ ! -f "$FREE_STACK_MANIFEST_FILE" ] || [ ! -f "$STARTER_FILE" ]; then
  echo "MAYA skill files are incomplete. Keep every MAYA_*.md, MAYA_*.json, OX_ALPHA_START_MAYA.md, and skills.sh together." >&2
  exit 1
fi

if command -v python3 >/dev/null 2>&1; then
  python3 -m json.tool "$MANIFEST_FILE" >/dev/null
  python3 -m json.tool "$CATALOG_MANIFEST_FILE" >/dev/null
  python3 -m json.tool "$TOOL_REGISTRY_MANIFEST_FILE" >/dev/null
  python3 -m json.tool "$FREE_STACK_MANIFEST_FILE" >/dev/null
fi

if [ "${1:-}" = "--discover" ]; then
  cat <<'EOF'
Live skills.sh discovery (review every candidate before installing):
  npx skills find "agent orchestration"
  npx skills find "security hardening"
  npx skills find "observability"
  npx skills find "Remotion"
  npx skills find "Playwright"
  npx skills find "music generation"

Read MAYA_OX_ALPHA_SKILLS_TOOL_REGISTRY.md for the complete query set,
permission policy, decision-log format, and prohibited capabilities.
EOF
  exit 0
fi

if [ "${1:-}" = "--starter" ]; then
  cat "$STARTER_FILE"
  exit 0
fi

cat <<'EOF'
MAYA AI skills are ready for implementation.

Priority:
  1. React/frontend component generation
  2. FastAPI/Python backend architecture
  3. Prompt engineering for MAYA Enhancement Engine
  4. FLUX/SDXL/ControlNet/SVD/LTX-Video provider integration
  5. Supabase/Postgres schema and RLS
  6. UI/UX design tokens, typography, spacing, and accessibility
  7. OAuth, API, and optional social integrations
  8. FFmpeg/MoviePy video editing and media-worker architecture
  9. Vector database, RAG, and durable memory controls
 10. Testing, Docker, Vercel/Hugging Face deployment and CI/CD
 11. Agentic tool-calling, durable workflows, and user approvals
 12. Frontend/backend performance budgets and optimisation
 13. SEO, analytics, and human-reviewed marketing automation
 14. Accessible data visualization and Chart.js dashboards
 15. Playwright browser automation and authorised publishing workflows
 16. Live skills/tool discovery with approval and permission governance
 17. Free-first APIs, CLIs, MCPs, and provider-adapter build path

Ox Alpha instruction:
  Read MAYA_OX_ALPHA_IMPLEMENTATION.md fully.
  Parse maya-skills-manifest.json for the machine-readable scope.
  Read MAYA_OX_ALPHA_SKILLS_CATALOG.md before installing any skills.
  Parse MAYA_OX_ALPHA_SKILLS_CATALOG.json for the curated skills.sh selection.
  Read MAYA_OX_ALPHA_SKILLS_TOOL_REGISTRY.md before every new major capability.
  Read MAYA_FREE_STACK_AND_TOOLS.md for free-first keys, CLIs, MCPs, and phase order.
  Run ./skills.sh --discover to print representative live-discovery commands.
  Run ./skills.sh --starter to print the ready-to-paste Ox Alpha brief.
  Preserve the existing repository conventions.
  Review and approve skills before installation; never auto-install review-only skills.
  Implement in the order defined in the specification.
  Do not add secrets or model weights to source control.
EOF



---

## Source document: `docs/skill-decisions.md`

# MAYA skill decision log

## D-001 — Individual skill review

Decision: Skills are previewed and installed individually; bulk installation is forbidden. Permission ladder is default-deny.

Rationale: Keep project instructions auditable and reduce unreviewed code/dependency changes.

Date: 2026-10-17

## D-002 — Secret and model boundaries

Decision: Model and media keys stay server/worker-side. Gemini is optional until explicitly configured; Hugging Face ZeroGPU is prototype-only.

Rationale: Prevent browser exposure and keep the zero-key mock path functional.

Date: 2026-10-17

## D-003 — Boot order and reporting

Decision: Follow `OX_ALPHA_START_MAYA.md` read order, scaffold empty repositories, and report changed files, checks, secret placement, and blockers.

Rationale: Make agent sessions repeatable and reviewable.

Date: 2026-10-17

## D-004 — Workloads and deployment

Decision: Heavy media work runs in worker containers, never serverless. Preview deployments precede production; production changes require owner approval.

Rationale: Avoid timeout-bound processing and unreviewed production changes.

Date: 2026-10-17

## D-005 — Approved skill installs

Decision: Install only skills named in the approved catalog, one at a time after previewing their contents and license. The resolved source and content hash are recorded in `skills-lock.json`; files are copied into `.agents/skills/` for repository-local use. See `docs/THIRD_PARTY_SKILLS.md` for the complete install/skip list and notices.

Rationale: Apply useful project guidance while retaining auditable, project-scoped skill copies and respecting declared licenses.

Date: 2026-10-17

SKILL-ADD: vercel-react-best-practices — previewed, approved
SKILL-ADD: vercel-composition-patterns — previewed, approved
SKILL-SKIP: web-design-guidelines — previewed; no license is declared in the skill or upstream repository.
SKILL-ADD: fba — previewed, approved
SKILL-ADD: supabase — previewed, approved; upstream MIT license verified.
SKILL-ADD: supabase-postgres-best-practices — previewed, approved; MIT, skill version 1.1.1.
SKILL-ADD: prompt-engineering-patterns — previewed, approved; upstream MIT license verified.
SKILL-ADD: design-system-patterns — previewed, approved; upstream MIT license verified.
SKILL-ADD: rag-implementation — previewed, approved; upstream MIT license verified.
SKILL-ADD: webapp-testing — previewed, approved; bundled Apache-2.0 LICENSE.txt.
SKILL-ADD: mcp-builder — previewed, approved; bundled Apache-2.0 LICENSE.txt.
SKILL-ADD: docker-project-foundations — previewed, approved; Apache-2.0.
SKILL-NOTE: Retain `docker-compose.yml` because the user-specified build contract names it; validate with `docker compose -f docker-compose.yml`.
SKILL-ADD: docker-build-strategies — previewed, approved; Apache-2.0.
SKILL-ADD: performance — previewed, approved; MIT, skill version 2.0.



---

## Source document: `docs/THIRD_PARTY_SKILLS.md`

# Third-party skill notices

The following skills are copied into `.agents/skills/` for repository-local agent guidance. Upstream references are pinned by repository commit and per-skill content hash so a later refresh can be reviewed as a separate change. Skills are guidance files; their presence does not install or grant access to the tools, credentials, or services they discuss.

| Skill | Upstream source snapshot | License / declared version | `skills-lock.json` content hash |
|---|---|---|---|
| `vercel-react-best-practices` | `vercel-labs/agent-skills` @ `063bee94c3f4df8453406c830b0a7df0f2860278` | MIT / 1.0.0 | `3219a1944e404ffc14d1d9d6aef6dd2e3855b81387ee0a044ccbfe14d34c2357` |
| `vercel-composition-patterns` | `vercel-labs/agent-skills` @ `063bee94c3f4df8453406c830b0a7df0f2860278` | MIT / 1.0.0 | `f98931159fa9c7fed043bcd18a891a46dcf89ababa38df13a4c5b7b30dc0ce07` |
| `fba` | `fastapi-practices/skills` @ `8d6155c2be880b3e3e2d359b67904e378eaf5f13` | MIT / no skill version declared | `6040ad4cc1db89d01682193e5edb5178d96642a27a0a4db5046f23221d315ae6` |
| `supabase` | `supabase/agent-skills` @ `c9be0e931b7930f7d02126d04774d904c381e7d7` | MIT / 0.1.2 | `211141fd078b4b3645803868528d54221bc7755d24d5c8af45a366785c151dba` |
| `supabase-postgres-best-practices` | `supabase/agent-skills` @ `c9be0e931b7930f7d02126d04774d904c381e7d7` | MIT / 1.1.1 | `e14e276241805c97dbcfe40dcbea1a3035269cc7293cac4b1832dda41a835e60` |
| `prompt-engineering-patterns` | `wshobson/agents` @ `044b4b21f083948e69ec878a7b07c8d0951a6ffa` | MIT / no skill version declared | `6a8cf3a5e9120641c1c1953c870c156377c57be4a806e1df6fc5f073a41cc639` |
| `design-system-patterns` | `wshobson/agents` @ `044b4b21f083948e69ec878a7b07c8d0951a6ffa` | MIT / no skill version declared | `e1d2631eab1a7113fb60e6df3ace05aac0ddce6207bceec87721119a8e1a1c78` |
| `rag-implementation` | `wshobson/agents` @ `044b4b21f083948e69ec878a7b07c8d0951a6ffa` | MIT / no skill version declared | `595e221310222b991452ac6d850097b466fbda46860c9ce933ddd56a0998dac9` |
| `webapp-testing` | `anthropics/skills` @ `dbd4588f9e1033efb41dad4bef2f7947c8993d44` | Apache-2.0 / bundled `LICENSE.txt` | `ad5b1fc52807e9afa4635e59218a026b164dc58b6c3f41b0f7c644dcd6ccf572` |
| `mcp-builder` | `anthropics/skills` @ `dbd4588f9e1033efb41dad4bef2f7947c8993d44` | Apache-2.0 / bundled `LICENSE.txt` | `826e46adf81e1372282e205c34e1a2ee876e72148007726e4a2512599d2fef7b` |
| `docker-project-foundations` | `docker/skills` @ `25f7e03184ce455ea1604bea00f7b40f95ca50e5` | Apache-2.0 | `6b2334b2c24910d177e1f80a0cc1f5135f2a9b33b722673873435736de36128f` |
| `docker-build-strategies` | `docker/skills` @ `25f7e03184ce455ea1604bea00f7b40f95ca50e5` | Apache-2.0 | `e6a297d613873cf74b030655ee8405ca4434980cfb0dfd412ac5aa4e213d3d5c` |
| `performance` | `addyosmani/web-quality-skills` @ `afa8da942115f2961fdbfa80807ea0b232ff6c00` | MIT / 2.0 | `ce9d36f139a1b2a6a8ac2cb222698963b8076d2dd8b41685e8e8ae589cdcf1e4` |

MIT terms and upstream copyright notices are reproduced in [LICENSE-MIT.txt](third_party_licenses/LICENSE-MIT.txt). Docker's Apache-2.0 license is reproduced in [LICENSE-APACHE-2.0-Docker.txt](third_party_licenses/LICENSE-APACHE-2.0-Docker.txt); Anthropic's skill folders retain their bundled Apache-2.0 `LICENSE.txt` files.

`web-design-guidelines` was previewed but not copied: neither the skill nor its upstream repository declared a license at review time. The review-only Codex prompting skill was not installed because it is not in `approved_install`.



---

## Source document: `.env.example`

# Frontend-safe publishable configuration
VITE_SUPABASE_URL=
VITE_SUPABASE_PUBLISHABLE_KEY=
VITE_API_BASE_URL=[external address omitted in offline package]

# Local Docker Postgres only; never reuse this value in hosted environments
POSTGRES_PASSWORD=local-only

# Backend/server ONLY — never expose to browser or Git
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
SUPABASE_JWT_SECRET=
SUPABASE_STORAGE_BUCKET=maya-assets
GEMINI_API_KEY=
DATABASE_URL=sqlite+aiosqlite:///./maya.db
DEV_AUTH_ENABLED=true

# Worker ONLY
COMFYUI_BASE_URL=
COMFYUI_API_TOKEN=
HF_TOKEN=

# CI / Deploy dashboard secrets only
CLOUDFLARE_API_TOKEN=
VERCEL_CRON_SECRET=



---

## Source document: `.github/workflows/ci.yml`

name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  backend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with:
          python-version: "3.12"
          enable-cache: true
      - run: uv sync --extra dev --locked
      - run: uv run ruff check app migrations tests ../worker
      - run: uv run mypy app ../worker
      - run: uv run pytest tests --cov=app --cov-fail-under=80
      - run: uv run alembic upgrade head
      - run: uv run python -m app.seed

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm
          cache-dependency-path: frontend/package-lock.json
      - run: npm ci --prefix frontend
      - run: npm --prefix frontend run typecheck
      - run: npm --prefix frontend run lint
      - run: npm --prefix frontend run test
      - run: npm --prefix frontend run build
      - name: Fail if server secret identifiers appear in frontend source
        run: if rg -n 'SUPABASE_SERVICE_ROLE_KEY|GEMINI_API_KEY' frontend/src; then exit 1; fi

  e2e:
    runs-on: ubuntu-latest
    needs: [backend, frontend]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with:
          python-version: "3.12"
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm
          cache-dependency-path: frontend/package-lock.json
      - run: cp .env.example .env
      - run: docker compose up -d --build
      - run: npm ci --prefix frontend
      - run: npx playwright install --with-deps chromium
        working-directory: frontend
      - run: npm --prefix frontend run e2e
      - if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: frontend/playwright-report/
          if-no-files-found: ignore
      - if: always()
        run: docker compose logs --no-color > compose.log
      - if: always()
        uses: actions/upload-artifact@v4
        with:
          name: compose-logs
          path: compose.log
          if-no-files-found: ignore
      - if: always()
        run: docker compose down -v




---

## Reviewed skill instruction: `.agents/skills/design-system-patterns/SKILL.md`

---
name: design-system-patterns
description: Build scalable design systems with design tokens, theming infrastructure, and component architecture patterns. Use when creating design tokens, implementing theme switching, building component libraries, or establishing design system foundations.
---

# Design System Patterns

Master design system architecture to create consistent, maintainable, and scalable UI foundations across web and mobile applications.

## When to Use This Skill

- Creating design tokens for colors, typography, spacing, and shadows
- Implementing light/dark theme switching with CSS custom properties
- Building multi-brand theming systems
- Architecting component libraries with consistent APIs
- Establishing design-to-code workflows with Figma tokens
- Creating semantic token hierarchies (primitive, semantic, component)
- Setting up design system documentation and guidelines

## Core Capabilities

### 1. Design Tokens

- Primitive tokens (raw values: colors, sizes, fonts)
- Semantic tokens (contextual meaning: text-primary, surface-elevated)
- Component tokens (specific usage: button-bg, card-border)
- Token naming conventions and organization
- Multi-platform token generation (CSS, iOS, Android)

### 2. Theming Infrastructure

- CSS custom properties architecture
- Theme context providers in React
- Dynamic theme switching
- System preference detection (prefers-color-scheme)
- Persistent theme storage
- Reduced motion and high contrast modes

### 3. Component Architecture

- Compound component patterns
- Polymorphic components (as prop)
- Variant and size systems
- Slot-based composition
- Headless UI patterns
- Style props and responsive variants

### 4. Token Pipeline

- Figma to code synchronization
- Style Dictionary configuration
- Token transformation and formatting
- CI/CD integration for token updates

## Quick Start

```typescript
// Design tokens with CSS custom properties
const tokens = {
  colors: {
    // Primitive tokens
    gray: {
      50: "#fafafa",
      100: "#f5f5f5",
      900: "#171717",
    },
    blue: {
      500: "#3b82f6",
      600: "#2563eb",
    },
  },
  // Semantic tokens (reference primitives)
  semantic: {
    light: {
      "text-primary": "var(--color-gray-900)",
      "text-secondary": "var(--color-gray-600)",
      "surface-default": "var(--color-white)",
      "surface-elevated": "var(--color-gray-50)",
      "border-default": "var(--color-gray-200)",
      "interactive-primary": "var(--color-blue-500)",
    },
    dark: {
      "text-primary": "var(--color-gray-50)",
      "text-secondary": "var(--color-gray-400)",
      "surface-default": "var(--color-gray-900)",
      "surface-elevated": "var(--color-gray-800)",
      "border-default": "var(--color-gray-700)",
      "interactive-primary": "var(--color-blue-400)",
    },
  },
};
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

1. **Name Tokens by Purpose**: Use semantic names (text-primary) not visual descriptions (dark-gray)
2. **Maintain Token Hierarchy**: Primitives > Semantic > Component tokens
3. **Document Token Usage**: Include usage guidelines with token definitions
4. **Version Tokens**: Treat token changes as API changes with semver
5. **Test Theme Combinations**: Verify all themes work with all components
6. **Automate Token Pipeline**: CI/CD for Figma-to-code synchronization
7. **Provide Migration Paths**: Deprecate tokens gradually with clear alternatives

## Common Issues

- **Token Sprawl**: Too many tokens without clear hierarchy
- **Inconsistent Naming**: Mixed conventions (camelCase vs kebab-case)
- **Missing Dark Mode**: Tokens that don't adapt to theme changes
- **Hardcoded Values**: Using raw values instead of tokens
- **Circular References**: Tokens referencing each other in loops
- **Platform Gaps**: Tokens missing for some platforms (web but not mobile)



---

## Reviewed skill instruction: `.agents/skills/docker-build-strategies/SKILL.md`

---
name: docker-build-strategies
description: Use this skill when writing, reviewing, or optimizing Dockerfiles, even if the user just says their image is too large, their build is slow, or they need to harden a container for production. Covers multi-stage builds, layer caching, .dockerignore, non-root users, and image size optimization.
license: Apache-2.0
compatibility: Requires Docker 23.0+ (BuildKit default). On Docker 20.10–22.x, set DOCKER_BUILDKIT=1 before building.
---

# Docker Build Strategies

## Overview

This skill provides rules and patterns for writing and reviewing production-quality Dockerfiles. Apply it when the main task is image-build quality: multi-stage builds, cache behavior, non-root execution, build context hygiene, and runtime image size.

## When to use this skill

Activate this skill when:

- Creating a new Dockerfile for any language or framework
- Optimizing an existing Dockerfile for size, speed, or security
- Reviewing a Dockerfile for best-practice compliance
- Adding a `.dockerignore` file to a project

## Do not use this skill when

Do not use this skill when:

- The project has no Docker setup yet and the main need is a first-pass scaffold
- The main task is wiring services together in `compose.yaml`
- The main task is debugging Compose startup ordering, networking, or development overrides

## Core guidance

### Multi-stage builds

Use multi-stage builds when the project has a build step or when build-time dependencies differ from runtime. Separate build-time dependencies from the runtime image.

1. Name every stage explicitly (`FROM ... AS build`, `FROM ... AS runtime`).
2. Use the smallest appropriate base for the runtime stage: `distroless`, `alpine`, or `slim` variants.
3. Copy only the final artifact into the runtime stage with `COPY --from=build`.
4. Use `COPY --link` when copying from a prior stage or adding static files — it improves cache reuse by making the COPY independent of previous layers.

See `references/multi-stage-builds.md` for language-specific patterns (Go, Node, Python, Java).

### Layer caching

Order Dockerfile instructions from least-frequently-changed to most-frequently-changed.

1. Place dependency manifests (`package.json`, `go.mod`, `requirements.txt`) and install steps before copying application source code. Bind-mount the manifest into the install step instead of `COPY`-ing it, so it never enters a layer: `RUN --mount=type=bind,source=package.json,target=package.json --mount=type=bind,source=package-lock.json,target=package-lock.json npm ci`. This is safe for install commands that only read the manifest (`npm ci`, `pip install -r`, `go mod download`); if a step also needs to write the manifest back into the image, `COPY` it instead.
2. Use BuildKit cache mounts for package manager caches:
   - Go: `RUN --mount=type=cache,target=/go/pkg/mod go build ...`
   - Node: `RUN --mount=type=cache,target=/root/.npm npm ci`
   - Python: `RUN --mount=type=cache,target=/root/.cache/pip pip install ...`
   - apt: `RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && apt-get install -y ...` — no `rm -rf /var/lib/apt/lists/*` needed, since the cache lives outside the image layer. `sharing=locked` is required because apt needs exclusive access to its cache directories.
   - apk (Alpine — per the Alpine wiki, not a Docker-verified doc; `references/layer-caching.md` links the source): `RUN --mount=type=cache,target=/etc/apk/cache,sharing=locked apk add ...` — drop `--no-cache` so downloaded packages land in the mounted cache directory instead of being discarded.
3. Pin base image tags to a specific version or digest — never use `latest` in production.
4. Combine related `RUN` commands with `&&` to reduce layer count, but keep logically distinct steps separate for cache granularity.

See `references/layer-caching.md` for detailed cache invalidation rules and cache mount patterns.

### Build secrets and SSH access

Never bake credentials into the image. Use BuildKit secrets and SSH mounts so credentials are available only during the specific `RUN` step that needs them, and never persist in any layer or `docker history` output.

1. **Do NOT** pass credentials through `ARG` or `ENV`. Both end up in the image layers and are inspectable via `docker history`.
2. **Do NOT** `COPY` credential files into the build context: `.npmrc`, `.pypirc`, `.netrc`, `pip.conf`, Maven `settings.xml`, `.env`, cloud credentials (`~/.aws/credentials`, `~/.config/gcloud/`, service-account JSON files, `~/.azure/`), secret-manager tokens (`~/.vault-token`), package-registry tokens (`~/.cargo/credentials.toml`), TLS keys (`*.pem`, `*.p12`), `kubeconfig`, SSH keys (`id_rsa`, `id_dsa`, `id_ed25519`, `id_ecdsa`). Even when the final stage does not copy them forward, they live in intermediate layers and the build cache.
3. **Do NOT** echo, write, or expand the secret value inside a `RUN` command in a way that persists it to a layer or emits it to build logs. Access the secret file (e.g., `/run/secrets/<id>`, or directly via the mount `target=`) — never `echo "$(cat /run/secrets/X)"`, never substitute it into a shell argument that will be logged with `--progress=plain`.
4. **Use `RUN --mount=type=secret`** for package manager registry credentials:
   ```dockerfile
   RUN --mount=type=secret,id=npmrc,target=/root/.npmrc,required=false \
       --mount=type=cache,target=/root/.npm \
       npm ci --omit=dev
   ```
   The secret is available only inside that `RUN`, never written to a layer. Use `required=true` when the build will always need the credential (e.g., all packages come from a private registry, so missing the secret should fail the build immediately); use `required=false` only when the secret is optional (the build can succeed with public packages alone).
5. **Use `RUN --mount=type=ssh`** for fetching private Git repositories or modules. The build container has no `known_hosts` by default — populate it inside the same `RUN`:
   ```dockerfile
   RUN --mount=type=ssh \
       mkdir -p -m 0700 /root/.ssh && \
       ssh-keyscan github.com >> /root/.ssh/known_hosts && \
       git clone git@github.com:org/private-repo.git
   ```
   Do NOT use `StrictHostKeyChecking=no` as a shortcut — it disables host-key verification entirely. `ssh-keyscan` accepts whatever host key the server presents each time the step runs; nothing is pinned between builds. For stronger assurance, compare it against the provider's published host key fingerprints, or write the published key into `known_hosts` instead of scanning.
6. **Invoke buildx with the secret and SSH sources:**
   ```bash
   # --ssh default forwards this shell's SSH agent (SSH_AUTH_SOCK); list every key the build can use:
   ssh-add -l

   docker buildx build \
       --secret id=npmrc,src=$HOME/.npmrc \
       --ssh default \
       .
   ```
   The `RUN --mount=type=ssh` step can use every key that `ssh-add -l` lists, so expose only the key this build needs. In an interactive terminal, run `ssh-agent bash` to start a shell with a dedicated agent, then run `ssh-add <key-file>`, confirm that `ssh-add -l` lists only that key, and run the build in that shell. A tool that starts a new shell for each command loses that agent between commands, so ask the user to run these steps. Alternatively, pass an unencrypted key file, such as a dedicated deploy key, directly with `--ssh default=<key-file>`; BuildKit rejects passphrase-protected keys in this form, so load those into an agent instead.
7. `.dockerignore` exclusions of `.env` and credential files are **defense in depth**, not the primary mechanism — keep them, but do not rely on them as your only protection.

See `references/multi-stage-builds.md` for per-language patterns (npm, pip, Maven, Go `GOPRIVATE`).

### .dockerignore

Always generate a `.dockerignore` alongside the Dockerfile. Exclude:

- `.git/`, `.github/`, `.vscode/`, `.idea/`
- `node_modules/`, `__pycache__/`, `.venv/`, `vendor/` (when rebuilt in the build stage)
- `*.md`, `LICENSE`, `docs/`
- Build outputs, test artifacts, and IDE configs
- `.env` files and any secrets

See `assets/dockerignore-example` for a comprehensive template.

### Non-root user

Always configure the final image to run as a non-root user.

1. Create a dedicated user and group in the runtime stage:
   ```dockerfile
   RUN addgroup --system --gid 1001 appgroup && \
       adduser --system --uid 1001 --ingroup appgroup appuser
   ```
2. Set ownership on application files: `COPY --from=build --chown=appuser:appgroup /app /app`
3. When combining `--chown` with `COPY --link`, always use the numeric UID:GID you assigned (e.g., `--chown=1001:1001` if you used `--uid 1001 --gid 1001` above), not named users. `--link` creates an independent layer where named users from prior `RUN` instructions are not available.
4. Place the `USER appuser` instruction after all file operations and before `ENTRYPOINT`/`CMD`.
5. On distroless images, use the built-in nonroot user: `USER nonroot:nonroot`.

### Image size optimization

1. Prefer `FROM scratch` (Go static binaries), distroless, or Alpine-based images for the runtime stage.
2. Install OS packages with a BuildKit cache mount rather than `rm -rf`-ing the cache in the same layer — see "Layer caching" above. The cache mount keeps the package cache out of the image layer entirely, so no cleanup step is needed.
3. Do not install documentation, man pages, or debug tools in the runtime image.
4. Use `.dockerignore` aggressively to minimize the build context.

### General rules

- Always include a `# syntax=docker/dockerfile:1` directive as the first line to enable BuildKit features.
- Set `WORKDIR` before any `COPY` or `RUN` instructions — never rely on the default `/`.
- Prefer `ENTRYPOINT` with exec form (`["binary"]`) over shell form.
- Add `EXPOSE` to document the listening port.
- Add metadata labels: `LABEL org.opencontainers.image.source=...`

## Related skills

- For first-time Docker project scaffolding and deciding which files to create, use `docker-project-foundations`.
- For service dependencies, health checks, overrides, networks, and volume patterns, use `docker-compose-patterns`.
- For destructive Docker CLI commands (`docker system prune`, `docker rm -f`, image/network/builder pruning) and a cross-product index of destructive-command guardrails, use `docker-destructive-guardrails`.

## References

- `references/multi-stage-builds.md` — Language-specific multi-stage patterns for Go, Node.js, Python, and Java
- `references/layer-caching.md` — Deep dive on layer ordering, cache invalidation, and BuildKit cache mounts

## Assets

- `assets/Dockerfile.go` — Multi-stage Go build with distroless runtime and non-root user
- `assets/Dockerfile.nodejs` — Multi-stage Node.js build with proper layer caching and non-root user
- `assets/Dockerfile.python` — Python build with virtual env, layer ordering, and non-root user
- `assets/dockerignore-example` — Comprehensive `.dockerignore` template

## Scripts

- **`scripts/verify-build.sh`** — Builds the Dockerfile in the current directory, then reports image size and configured user. Run it from the project root (the directory that contains the `Dockerfile`), with the script path resolved under this skill's directory:
  ```bash
  bash "<skill-dir>/scripts/verify-build.sh" [--help] [IMAGE_NAME]
  ```
  Replace `<skill-dir>` with the absolute path of the folder that contains this `SKILL.md`; the `scripts/` path is relative to that folder, not to the project. Do not change into the skill directory first: the script builds whatever is in the current directory. If the skill directory cannot be resolved, run `docker build -t verify-build-test .`, then `docker images verify-build-test` and `docker inspect verify-build-test --format '{{.Config.User}}'`. Exit status is `0` when all Docker commands succeed or help is requested, the failing Docker command's non-zero status when verification fails, and `2` for invalid arguments.

## Checks

- `checks/verification.md` — Detailed verification runbook for manual review.



---

## Reviewed skill instruction: `.agents/skills/docker-project-foundations/SKILL.md`

---
name: docker-project-foundations
description: Use this skill when setting up, initializing, or Dockerizing a project, even if the user doesn't explicitly mention Docker but describes a need for containerized local development, adding a database or cache dependency, or running services without host-level installs. Covers Dockerfile, compose.yaml, and .dockerignore creation with Docker best practices.
license: Apache-2.0
compatibility: Requires Docker 20.10+ and Docker Compose v2.
---

# Docker Project Foundations

## Overview

This skill guides you in Dockerizing a project from scratch. It focuses on creating the initial Docker file set, choosing a sane layout, and preferring containerized dependencies over host-level installs.

## When to use this skill

Activate this skill when:

- A user asks you to set up, initialize, or Dockerize a project
- A project needs an initial `Dockerfile`, `compose.yaml`, or `.dockerignore` and does not have one
- A user wants to add a service dependency (database, cache, message queue) to a project
- A user asks how to run or develop a project locally and Docker is available

## Do not use this skill when

Do not use this skill when:

- The user explicitly wants to avoid Docker
- The project already has a mature Docker setup and only needs minor edits
- The main task is optimizing an existing `Dockerfile`
- The main task is editing or debugging an existing Compose stack

## Core guidance

### Always create these three files

When Dockerizing a project, always produce all three:

1. **`.dockerignore`** — Create this first so the initial build context is small and safe. See `assets/dockerignore-example` for a reference.
2. **`Dockerfile`** — Create a working starter image definition that the project can build and run with. See `assets/Dockerfile.simple`.
3. **`compose.yaml`** — Create a local development stack that includes the application service and any required dependencies. See `assets/compose-dev.yaml`.

### npm registry credentials

- Exclude `.npmrc` at every depth with `**/.npmrc` in `.dockerignore`; otherwise a broad source copy can persist credentials in image layers.
- The Node.js starter mounts `npmrc` as a BuildKit secret for both `npm ci` steps. Public-package builds need no secret. For private registries, pass the config explicitly:
  ```bash
  DOCKER_BUILDKIT=1 docker build --secret id=npmrc,src="$HOME/.npmrc" .
  ```
  Use the actual config path if the project keeps it elsewhere. Never copy the credential file or pass its values through `ARG` or `ENV`. Dependency scripts run during installation can access the mounted secret; use trusted dependencies and a least-privilege registry token.
- For private-registry builds through Compose, add this optional override as `compose.npm.yaml` alongside the starter's `compose.yaml`:
  ```yaml
  services:
    app:
      build:
        secrets:
          - npmrc
  secrets:
    npmrc:
      file: ${NPMRC_PATH:?Set NPMRC_PATH to your npm config file}
  ```
  Build with `NPMRC_PATH="$HOME/.npmrc" docker compose -f compose.yaml -f compose.npm.yaml build`. This grants build-time access only, not a runtime secret. Public-package builds should omit the override so no credential file is required.

### Prefer Dockerized dependencies over host installs

When a project needs a database (Postgres, MySQL, MongoDB), cache (Redis, Memcached), queue (RabbitMQ, Kafka), or any other infrastructure service:

- **Always** define it as a service in `compose.yaml` instead of telling the user to install it on the host.
- **Never** suggest `brew install postgres`, `apt install redis`, or similar host-level installs for development dependencies.
- Use official Docker images from Docker Hub for these services.
- Configure services with environment variables, not config files baked into images.

### Bootstrap checklist

- Name the file `compose.yaml` rather than legacy Compose filenames.
- Put all three files at the project root unless there is a clear multi-service layout that justifies a `docker/` subdirectory.
- Ensure the initial setup can build and start locally with one command path.
- Bind published application ports to loopback by default. Widen the host address only when another device must reach the development service.
- Keep unauthenticated datastores on the Compose network instead of publishing their ports. If local host tools require database access, publish only to loopback.
- If a development-only credential fallback enables one-command startup, label it clearly and document a `.env` override.
- Use Compose services for local databases, caches, and queues instead of host installs.
- Keep the first scaffold simple; defer detailed image optimization and advanced Compose tuning to the owning skills.

### Development vs production

- Development: Use bind mounts for live reload, publish application ports on loopback by default, and enable verbose logging. Keep unauthenticated datastores on the Compose network; publish a datastore port only on loopback when local host tools require it.
- Production: Use multi-stage builds, copy only built artifacts, do not mount source code, minimize image layers, set appropriate resource limits.
- Keep a single `Dockerfile` that supports both via build stages and build arguments when possible.

### File placement

- Place `Dockerfile` at the project root (or in a `docker/` subdirectory if the project has multiple services).
- Place `compose.yaml` at the project root.
- Place `.dockerignore` at the project root, next to the `Dockerfile`.

## Related skills

- For Dockerfile optimization, cache strategy, non-root execution, and image hardening, use `docker-build-strategies`.
- For service dependencies, health checks, overrides, volumes, networks, and Compose debugging, use `docker-compose-patterns`.
- For destructive Docker CLI commands (`docker system prune`, `docker rm -f`, image/network/builder pruning) and a cross-product index of destructive-command guardrails, use `docker-destructive-guardrails`.

## References

- `references/project-structure.md` — Detailed guidance on Docker project file organization, naming conventions, and multi-service layouts.

## Assets

- `assets/dockerignore-example` — A comprehensive `.dockerignore` for a typical project.
- `assets/compose-dev.yaml` — A development-oriented Compose file with Dockerized dependencies.
- `assets/Dockerfile.simple` — A basic multi-stage Dockerfile following best practices.

## Scripts

- **`scripts/verify-setup.sh`** — Checks that required files exist in the current directory and validates its `compose.yaml`. Run it from the project root, with the script path resolved under this skill's directory:
  ```bash
  bash "<skill-dir>/scripts/verify-setup.sh" [--help]
  ```
  Replace `<skill-dir>` with the absolute path of the folder that contains this `SKILL.md`; the `scripts/` path is relative to that folder, not to the project. Do not change into the skill directory first: the script checks the current directory. If the skill directory cannot be resolved, check that `.dockerignore`, `Dockerfile`, and `compose.yaml` exist in the project root, then run `docker compose config --quiet`. Exit status is `0` when verification succeeds or help is requested, `1` when required files are missing or the Compose configuration is invalid, and `2` for invalid arguments.

## Checks

- `checks/verification.md` — Detailed verification checklist for manual review.



---

## Reviewed skill instruction: `.agents/skills/fba/SKILL.md`

---
name: fba
description: FastAPI Best Architecture (fba) project development guide. Use when working in fba projects to design, implement, review, or document APIs, Schema, Service, CRUD, Model, configuration, response contracts, pagination, cache, Celery, i18n, coding style, plugin development, plugin README files, plugin sharing, plugin publishing, or plugin marketplace updates.
---

# FastAPI Best Architecture

Official documentation: [external address omitted in offline package]

Use this skill to follow fba architecture and plugin conventions. Load the required baseline below, then only the additional references needed for the task.

## Required Coding Baseline

For every backend Python implementation, fix, refactor, or code review, read `references/coding-style.md` and `references/naming.md` before working on code. These rules apply to ordinary development as well as explicit style requests; the user does not need to repeat them. Apply them to maintained application and plugin code, including runtime modules, utilities, and relevant tests, while preserving framework-required contracts.

For cross-layer features, directory changes, or SDK integrations, also read `references/development.md` before choosing module boundaries, then load the layer-specific references.

Keep the requested scope: a comprehensive plugin review covers all maintained modules in that plugin and affected tests, not only API/Service/CRUD files. An ordinary feature or fix does not authorize unrelated repository-wide cleanup. For documentation-only work, load the relevant documentation reference without the Python baseline.

Before completion, apply the review checks in `references/coding-style.md`. Ruff passing alone does not verify function design, test-driven helper extraction, or layer boundaries.

## Core Architecture

Project adopts a layered backend architecture centered on API, Service, and CRUD, with Schema and Model as explicit data contracts:

| Layer   | Responsibility                                                     |
|---------|--------------------------------------------------------------------|
| API     | Route processing, parameter validation, and response return        |
| Schema  | Data transfer objects, request/response data structure definitions |
| Service | Business logic, data processing, exception handling                |
| CRUD    | Database operations (inherits `CRUDPlus`)                          |
| Model   | ORM models (inherits `Base`)                                       |

## Development Workflow

1. Define database models (model)
2. Define data validation models (schema)
3. Define routes (router)
4. Write business logic (service)
5. Write database operations (crud)

## Reference Selection

| Task | Read |
|------|------|
| Feature/module development flow, Service/CRUD placement, pagination, cache, Celery, i18n, code generation | `references/development.md` |
| API routes, dependencies, response patterns, auth, permissions | `references/api.md` |
| Pydantic request/response DTOs | `references/schema.md` |
| SQLAlchemy models and migrations | `references/model.md` |
| CRUD, Service, API, Schema, entity and table prefix naming | `references/naming.md` |
| Backend/frontend plugin development and plugin README files | `references/plugin.md` |
| Plugin sharing, public repositories, marketplace PRs, submodules, updates | `references/plugin-sharing.md` |
| Every backend Python implementation/review: functions, private helpers, test boundaries, typing, formatting, comments, docstrings | `references/coding-style.md` (required baseline) |
| Global settings and configuration | `references/config.md` |

## Plugin Work

When creating, reviewing, or updating plugins:

1. Read `references/plugin.md` for plugin type, structure, manifest, configuration, hooks, SQL, and README rules
2. Read `references/plugin-sharing.md` when the task involves sharing, publishing, updating, marketplace PRs, plugin repositories, or Git submodules
3. Prefer source-code behavior from `fastapi-best-architecture` when docs and implementation differ
4. Do not perform git add, commit, push, or PR actions unless the user explicitly asks

## CLI

Execute `fba -h` for more details.



---

## Reviewed skill instruction: `.agents/skills/mcp-builder/SKILL.md`

---
name: mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
license: Complete terms in LICENSE.txt
---

# MCP Server Development Guide

## Overview

Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks.

---

# Process

## 🚀 High-Level Workflow

Creating a high-quality MCP server involves four main phases:

### Phase 1: Deep Research and Planning

#### 1.1 Understand Modern MCP Design

**API Coverage vs. Workflow Tools:**
Balance comprehensive API endpoint coverage with specialized workflow tools. Workflow tools can be more convenient for specific tasks, while comprehensive coverage gives agents flexibility to compose operations. Performance varies by client—some clients benefit from code execution that combines basic tools, while others work better with higher-level workflows. When uncertain, prioritize comprehensive API coverage.

**Tool Naming and Discoverability:**
Clear, descriptive tool names help agents find the right tools quickly. Use consistent prefixes (e.g., `github_create_issue`, `github_list_repos`) and action-oriented naming.

**Context Management:**
Agents benefit from concise tool descriptions and the ability to filter/paginate results. Design tools that return focused, relevant data. Some clients support code execution which can help agents filter and process data efficiently.

**Actionable Error Messages:**
Error messages should guide agents toward solutions with specific suggestions and next steps.

#### 1.2 Study MCP Protocol Documentation

**Navigate the MCP specification:**

Start with the sitemap to find relevant pages: `[external address omitted in offline package]`

Then fetch specific pages with `.md` suffix for markdown format (e.g., `[external address omitted in offline package]`).

Key pages to review:
- Specification overview and architecture
- Transport mechanisms (streamable HTTP, stdio)
- Tool, resource, and prompt definitions

#### 1.3 Study Framework Documentation

**Recommended stack:**
- **Language**: TypeScript (high-quality SDK support and good compatibility in many execution environments e.g. MCPB. Plus AI models are good at generating TypeScript code, benefiting from its broad usage, static typing and good linting tools)
- **Transport**: Streamable HTTP for remote servers, using stateless JSON (simpler to scale and maintain, as opposed to stateful sessions and streaming responses). stdio for local servers.

**Load framework documentation:**

- **MCP Best Practices**: [📋 View Best Practices](./reference/mcp_best_practices.md) - Core guidelines

**For TypeScript (recommended):**
- **TypeScript SDK**: Use WebFetch to load `[external address omitted in offline package]`
- [⚡ TypeScript Guide](./reference/node_mcp_server.md) - TypeScript patterns and examples

**For Python:**
- **Python SDK**: Use WebFetch to load `[external address omitted in offline package]`
- [🐍 Python Guide](./reference/python_mcp_server.md) - Python patterns and examples

#### 1.4 Plan Your Implementation

**Understand the API:**
Review the service's API documentation to identify key endpoints, authentication requirements, and data models. Use web search and WebFetch as needed.

**Tool Selection:**
Prioritize comprehensive API coverage. List endpoints to implement, starting with the most common operations.

---

### Phase 2: Implementation

#### 2.1 Set Up Project Structure

See language-specific guides for project setup:
- [⚡ TypeScript Guide](./reference/node_mcp_server.md) - Project structure, package.json, tsconfig.json
- [🐍 Python Guide](./reference/python_mcp_server.md) - Module organization, dependencies

#### 2.2 Implement Core Infrastructure

Create shared utilities:
- API client with authentication
- Error handling helpers
- Response formatting (JSON/Markdown)
- Pagination support

#### 2.3 Implement Tools

For each tool:

**Input Schema:**
- Use Zod (TypeScript) or Pydantic (Python)
- Include constraints and clear descriptions
- Add examples in field descriptions

**Output Schema:**
- Define `outputSchema` where possible for structured data
- Use `structuredContent` in tool responses (TypeScript SDK feature)
- Helps clients understand and process tool outputs

**Tool Description:**
- Concise summary of functionality
- Parameter descriptions
- Return type schema

**Implementation:**
- Async/await for I/O operations
- Proper error handling with actionable messages
- Support pagination where applicable
- Return both text content and structured data when using modern SDKs

**Annotations:**
- `readOnlyHint`: true/false
- `destructiveHint`: true/false
- `idempotentHint`: true/false
- `openWorldHint`: true/false

---

### Phase 3: Review and Test

#### 3.1 Code Quality

Review for:
- No duplicated code (DRY principle)
- Consistent error handling
- Full type coverage
- Clear tool descriptions

#### 3.2 Build and Test

**TypeScript:**
- Run `npm run build` to verify compilation
- Test with MCP Inspector: `npx @modelcontextprotocol/inspector`

**Python:**
- Verify syntax: `python -m py_compile your_server.py`
- Test with MCP Inspector

See language-specific guides for detailed testing approaches and quality checklists.

---

### Phase 4: Create Evaluations

After implementing your MCP server, create comprehensive evaluations to test its effectiveness.

**Load [✅ Evaluation Guide](./reference/evaluation.md) for complete evaluation guidelines.**

#### 4.1 Understand Evaluation Purpose

Use evaluations to test whether LLMs can effectively use your MCP server to answer realistic, complex questions.

#### 4.2 Create 10 Evaluation Questions

To create effective evaluations, follow the process outlined in the evaluation guide:

1. **Tool Inspection**: List available tools and understand their capabilities
2. **Content Exploration**: Use READ-ONLY operations to explore available data
3. **Question Generation**: Create 10 complex, realistic questions
4. **Answer Verification**: Solve each question yourself to verify answers

#### 4.3 Evaluation Requirements

Ensure each question is:
- **Independent**: Not dependent on other questions
- **Read-only**: Only non-destructive operations required
- **Complex**: Requiring multiple tool calls and deep exploration
- **Realistic**: Based on real use cases humans would care about
- **Verifiable**: Single, clear answer that can be verified by string comparison
- **Stable**: Answer won't change over time

#### 4.4 Output Format

Create an XML file with this structure:

```xml
<evaluation>
  <qa_pair>
    <question>Find discussions about AI model launches with animal codenames. One model needed a specific safety designation that uses the format ASL-X. What number X was being determined for the model named after a spotted wild cat?</question>
    <answer>3</answer>
  </qa_pair>
<!-- More qa_pairs... -->
</evaluation>
```

---

# Reference Files

## 📚 Documentation Library

Load these resources as needed during development:

### Core MCP Documentation (Load First)
- **MCP Protocol**: Start with sitemap at `[external address omitted in offline package]`, then fetch specific pages with `.md` suffix
- [📋 MCP Best Practices](./reference/mcp_best_practices.md) - Universal MCP guidelines including:
  - Server and tool naming conventions
  - Response format guidelines (JSON vs Markdown)
  - Pagination best practices
  - Transport selection (streamable HTTP vs stdio)
  - Security and error handling standards

### SDK Documentation (Load During Phase 1/2)
- **Python SDK**: Fetch from `[external address omitted in offline package]`
- **TypeScript SDK**: Fetch from `[external address omitted in offline package]`

### Language-Specific Implementation Guides (Load During Phase 2)
- [🐍 Python Implementation Guide](./reference/python_mcp_server.md) - Complete Python/FastMCP guide with:
  - Server initialization patterns
  - Pydantic model examples
  - Tool registration with `@mcp.tool`
  - Complete working examples
  - Quality checklist

- [⚡ TypeScript Implementation Guide](./reference/node_mcp_server.md) - Complete TypeScript guide with:
  - Project structure
  - Zod schema patterns
  - Tool registration with `server.registerTool`
  - Complete working examples
  - Quality checklist

### Evaluation Guide (Load During Phase 4)
- [✅ Evaluation Guide](./reference/evaluation.md) - Complete evaluation creation guide with:
  - Question creation guidelines
  - Answer verification strategies
  - XML format specifications
  - Example questions and answers
  - Running an evaluation with the provided scripts



---

## Reviewed skill instruction: `.agents/skills/performance/SKILL.md`

---
name: performance
description: Optimize web performance for faster loading and better user experience. Use when asked to "speed up my site", "optimize performance", "reduce load time", "fix slow loading", "improve page speed", or "performance audit".
license: MIT
metadata:
  author: web-quality-skills
  version: "2.0"
---

# Performance optimization

Evidence-led performance optimization using real-user signals for prioritization and browser traces for diagnosis. Focuses on loading speed, runtime responsiveness, and resource delivery.

## How it works

1. If a page can run, read [the measurement workflow](references/MEASUREMENT.md) and establish a field-plus-lab baseline before editing.
2. Prioritize poor real-user Core Web Vitals. Use a DevTools performance trace and its focused insights to find the cause.
3. Inspect and change only the code or assets connected to measured bottlenecks.
4. Re-run equivalent lab measurements and report before/after values, conditions, and uncertainty. Field verification remains pending until enough new user data arrives.

When no runnable page exists, perform static inspection but call findings **hypotheses**, not measured regressions. Include the command or browser workflow that can verify each high-impact hypothesis.

Prefer a browser tool that records a performance trace and exposes focused insights. With Chrome DevTools MCP, use `performance_start_trace` and `performance_analyze_insight`; do not route performance through `lighthouse_audit`, which covers non-performance Lighthouse categories.

## Starting performance budget

Budgets must reflect the product's target devices, networks, page types, and user journeys. The values below are initial guardrails for a typical content or commerce page, not universal pass/fail criteria. Preserve an existing project budget when one is already defined.

| Resource | Budget | Rationale |
|----------|--------|-----------|
| Total page weight | < 1.5 MB | Bounds transfer time and data cost on constrained target networks; calibrate with representative pages |
| JavaScript (compressed) | < 300 KB | Protect parse and execution cost |
| CSS (compressed) | < 100 KB | Limit render-blocking work |
| Images (above-fold) | < 500 KB | Protect likely LCP resources |
| Fonts | < 100 KB | Limit critical font transfer |
| Third-party | < 200 KB | Bound code outside product control |

## Critical rendering path

### Server response
* **TTFB < 800ms.** Time to First Byte should be fast. Use CDN, caching, and efficient backends.
* **Enable compression.** Gzip or Brotli for text assets. Brotli preferred (15-20% smaller).
* **HTTP/2 or HTTP/3.** Multiplexing reduces connection overhead.
* **Edge caching.** Cache HTML at CDN edge when possible.
* **Consider Early Hints (HTTP 103) for measured document latency.** If a trace shows slow HTML generation and stable critical subresources, send an interim `103` with `Link` headers before the normal final response from the same request. Use HTTP/2 or later. A CDN may synthesize the `103` from `Link` headers on an earlier `200`, or the origin/edge handler can emit it directly. Unsupported clients continue to the final response, but confirm current browser and infrastructure support. Limit hints to proven critical preloads or preconnects: inaccurate hints waste bandwidth. Cloudflare reported a 20–30% LCP improvement in an artificial, image-heavy test; treat that as a vendor case study, not an expected saving, and measure your result. See MDN's 103 implementation example and the Cloudflare study.

### Resource loading

**Preconnect to required origins:**
```html
<link rel="preconnect" href="[external address omitted in offline package]>
<link rel="preconnect" href="[external address omitted in offline package] crossorigin>
```

**Preload critical resources:**

Preload only resources whose late discovery is visible in the trace. Each preload competes for bandwidth and an unnecessary high-priority request can delay LCP.

```html
<!-- LCP image -->
<link rel="preload" href="/hero.webp" as="image" fetchpriority="high">

<!-- Critical font -->
<link rel="preload" href="/font.woff2" as="font" type="font/woff2" crossorigin>
```

**Prerender likely-next navigations** with the Speculation Rules API:
```html
<script type="speculationrules">
{
  "prerender": [{
    "where": { "href_matches": "/*" },
    "eagerness": "moderate"
  }]
}
</script>
```
`moderate` waits for a stronger intent signal than eager modes. Measure prediction hit rate, transferred bytes, and server cost; a wrong prerender is roughly an unused navigation. See [core-web-vitals → LCP](../core-web-vitals/SKILL.md#lcp-largest-contentful-paint) for the tradeoffs and the `prerenderingchange` gating needed for analytics.

**Defer non-critical CSS:**
```html
<!-- Critical CSS inlined -->
<style>/* Above-fold styles */</style>

<!-- Non-critical CSS -->
<link rel="preload" href="/styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/styles.css"></noscript>
```

### JavaScript optimization

**Defer non-essential scripts:**
```html
<!-- Parser-blocking (avoid) -->
<script src="/critical.js"></script>

<!-- Deferred (preferred) -->
<script defer src="/app.js"></script>

<!-- Async (for independent scripts) -->
<script async src="/analytics.js"></script>

<!-- Module (deferred by default) -->
<script type="module" src="/app.mjs"></script>
```

**Code splitting patterns:**
```javascript
// Route-based splitting
const Dashboard = lazy(() => import('./Dashboard'));

// Component-based splitting
const HeavyChart = lazy(() => import('./HeavyChart'));

// Feature-based splitting
if (user.isPremium) {
  const PremiumFeatures = await import('./PremiumFeatures');
}
```

**Tree shaking best practices:**
```javascript
// ❌ Imports entire library
import _ from 'lodash';
_.debounce(fn, 300);

// ✅ Imports only what's needed
import debounce from 'lodash/debounce';
debounce(fn, 300);
```

## Image optimization

### Format selection
| Format | Use case | Browser support |
|--------|----------|-----------------|
| AVIF | Photos, best compression | 92%+ |
| WebP | Photos, good fallback | 97%+ |
| PNG | Graphics with transparency | Universal |
| SVG | Icons, logos, illustrations | Universal |

### Responsive images
```html
<picture>
  <!-- AVIF for modern browsers -->
  <source 
    type="image/avif"
    srcset="hero-400.avif 400w,
            hero-800.avif 800w,
            hero-1200.avif 1200w"
    sizes="(max-width: 600px) 100vw, 50vw">
  
  <!-- WebP fallback -->
  <source 
    type="image/webp"
    srcset="hero-400.webp 400w,
            hero-800.webp 800w,
            hero-1200.webp 1200w"
    sizes="(max-width: 600px) 100vw, 50vw">
  
  <!-- JPEG fallback -->
  <img 
    src="hero-800.jpg"
    srcset="hero-400.jpg 400w,
            hero-800.jpg 800w,
            hero-1200.jpg 1200w"
    sizes="(max-width: 600px) 100vw, 50vw"
    width="1200" 
    height="600"
    alt="Hero image"
    loading="lazy"
    decoding="async">
</picture>
```

### LCP image priority
```html
<!-- Above-fold LCP image: eager loading, high priority -->
<img 
  src="hero.webp" 
  fetchpriority="high"
  loading="eager"
  decoding="sync"
  alt="Hero">

<!-- Below-fold images: lazy loading -->
<img 
  src="product.webp" 
  loading="lazy"
  decoding="async"
  alt="Product">
```

## Font optimization

### Loading strategy
```css
/* System font stack as fallback */
body {
  font-family: 'Custom Font', -apple-system, BlinkMacSystemFont, 
               'Segoe UI', Roboto, sans-serif;
}

/* Prevent invisible text */
@font-face {
  font-family: 'Custom Font';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap; /* or optional for non-critical */
  font-weight: 400;
  font-style: normal;
  unicode-range: U+0000-00FF; /* Subset to Latin */
}
```

### Preloading critical fonts
```html
<link rel="preload" href="/fonts/heading.woff2" as="font" type="font/woff2" crossorigin>
```

### Variable fonts
```css
/* One file instead of multiple weights */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-display: swap;
}
```

## Caching strategy

### Cache-Control headers
```
# HTML (short or no cache)
Cache-Control: no-cache, must-revalidate

# Static assets with hash (immutable)
Cache-Control: public, max-age=31536000, immutable

# Static assets without hash
Cache-Control: public, max-age=86400, stale-while-revalidate=604800

# API responses
Cache-Control: private, max-age=0, must-revalidate
```

### Service worker caching
```javascript
// Cache-first for static assets
self.addEventListener('fetch', (event) => {
  if (event.request.destination === 'image' ||
      event.request.destination === 'style' ||
      event.request.destination === 'script') {
    event.respondWith(
      caches.match(event.request).then((cached) => {
        return cached || fetch(event.request).then((response) => {
          const clone = response.clone();
          caches.open('static-v1').then((cache) => cache.put(event.request, clone));
          return response;
        });
      })
    );
  }
});
```

## Runtime performance

### Avoid layout thrashing
```javascript
// ❌ Forces multiple reflows
elements.forEach(el => {
  const height = el.offsetHeight; // Read
  el.style.height = height + 10 + 'px'; // Write
});

// ✅ Batch reads, then batch writes
const heights = elements.map(el => el.offsetHeight); // All reads
elements.forEach((el, i) => {
  el.style.height = heights[i] + 10 + 'px'; // All writes
});
```

### Debounce expensive operations
```javascript
function debounce(fn, delay) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
}

// Debounce scroll/resize handlers
window.addEventListener('scroll', debounce(handleScroll, 100));
```

### Use requestAnimationFrame
```javascript
// ❌ May cause jank
setInterval(animate, 16);

// ✅ Synced with display refresh
function animate() {
  // Animation logic
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
```

### Virtualize long lists
```javascript
// For lists > 100 items, render only visible items
// Use libraries like react-window, vue-virtual-scroller, or native CSS:
.virtual-list {
  content-visibility: auto;
  contain-intrinsic-size: 0 50px; /* Estimated item height */
}
```

### Smooth navigations with View Transitions

The View Transitions API lets the browser cross-fade (or custom-animate) between two DOM states using a single GPU-composited snapshot — no double-render, no layout thrash, and the snapshot doesn't count toward CLS.

**Same-document (SPA-style) — Baseline 2026:**
```javascript
// Wrap the DOM mutation that swaps the view
function navigate(newView) {
  if (!document.startViewTransition) return swapDOM(newView);
  document.startViewTransition(() => swapDOM(newView));
}
```

**Cross-document (MPA-style) — Chromium-stable, progressive enhancement elsewhere:**
```css
/* On both source and destination pages */
@view-transition { navigation: auto; }
```
That's the entire integration — same-origin navigations now fade automatically. To opt specific elements into shared-element transitions (e.g. a thumbnail expanding into a hero), give them a matching `view-transition-name`:
```css
.product-thumb[data-id="42"], .product-hero { view-transition-name: product-42; }
```

Pair this with Speculation Rules (above) for instant + animated navigations.

## Third-party scripts

### Load strategies
```javascript
// ❌ Blocks main thread
<script src="[external address omitted in offline package]></script>

// ✅ Async loading
<script async src="[external address omitted in offline package]></script>

// ✅ Delay until interaction
<script>
document.addEventListener('DOMContentLoaded', () => {
  const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      const script = document.createElement('script');
      script.src = '[external address omitted in offline package]
      document.body.appendChild(script);
      observer.disconnect();
    }
  });
  observer.observe(document.querySelector('#widget-container'));
});
</script>
```

### Facade pattern
```html
<!-- Show static placeholder until interaction -->
<div class="youtube-facade" 
     data-video-id="abc123" 
     onclick="loadYouTube(this)">
  <img src="/thumbnails/abc123.jpg" alt="Video title">
  <button aria-label="Play video">▶</button>
</div>
```

## Measurement

Use [the measurement workflow](references/MEASUREMENT.md) whenever a URL is runnable. It defines Chrome DevTools MCP routing, CrUX and fallback sources, repeatable lab conditions, and a compact evidence format.

| Metric | Kind | Interpretation |
|--------|------|----------------|
| LCP, INP, CLS at p75 | Field | User-outcome Core Web Vitals; use for pass/fail prioritization |
| LCP, CLS in a trace | Lab | Reproducible diagnostic values for one navigation |
| TBT | Lab | Main-thread blocking diagnostic and a rough INP proxy, not field INP |
| FCP, Speed Index | Lab | Loading diagnostics, not Core Web Vitals |

Raw `PerformanceObserver` snippets are useful for the current browser session but are not real-user data by themselves. When the user wants production telemetry, read [the first-party RUM reference](references/RUM.md) and prefer `web-vitals` over a hand-rolled metric implementation.

## References

For Core Web Vitals specific optimizations, see [Core Web Vitals](../core-web-vitals/SKILL.md).



---

## Reviewed skill instruction: `.agents/skills/prompt-engineering-patterns/SKILL.md`

---
name: prompt-engineering-patterns
description: >-
  This skill should be used when the user asks to "optimize a prompt", "improve prompt
  performance", "design a prompt template", "write better prompts", "debug prompt issues", "use
  chain-of-thought", "structured prompting", "few-shot prompting", or wants to apply advanced
  prompt engineering patterns for production LLM applications.
---

# Prompt Engineering Patterns

Master advanced prompt engineering techniques to maximize LLM performance, reliability, and controllability.

## When to Use This Skill

- Designing complex prompts for production LLM applications
- Optimizing prompt performance and consistency
- Implementing structured reasoning patterns (chain-of-thought, tree-of-thought)
- Building few-shot learning systems with dynamic example selection
- Creating reusable prompt templates with variable interpolation
- Debugging and refining prompts that produce inconsistent outputs
- Implementing system prompts for specialized AI assistants
- Using structured outputs (JSON mode) for reliable parsing

## Core Capabilities

### 1. Few-Shot Learning

- Example selection strategies (semantic similarity, diversity sampling)
- Balancing example count with context window constraints
- Constructing effective demonstrations with input-output pairs
- Dynamic example retrieval from knowledge bases
- Handling edge cases through strategic example selection

### 2. Chain-of-Thought Prompting

- Step-by-step reasoning elicitation
- Zero-shot CoT with "Let's think step by step"
- Few-shot CoT with reasoning traces
- Self-consistency techniques (sampling multiple reasoning paths)
- Verification and validation steps

### 3. Structured Outputs

- JSON mode for reliable parsing
- Pydantic schema enforcement
- Type-safe response handling
- Error handling for malformed outputs

### 4. Prompt Optimization

- Iterative refinement workflows
- A/B testing prompt variations
- Measuring prompt performance metrics (accuracy, consistency, latency)
- Reducing token usage while maintaining quality
- Handling edge cases and failure modes

### 5. Template Systems

- Variable interpolation and formatting
- Conditional prompt sections
- Multi-turn conversation templates
- Role-based prompt composition
- Modular prompt components

### 6. System Prompt Design

- Setting model behavior and constraints
- Defining output formats and structure
- Establishing role and expertise
- Safety guidelines and content policies
- Context setting and background information

## Quick Start

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Define structured output schema
class SQLQuery(BaseModel):
    query: str = Field(description="The SQL query")
    explanation: str = Field(description="Brief explanation of what the query does")
    tables_used: list[str] = Field(description="List of tables referenced")

# Initialize model with structured output
llm = ChatAnthropic(model="claude-sonnet-5")
structured_llm = llm.with_structured_output(SQLQuery)

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert SQL developer. Generate efficient, secure SQL queries.
    Always use parameterized queries to prevent SQL injection.
    Explain your reasoning briefly."""),
    ("user", "Convert this to SQL: {query}")
])

# Create chain
chain = prompt | structured_llm

# Use
result = await chain.ainvoke({
    "query": "Find all users who registered in the last 30 days"
})
print(result.query)
print(result.explanation)
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

1. **Be Specific**: Vague prompts produce inconsistent results
2. **Show, Don't Tell**: Examples are more effective than descriptions
3. **Use Structured Outputs**: Enforce schemas with Pydantic for reliability
4. **Test Extensively**: Evaluate on diverse, representative inputs
5. **Iterate Rapidly**: Small changes can have large impacts
6. **Monitor Performance**: Track metrics in production
7. **Version Control**: Treat prompts as code with proper versioning
8. **Document Intent**: Explain why prompts are structured as they are

## Common Pitfalls

- **Over-engineering**: Starting with complex prompts before trying simple ones
- **Example pollution**: Using examples that don't match the target task
- **Context overflow**: Exceeding token limits with excessive examples
- **Ambiguous instructions**: Leaving room for multiple interpretations
- **Ignoring edge cases**: Not testing on unusual or boundary inputs
- **No error handling**: Assuming outputs will always be well-formed
- **Hardcoded values**: Not parameterizing prompts for reuse

## Success Metrics

Track these KPIs for your prompts:

- **Accuracy**: Correctness of outputs
- **Consistency**: Reproducibility across similar inputs
- **Latency**: Response time (P50, P95, P99)
- **Token Usage**: Average tokens per request
- **Success Rate**: Percentage of valid, parseable outputs
- **User Satisfaction**: Ratings and feedback



---

## Reviewed skill instruction: `.agents/skills/rag-implementation/SKILL.md`

---
name: rag-implementation
description: Build Retrieval-Augmented Generation (RAG) systems for LLM applications with vector databases and semantic search. Use when implementing knowledge-grounded AI, building document Q&A systems, or integrating LLMs with external knowledge bases.
---

# RAG Implementation

Master Retrieval-Augmented Generation (RAG) to build LLM applications that provide accurate, grounded responses using external knowledge sources.

## When to Use This Skill

- Building Q&A systems over proprietary documents
- Creating chatbots with current, factual information
- Implementing semantic search with natural language queries
- Reducing hallucinations with grounded responses
- Enabling LLMs to access domain-specific knowledge
- Building documentation assistants
- Creating research tools with source citation

## Core Components

### 1. Vector Databases

**Purpose**: Store and retrieve document embeddings efficiently

**Options:**

- **Pinecone**: Managed, scalable, serverless
- **Weaviate**: Open-source, hybrid search, GraphQL
- **Milvus**: High performance, on-premise
- **Chroma**: Lightweight, easy to use, local development
- **Qdrant**: Fast, filtered search, Rust-based
- **pgvector**: PostgreSQL extension, SQL integration

### 2. Embeddings

**Purpose**: Convert text to numerical vectors for similarity search

**Models (2026):**
| Model | Dimensions | Best For |
|-------|------------|----------|
| **voyage-3-large** | 1024 | Claude apps (Anthropic recommended) |
| **voyage-code-3** | 1024 | Code search |
| **text-embedding-3-large** | 3072 | OpenAI apps, high accuracy |
| **text-embedding-3-small** | 1536 | OpenAI apps, cost-effective |
| **bge-large-en-v1.5** | 1024 | Open source, local deployment |
| **multilingual-e5-large** | 1024 | Multi-language support |

### 3. Retrieval Strategies

**Approaches:**

- **Dense Retrieval**: Semantic similarity via embeddings
- **Sparse Retrieval**: Keyword matching (BM25, TF-IDF)
- **Hybrid Search**: Combine dense + sparse with weighted fusion
- **Multi-Query**: Generate multiple query variations
- **HyDE**: Generate hypothetical documents for better retrieval

### 4. Reranking

**Purpose**: Improve retrieval quality by reordering results

**Methods:**

- **Cross-Encoders**: BERT-based reranking (ms-marco-MiniLM)
- **Cohere Rerank**: API-based reranking
- **Maximal Marginal Relevance (MMR)**: Diversity + relevance
- **LLM-based**: Use LLM to score relevance

## Quick Start with LangGraph

```python
from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic
from langchain_voyageai import VoyageAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import TypedDict, Annotated

class RAGState(TypedDict):
    question: str
    context: list[Document]
    answer: str

# Initialize components
llm = ChatAnthropic(model="claude-sonnet-5")
embeddings = VoyageAIEmbeddings(model="voyage-3-large")
vectorstore = PineconeVectorStore(index_name="docs", embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# RAG prompt
rag_prompt = ChatPromptTemplate.from_template(
    """Answer based on the context below. If you cannot answer, say so.

    Context:
    {context}

    Question: {question}

    Answer:"""
)

async def retrieve(state: RAGState) -> RAGState:
    """Retrieve relevant documents."""
    docs = await retriever.ainvoke(state["question"])
    return {"context": docs}

async def generate(state: RAGState) -> RAGState:
    """Generate answer from context."""
    context_text = "\n\n".join(doc.page_content for doc in state["context"])
    messages = rag_prompt.format_messages(
        context=context_text,
        question=state["question"]
    )
    response = await llm.ainvoke(messages)
    return {"answer": response.content}

# Build RAG graph
builder = StateGraph(RAGState)
builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

rag_chain = builder.compile()

# Use
result = await rag_chain.ainvoke({"question": "What are the main features?"})
print(result["answer"])
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.




---

## Reviewed skill instruction: `.agents/skills/supabase/SKILL.md`

---
name: supabase
description: "Use when doing ANY task involving Supabase. Triggers: Supabase products (Database, Auth, Edge Functions, Realtime, Storage, Vectors, Cron, Queues); client libraries and SSR integrations (supabase-js, @supabase/ssr) in Next.js, React, SvelteKit, Astro, Remix; auth issues (login, logout, sessions, JWT, cookies, getSession, getUser, getClaims, RLS); Supabase CLI or MCP server; schema changes, migrations, declarative schemas, security audits, Postgres extensions (pg_graphql, pg_cron, pg_vector); debugging and troubleshooting errors or unexpected behavior on Supabase projects (HTTP errors, Postgres errors, RLS surprises, permission denied, schema cache issues, timeouts, Edge Function crashes, Realtime drops, Storage failures) and reading or querying logs (Logs Explorer, ClickHouse)."
metadata:
  author: supabase
  version: "0.1.2"
---

# Supabase

## Core Principles

**1. Supabase changes frequently — verify against changelog and current docs before implementing.**
Do not rely on training data for Supabase features. Function signatures, config.toml settings, and API conventions change between versions.

First, fetch `[external address omitted in offline package]` (a lightweight summary index — not a heavy pull), scan for `breaking-change` tags relevant to your task, and follow the linked page for any that apply. Then look up the relevant topic using the documentation access methods below.

**2. Verify your work.**
After implementing any fix, run a test query to confirm the change works. A fix without verification is incomplete.

**3. Recover from errors, don't loop.**
If an approach fails after 2-3 attempts, stop and reconsider. Try a different method, check documentation, inspect the error more carefully, and review relevant logs when available. Supabase issues are not always solved by retrying the same command, and the answer is not always in the logs, but logs are often worth checking before proceeding.

**4. Exposing tables to the Data API:** Depending on the user's Data API settings, newly created tables may not be automatically exposed via the Data (REST) API. If this is the case, `anon` and `authenticated` roles will need to be explicitly granted access.

> Note that this is separate from RLS, which controls which _rows_ are visible once a table is accessible, not whether the table is accessible at all.

When a user reports a SQL-created table is unexpectedly inaccessible, check their Data API settings and whether the roles have been granted access via explicit `GRANT` SQL. When granting public (`anon`/`authenticated`) access, always enable RLS too. See Exposing a Table to the Data API for the full setup workflow.

**5. RLS in exposed schemas.**
Enable RLS on every table in any exposed schema, which includes `public` by default. This is critical in Supabase because tables in exposed schemas can be reachable through the Data API when the `anon`/`authenticated` roles have access (see Exposing a Table to the Data API). For private schemas, prefer RLS as defense in depth. After enabling RLS, create policies that match the actual access model rather than defaulting every table to the same `auth.uid()` pattern.

**6. Security checklist.**
When working on any Supabase task that touches auth, RLS, views, storage, or user data, run through this checklist. These are Supabase-specific security traps that silently create vulnerabilities:

- **Auth and session security**
  - **Never use `user_metadata` claims in JWT-based authorization decisions.** In Supabase, `raw_user_meta_data` is user-editable and can appear in `auth.jwt()`, so it is unsafe for RLS policies or any other authorization logic. Store authorization data in `raw_app_meta_data` / `app_metadata` instead.
  - **Deleting a user does not invalidate existing access tokens.** Sign out or revoke sessions first, keep JWT expiry short for sensitive apps, and for strict guarantees validate `session_id` against `auth.sessions` on sensitive operations.
  - **If you use `app_metadata` or `auth.jwt()` for authorization, remember JWT claims are not always fresh until the user's token is refreshed.**

- **API key and client exposure**
  - **Never expose the `service_role` or secret key in public clients.** Prefer publishable keys for frontend code. Legacy `anon` keys are only for compatibility. In Next.js, any `NEXT_PUBLIC_` env var is sent to the browser.
  - **Use scoped personal access tokens for the Management API, CLI, and MCP server.** A classic personal access token carries the user's full account access, on every organization and project. For scripts, CI, and agents, have the user create a scoped token limited to the organizations, projects, and permissions the task needs. The personal access tokens guide lists the permission each Management API endpoint and MCP tool requires. Look permissions up there rather than guessing.

- **RLS, views, and privileged database code**
  - **Views bypass RLS by default.** In Postgres 15 and above, use `CREATE VIEW ... WITH (security_invoker = true)`. In older versions of Postgres, protect your views by revoking access from the `anon` and `authenticated` roles, or by putting them in an unexposed schema.
  - **UPDATE requires a SELECT policy.** In Postgres RLS, an UPDATE needs to first SELECT the row. Without a SELECT policy, updates silently return 0 rows — no error, just no change.
  - **`auth.role()` is deprecated — use the `TO` clause instead.** Supabase has deprecated `auth.role()` in favour of specifying the target role directly on the policy with `TO authenticated` or `TO anon`. Beyond deprecation, `auth.role() = 'authenticated'` breaks silently when anonymous sign-ins are enabled, because anonymous users carry the `authenticated` Postgres role and pass the check regardless of whether the user is genuinely signed in.
    ```sql
    -- Deprecated (do not use)
    create policy "example" on table_name for select
    using ( auth.role() = 'authenticated' );
    ```
  - **`TO authenticated` alone is authentication without authorization (BOLA / IDOR).** Using `TO authenticated` only checks the role — it does not restrict which rows a user can access. The correct pattern combines `TO authenticated` with an ownership predicate in `USING`:
    ```sql
    create policy "example" on table_name for select
    to authenticated
    using ( (select auth.uid()) = user_id );
    ```
  - **UPDATE policies require both `USING` and `WITH CHECK`.** Without `WITH CHECK`, a user can reassign a row's `user_id` to another user:
    ```sql
    create policy "example" on table_name for update
    to authenticated
    using ( (select auth.uid()) = user_id )
    with check ( (select auth.uid()) = user_id );
    ```
  - **`SECURITY DEFINER` functions bypass RLS.** A `SECURITY DEFINER` function runs with its creator's privileges — typically a role with `bypassrls` (e.g., `postgres`). Never add `SECURITY DEFINER` to resolve a permission error; it silently removes access control without fixing the underlying cause. Prefer `SECURITY INVOKER`.
  - **`SECURITY DEFINER` functions in `public` are callable by all roles.** Postgres grants `EXECUTE` to `PUBLIC` by default for every new function, so any `SECURITY DEFINER` function in `public` is a public API endpoint callable by `anon` and `authenticated` (which inherit from `PUBLIC`) without any additional grant. When `SECURITY DEFINER` is genuinely needed (e.g., bypassing RLS on an internal lookup table), keep the function in a non-exposed schema, always include an `auth.uid()` check in the function body, and run `supabase db advisors` after making changes.

- **Storage access control**
  - **Storage upsert requires INSERT + SELECT + UPDATE.** Granting only INSERT allows new uploads but file replacement (upsert) silently fails. You need all three.

- **Dependency and supply-chain security**
  - **Always pin package versions and commit lockfiles** when installing Supabase packages (`supabase-js`, `@supabase/ssr`, `supabase-py`, etc.). See the npm security guide for the full checklist.

For any security concern not covered above, fetch the Supabase product security index: `[external address omitted in offline package]`

## Supabase CLI

Always discover commands via `--help` — never guess. The CLI structure changes between versions.

```bash
supabase --help                    # All top-level commands
supabase <group> --help            # Subcommands (e.g., supabase db --help)
supabase <group> <command> --help  # Flags for a specific command
```

**Supabase CLI Known gotchas:**

- `supabase db query` requires **CLI v2.79.0+** → use MCP `execute_sql` or `psql` as fallback
- `supabase db advisors` requires **CLI v2.81.3+** → use MCP `get_advisors` as fallback
- The browser flow of `supabase login` creates a classic token with full account access. In CI, set `SUPABASE_ACCESS_TOKEN` to a scoped personal access token instead. It takes precedence over any saved login. Commands that connect with the database password (`--password` or `SUPABASE_DB_PASSWORD`, for example `supabase db push`) aren't limited by the token's permissions.
- In imperative migration projects, create new hand-authored migration files with `supabase migration new <name>` first. Never invent a migration filename or rely on memory for the expected format. Declarative schema projects generate migrations from `supabase/schemas/`; see "Making and Committing Schema Changes" below.

**Version check and upgrade:** Run `supabase --version` to check. For CLI changelogs and version-specific features, consult the CLI documentation or GitHub releases.

## Supabase MCP Server

For setup instructions, server URL, and configuration, see the MCP setup guide.

**Troubleshooting connection issues** — follow these steps in order:

1. **Check if the server is reachable:**
   `curl -so /dev/null -w "%{http_code}" [external address omitted in offline package]`
   A `401` is expected (no token) and means the server is up. Timeout or "connection refused" means it may be down.

2. **Check `.mcp.json` configuration:**
   Verify the project root has a valid `.mcp.json` with the correct server URL. If missing, create one pointing to `[external address omitted in offline package]`.

3. **Authenticate the MCP server:**
   If the server is reachable and `.mcp.json` is correct but tools aren't visible, the user needs to authenticate. The Supabase MCP server uses OAuth 2.1 — tell the user to trigger the auth flow in their agent, complete it in the browser, and reload the session.
   In CI or other environments where the browser flow can't run, pass a scoped personal access token in the `Authorization: Bearer` header instead.

4. **Check scoped token permissions:**
   If a tool fails with "You do not have permission to perform this action" while using a scoped personal access token, the token lacks that tool's permission or the project is outside the token's scope. Check the tool's required permission in the personal access tokens guide.

## Supabase Documentation

Before implementing any Supabase feature, find the relevant documentation. Use these methods in priority order:

1. **MCP `search_docs` tool** (preferred — returns relevant snippets directly)
2. **Fetch docs pages as markdown** — any docs page can be fetched by appending `.md` to the URL path.
3. **Web search** for Supabase-specific topics when you don't know which page to look at.

## Making and Committing Schema Changes

First decide which schema workflow the project uses.

### Option A: Declarative schemas

Use this when `supabase/schemas/` exists or `config.toml` sets `schema_paths`. Edit the desired schema state in those files, then generate and review the migration. Do not start by hand-writing a migration. See the Declarative database schemas guide.

### Option B: Imperative migrations

Use this when the project does not use declarative schemas.

**To make schema changes, use `execute_sql` (MCP) or `supabase db query` (CLI).** These run SQL directly on the database without creating migration history entries, so you can iterate freely and generate a clean migration when ready.

Do NOT use `apply_migration` to change a local database schema — it writes a migration history entry on every call, which means you can't iterate, and `supabase db diff` / `supabase db pull` will produce empty or conflicting diffs. If you use it, you'll be stuck with whatever SQL you passed on the first try.

**When ready to commit** your changes to a migration file:

1. **Run advisors** → `supabase db advisors` (CLI v2.81.3+) or MCP `get_advisors`. Fix any issues.
2. **Review the Security Checklist above** if your changes involve views, functions, triggers, or storage.
3. **Generate the migration** → `supabase db pull <descriptive-name> --local --yes`
4. **Verify** → `supabase migration list --local`

## Debugging

When you get an error on a Supabase-related request, for example an error code from the Supabase REST API, Postgres database, or PostgREST, an empty result, getting blocked by RLS unexpectedly, or an error from a Supabase service like Auth, Realtime, Edge Functions, or Storage, you **must** fetch Supabase's Monitoring and Debugging documentation before diagnosing or proposing a fix, rather than working from memory. The same docs also cover performance optimizations, such as slow queries and missing indexes.

## Reference Guides

- **Skill Feedback** → [references/skill-feedback.md](references/skill-feedback.md)
  **MUST read when** the user reports that this skill gave incorrect guidance or is missing information.



---

## Reviewed skill instruction: `.agents/skills/supabase-postgres-best-practices/SKILL.md`

---
name: supabase-postgres-best-practices
description: "Postgres best practices maintained by Supabase, for Postgres running anywhere. Load this skill BEFORE writing or changing anything that lives in a Postgres database: creating or altering tables and columns (including choosing column types), schema design, migrations and declarative schema files, RLS policies and the tests that verify them, indexes, triggers, database functions, queues and scheduled jobs (pg_cron, pgmq), vector/semantic search (pgvector), and restoring dumps (pg_restore) or importing data. Also load it when diagnosing slow queries, high CPU, timeouts, EXPLAIN plans, connection exhaustion, locking, bloat, or rows visible to the wrong user or tenant. This is not just a performance guide — schema, migration, security, and SQL authoring tasks need these rules too, even for a one-column change or a single query."
license: MIT
metadata:
  author: supabase
  version: "1.1.1"
  organization: Supabase
  date: January 2026
  abstract: Comprehensive Postgres performance optimization guide for developers using Supabase and Postgres. Contains performance rules across 8 categories, prioritized by impact from critical (query performance, connection management) to incremental (advanced features). Each rule includes detailed explanations, incorrect vs. correct SQL examples, query plan analysis, and specific performance metrics to guide automated optimization and code generation.
---

# Supabase Postgres Best Practices

Comprehensive performance optimization guide for Postgres, maintained by Supabase. Contains rules across 8 categories, prioritized by impact to guide automated query optimization and schema design.

## When to Apply

Reference these guidelines when:
- Writing SQL queries or designing schemas
- Implementing indexes or query optimization
- Reviewing database performance issues
- Configuring connection pooling or scaling
- Optimizing for Postgres-specific features
- Working with Row-Level Security (RLS)

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Query Performance | CRITICAL | `query-` |
| 2 | Connection Management | CRITICAL | `conn-` |
| 3 | Security & RLS | CRITICAL | `security-` |
| 4 | Schema Design | HIGH | `schema-` |
| 5 | Concurrency & Locking | MEDIUM-HIGH | `lock-` |
| 6 | Data Access Patterns | MEDIUM | `data-` |
| 7 | Monitoring & Diagnostics | LOW-MEDIUM | `monitor-` |
| 8 | Advanced Features | LOW | `advanced-` |

## How to Use

Read individual rule files for detailed explanations and SQL examples:

```
references/query-missing-indexes.md
references/query-partial-indexes.md
references/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect SQL example with explanation
- Correct SQL example with explanation
- Optional EXPLAIN output or metrics
- Additional context and references
- Supabase-specific notes (when applicable)

## References

- [external address omitted in offline package]
- [external address omitted in offline package]
- [external address omitted in offline package]
- [external address omitted in offline package]
- [external address omitted in offline package]



---

## Reviewed skill instruction: `.agents/skills/vercel-composition-patterns/SKILL.md`

---
name: vercel-composition-patterns
description:
  React composition patterns that scale. Use when refactoring components with
  boolean prop proliferation, building flexible component libraries, or
  designing reusable APIs. Triggers on tasks involving compound components,
  render props, context providers, or component architecture. Includes React 19
  API changes.
license: MIT
metadata:
  author: vercel
  version: '1.0.0'
---

# React Composition Patterns

Composition patterns for building flexible, maintainable React components. Avoid
boolean prop proliferation by using compound components, lifting state, and
composing internals. These patterns make codebases easier for both humans and AI
agents to work with as they scale.

## When to Apply

Reference these guidelines when:

- Refactoring components with many boolean props
- Building reusable component libraries
- Designing flexible component APIs
- Reviewing component architecture
- Working with compound components or context providers

## Rule Categories by Priority

| Priority | Category                | Impact | Prefix          |
| -------- | ----------------------- | ------ | --------------- |
| 1        | Component Architecture  | HIGH   | `architecture-` |
| 2        | State Management        | MEDIUM | `state-`        |
| 3        | Implementation Patterns | MEDIUM | `patterns-`     |
| 4        | React 19 APIs           | MEDIUM | `react19-`      |

## Quick Reference

### 1. Component Architecture (HIGH)

- `architecture-avoid-boolean-props` - Don't add boolean props to customize
  behavior; use composition
- `architecture-compound-components` - Structure complex components with shared
  context

### 2. State Management (MEDIUM)

- `state-decouple-implementation` - Provider is the only place that knows how
  state is managed
- `state-context-interface` - Define generic interface with state, actions, meta
  for dependency injection
- `state-lift-state` - Move state into provider components for sibling access

### 3. Implementation Patterns (MEDIUM)

- `patterns-explicit-variants` - Create explicit variant components instead of
  boolean modes
- `patterns-children-over-render-props` - Use children for composition instead
  of renderX props

### 4. React 19 APIs (MEDIUM)

> **⚠️ React 19+ only.** Skip this section if using React 18 or earlier.

- `react19-no-forwardref` - Don't use `forwardRef`; use `use()` instead of `useContext()`

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/architecture-avoid-boolean-props.md
rules/state-context-interface.md
```

Each rule file contains:

- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`



---

## Reviewed skill instruction: `.agents/skills/vercel-react-best-practices/SKILL.md`

---
name: vercel-react-best-practices
description: React and Next.js performance optimization guidelines from Vercel Engineering. This skill should be used when writing, reviewing, or refactoring React/Next.js code to ensure optimal performance patterns. Triggers on tasks involving React components, Next.js pages, data fetching, bundle optimization, or performance improvements.
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel React Best Practices

Comprehensive performance optimization guide for React and Next.js applications, maintained by Vercel. Contains 70 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new React components or Next.js pages
- Implementing data fetching (client or server-side)
- Reviewing code for performance issues
- Refactoring existing React/Next.js code
- Optimizing bundle size or load times

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Eliminating Waterfalls | CRITICAL | `async-` |
| 2 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 3 | Server-Side Performance | HIGH | `server-` |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` |
| 5 | Re-render Optimization | MEDIUM | `rerender-` |
| 6 | Rendering Performance | MEDIUM | `rendering-` |
| 7 | JavaScript Performance | LOW-MEDIUM | `js-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

## Quick Reference

### 1. Eliminating Waterfalls (CRITICAL)

- `async-cheap-condition-before-await` - Check cheap sync conditions before awaiting flags or remote values
- `async-defer-await` - Move await into branches where actually used
- `async-parallel` - Use Promise.all() for independent operations
- `async-dependencies` - Use better-all for partial dependencies
- `async-api-routes` - Start promises early, await late in API routes
- `async-suspense-boundaries` - Use Suspense to stream content

### 2. Bundle Size Optimization (CRITICAL)

- `bundle-barrel-imports` - Import directly, avoid barrel files
- `bundle-analyzable-paths` - Prefer statically analyzable import and file-system paths to avoid broad bundles and traces
- `bundle-dynamic-imports` - Use next/dynamic for heavy components
- `bundle-defer-third-party` - Load analytics/logging after hydration
- `bundle-conditional` - Load modules only when feature is activated
- `bundle-preload` - Preload on hover/focus for perceived speed

### 3. Server-Side Performance (HIGH)

- `server-auth-actions` - Authenticate server actions like API routes
- `server-cache-react` - Use React.cache() for per-request deduplication
- `server-cache-lru` - Use LRU cache for cross-request caching
- `server-dedup-props` - Avoid duplicate serialization in RSC props
- `server-hoist-static-io` - Hoist static I/O (fonts, logos) to module level
- `server-no-shared-module-state` - Avoid module-level mutable request state in RSC/SSR
- `server-serialization` - Minimize data passed to client components
- `server-parallel-fetching` - Restructure components to parallelize fetches
- `server-parallel-nested-fetching` - Chain nested fetches per item in Promise.all
- `server-after-nonblocking` - Use after() for non-blocking operations

### 4. Client-Side Data Fetching (MEDIUM-HIGH)

- `client-swr-dedup` - Use SWR for automatic request deduplication
- `client-event-listeners` - Deduplicate global event listeners
- `client-passive-event-listeners` - Use passive listeners for scroll
- `client-localstorage-schema` - Version and minimize localStorage data

### 5. Re-render Optimization (MEDIUM)

- `rerender-defer-reads` - Don't subscribe to state only used in callbacks
- `rerender-memo` - Extract expensive work into memoized components
- `rerender-memo-with-default-value` - Hoist default non-primitive props
- `rerender-dependencies` - Use primitive dependencies in effects
- `rerender-derived-state` - Subscribe to derived booleans, not raw values
- `rerender-derived-state-no-effect` - Derive state during render, not effects
- `rerender-functional-setstate` - Use functional setState for stable callbacks
- `rerender-lazy-state-init` - Pass function to useState for expensive values
- `rerender-simple-expression-in-memo` - Avoid memo for simple primitives
- `rerender-split-combined-hooks` - Split hooks with independent dependencies
- `rerender-move-effect-to-event` - Put interaction logic in event handlers
- `rerender-transitions` - Use startTransition for non-urgent updates
- `rerender-use-deferred-value` - Defer expensive renders to keep input responsive
- `rerender-use-ref-transient-values` - Use refs for transient frequent values
- `rerender-no-inline-components` - Don't define components inside components

### 6. Rendering Performance (MEDIUM)

- `rendering-animate-svg-wrapper` - Animate div wrapper, not SVG element
- `rendering-content-visibility` - Use content-visibility for long lists
- `rendering-hoist-jsx` - Extract static JSX outside components
- `rendering-svg-precision` - Reduce SVG coordinate precision
- `rendering-hydration-no-flicker` - Use inline script for client-only data
- `rendering-hydration-suppress-warning` - Suppress expected mismatches
- `rendering-activity` - Use Activity component for show/hide
- `rendering-conditional-render` - Use ternary, not && for conditionals
- `rendering-usetransition-loading` - Prefer useTransition for loading state
- `rendering-resource-hints` - Use React DOM resource hints for preloading
- `rendering-script-defer-async` - Use defer or async on script tags

### 7. JavaScript Performance (LOW-MEDIUM)

- `js-batch-dom-css` - Group CSS changes via classes or cssText
- `js-index-maps` - Build Map for repeated lookups
- `js-cache-property-access` - Cache object properties in loops
- `js-cache-function-results` - Cache function results in module-level Map
- `js-cache-storage` - Cache localStorage/sessionStorage reads
- `js-combine-iterations` - Combine multiple filter/map into one loop
- `js-length-check-first` - Check array length before expensive comparison
- `js-early-exit` - Return early from functions
- `js-hoist-regexp` - Hoist RegExp creation outside loops
- `js-min-max-loop` - Use loop for min/max instead of sort
- `js-set-map-lookups` - Use Set/Map for O(1) lookups
- `js-tosorted-immutable` - Use toSorted() for immutability
- `js-flatmap-filter` - Use flatMap to map and filter in one pass
- `js-request-idle-callback` - Defer non-critical work to browser idle time

### 8. Advanced Patterns (LOW)

- `advanced-effect-event-deps` - Don't put `useEffectEvent` results in effect deps
- `advanced-event-handler-refs` - Store event handlers in refs
- `advanced-init-once` - Initialize app once per app load
- `advanced-use-latest` - useLatest for stable callback refs

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`



---

## Reviewed skill instruction: `.agents/skills/webapp-testing/SKILL.md`

---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
license: Complete terms in LICENSE.txt
---

# Web Application Testing

To test local web applications, write native Python Playwright scripts.

**Helper Scripts Available**:
- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

**Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first and find that a customized solution is abslutely necessary. These scripts can be very large and thus pollute your context window. They exist to be called directly as black-box scripts rather than ingested into your context window.

## Decision Tree: Choosing Your Approach

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Example: Using with_server.py

To start a server, run `--help` first, then use the helper:

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers (e.g., backend + frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

To create an automation script, include only Playwright logic (servers are managed automatically):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('[external address omitted in offline package]) # Server already running and ready
    page.wait_for_load_state('networkidle') # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **Identify selectors** from inspection results

3. **Execute actions** using discovered selectors

## Common Pitfall

❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

## Best Practices

- **Use bundled scripts as black boxes** - To accomplish a task, consider whether one of the scripts available in `scripts/` can help. These scripts handle common, complex workflows reliably without cluttering the context window. Use `--help` to see usage, then invoke directly. 
- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`

## Reference Files

- **examples/** - Examples showing common patterns:
  - `element_discovery.py` - Discovering buttons, links, and inputs on a page
  - `static_html_automation.py` - Using file:// URLs for local HTML
  - `console_logging.py` - Capturing console logs during automation


---

# Exact current files — production-auth milestone

These are verbatim snapshots from the implementation after Milestone 1. Paths are repository-relative. Ox Alpha can copy or compare them directly. The test file is included in full so its fixtures, imports, and auth tests are visible.


---

## `backend/app/core/auth.py`

````python
from functools import lru_cache
from typing import Annotated, Any

import httpx
import jwt
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import Settings, get_settings
from app.core.errors import AppError

bearer = HTTPBearer(auto_error=False)


@lru_cache(maxsize=16)
def _jwks_url(supabase_url: str) -> str:
    return f"{supabase_url.rstrip('/')}/auth/v1/.well-known/jwks.json"


async def _verify_supabase_token(token: str, settings: Settings) -> dict[str, Any]:
    if settings.supabase_jwt_secret:
        try:
            return jwt.decode(
                token, settings.supabase_jwt_secret, algorithms=["HS256"], audience="authenticated"
            )
        except jwt.PyJWTError as exc:
            raise AppError("invalid_token", "The bearer token is invalid", 401) from exc

    if not settings.supabase_url:
        raise AppError("auth_unavailable", "Supabase authentication is not configured", 503)
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(_jwks_url(settings.supabase_url))
            response.raise_for_status()
            keys = response.json().get("keys", [])
        header = jwt.get_unverified_header(token)
        matching = next((key for key in keys if key.get("kid") == header.get("kid")), None)
        if matching is None:
            raise AppError("invalid_token", "The bearer token signing key is unknown", 401)
        algorithms = {"EC": "ES256", "RSA": "RS256", "OKP": "EdDSA"}
        expected_algorithm = matching.get("alg") or algorithms.get(matching.get("kty"))
        if not expected_algorithm or header.get("alg") != expected_algorithm:
            raise AppError("invalid_token", "The bearer token algorithm is not allowed", 401)
        signing_key = jwt.PyJWK.from_dict(matching).key
        return jwt.decode(
            token, signing_key, algorithms=[expected_algorithm], audience="authenticated"
        )
    except AppError:
        raise
    except (httpx.HTTPError, ValueError, jwt.PyJWTError) as exc:
        raise AppError("invalid_token", "The bearer token could not be verified", 401) from exc


async def get_current_user(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> dict[str, str]:
    if credentials is None:
        if settings.dev_auth_allowed:
            request.state.auth_mode = "dev-user (LOCAL/TEST ONLY)"
            return {"id": "dev-user", "email": "dev-user@local.invalid"}
        if settings.is_production and not settings.supabase_configured:
            raise AppError(
                "auth_unavailable",
                "Supabase authentication must be configured in production",
                503,
            )
        raise AppError("unauthorized", "A bearer token is required", 401)
    claims = await _verify_supabase_token(credentials.credentials, settings)
    subject = claims.get("sub")
    if not isinstance(subject, str) or not subject:
        raise AppError("invalid_token", "The bearer token has no user subject", 401)
    return {"id": subject, "email": str(claims.get("email", ""))}
````


---

## `backend/app/core/config.py`

````python
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    app_name: str = "MAYA AI"
    environment: str = "development"
    database_url: str = "sqlite+aiosqlite:///./maya.db"
    supabase_url: str | None = None
    supabase_service_role_key: str | None = None
    supabase_jwt_secret: str | None = None
    supabase_storage_bucket: str = "maya-assets"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.8-flash"
    comfyui_base_url: str | None = None
    comfyui_api_token: str | None = None
    hf_token: str | None = None
    dev_auth_enabled: bool = True
    upload_dir: str = "./uploads"
    max_upload_bytes: int = 20_000_000
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def supabase_configured(self) -> bool:
        return bool(self.supabase_url and self.supabase_url.strip())

    @property
    def is_production(self) -> bool:
        return self.environment.strip().casefold() == "production"

    @property
    def dev_auth_allowed(self) -> bool:
        return self.dev_auth_enabled and not self.is_production and not self.supabase_configured


@lru_cache
def get_settings() -> Settings:
    return Settings()
````


---

## `backend/app/main.py`

````python
import logging
import secrets
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import api_router
from app.core.config import Settings, get_settings
from app.core.db import make_session_factory
from app.core.errors import AppError
from app.models import Base

logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved = settings or get_settings()
    if resolved.is_production and not resolved.supabase_configured:
        raise ValueError("Supabase authentication must be configured when ENVIRONMENT=production")
    engine, session_factory = make_session_factory(resolved.database_url)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.engine = engine
        app.state.session_factory = session_factory
        app.state.upload_signing_key = secrets.token_bytes(32)
        if resolved.database_url.startswith("sqlite") and resolved.environment != "production":
            async with engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)
        yield
        await engine.dispose()

    app = FastAPI(title="MAYA AI API", version="1.0.0", lifespan=lifespan)
    app.dependency_overrides[get_settings] = lambda: resolved
    app.state.engine = engine
    app.state.session_factory = session_factory
    app.state.upload_signing_key = secrets.token_bytes(32)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved.cors_origin_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "Idempotency-Key", "x-maya-upload-token"],
    )

    @app.middleware("http")
    async def request_id_middleware(request: Request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        return response

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
                "request_id": getattr(request.state, "request_id", "unknown"),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        safe_details = [
            {"loc": item.get("loc"), "msg": item.get("msg"), "type": item.get("type")}
            for item in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content={
                "code": "validation_error",
                "message": "Request validation failed",
                "details": safe_details,
                "request_id": getattr(request.state, "request_id", "unknown"),
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_error_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": "http_error",
                "message": str(exc.detail),
                "details": None,
                "request_id": getattr(request.state, "request_id", "unknown"),
            },
            headers=exc.headers,
        )

    @app.exception_handler(Exception)
    async def unexpected_error_handler(request: Request, exc: Exception):
        logger.error(
            "Unhandled API error request_id=%s error_type=%s",
            getattr(request.state, "request_id", "unknown"),
            type(exc).__name__,
        )
        return JSONResponse(
            status_code=500,
            content={
                "code": "internal_error",
                "message": "An unexpected error occurred",
                "details": None,
                "request_id": getattr(request.state, "request_id", "unknown"),
            },
        )

    @app.get("/healthz", tags=["health"])
    async def healthz():
        return {
            "status": "ok",
            "auth_mode": (
                "supabase"
                if resolved.supabase_configured
                else "dev-user (LOCAL/TEST ONLY)"
                if resolved.dev_auth_allowed
                else "disabled"
            ),
        }

    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
````


---

## `backend/tests/test_api.py`

````python
import asyncio
import base64
import json
from datetime import UTC, datetime, timedelta
from uuid import UUID

import httpx
import jwt
import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.core.errors import AppError
from app.main import create_app
from app.models import Result


class FakeAsyncClient:
    def __init__(self, *args, get_response=None, post_response=None, **kwargs):
        self.get_response = get_response
        self.post_response = post_response

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return None

    async def get(self, url, **kwargs):
        if callable(self.get_response):
            return self.get_response(url, **kwargs)
        return self.get_response

    async def post(self, url, **kwargs):
        if callable(self.post_response):
            return self.post_response(url, **kwargs)
        return self.post_response


def client_for(tmp_path, **overrides):
    options = {
        "database_url": f"sqlite+aiosqlite:///{tmp_path / 'test.db'}",
        "upload_dir": str(tmp_path / "uploads"),
        "environment": "test",
        **overrides,
    }
    settings = Settings(**options)
    return TestClient(create_app(settings))


def create_project(client: TestClient) -> str:
    response = client.post("/api/v1/projects", json={"name": "Reading nook"})
    assert response.status_code == 201
    return response.json()["id"]


def test_health_and_dev_auth_mode(tmp_path):
    with client_for(tmp_path) as client:
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json()["auth_mode"].startswith("dev-user")
        assert client.get("/api/v1/projects").json() == []


def test_auth_fails_closed_when_supabase_is_configured(tmp_path):
    with client_for(
        tmp_path, supabase_url="https://project.supabase.co", dev_auth_enabled=False
    ) as client:
        response = client.get("/api/v1/projects")
        assert response.status_code == 401
        assert response.json()["code"] == "unauthorized"


def test_production_startup_requires_supabase_auth_even_if_dev_auth_enabled(tmp_path):
    settings = Settings(
        database_url=f"sqlite+aiosqlite:///{tmp_path / 'production.db'}",
        environment="production",
        dev_auth_enabled=True,
    )

    with pytest.raises(ValueError, match="Supabase authentication must be configured"):
        create_app(settings)


def test_production_never_falls_back_to_dev_user(tmp_path):
    with client_for(
        tmp_path,
        environment="production",
        supabase_url="https://project.supabase.co",
        dev_auth_enabled=True,
    ) as client:
        response = client.get("/api/v1/projects")
        assert response.status_code == 401
        assert response.json()["code"] == "unauthorized"
        assert client.get("/healthz").json()["auth_mode"] == "supabase"


def test_dev_auth_can_be_disabled_outside_production(tmp_path):
    with client_for(tmp_path, environment="test", dev_auth_enabled=False) as client:
        response = client.get("/api/v1/projects")
        assert response.status_code == 401
        assert response.json()["code"] == "unauthorized"
        assert client.get("/healthz").json()["auth_mode"] == "disabled"


def test_error_envelope_has_request_id(tmp_path):
    with client_for(tmp_path) as client:
        response = client.post("/api/v1/projects", json={})
        body = response.json()
        assert response.status_code == 422
        assert body["code"] == "validation_error"
        assert body["request_id"] == response.headers["x-request-id"]
        assert body["details"]


def test_idempotency_replay_and_payload_conflict(tmp_path):
    with client_for(tmp_path) as client:
        project_id = create_project(client)
        headers = {"Idempotency-Key": "brief-run-001"}
        payload = {"project_id": project_id, "brief": {"style": "Japandi"}}
        first = client.post("/api/v1/jobs", json=payload, headers=headers)
        replay = client.post("/api/v1/jobs", json=payload, headers=headers)
        conflict = client.post(
            "/api/v1/jobs", json={**payload, "brief": {"style": "Industrial"}}, headers=headers
        )
        assert first.status_code == 202
        assert replay.status_code == 202
        assert first.json()["id"] == replay.json()["id"]
        assert conflict.status_code == 409
        assert conflict.json()["code"] == "idempotency_conflict"


def test_cancel_sets_flag_without_unbounded_status_transition(tmp_path):
    with client_for(tmp_path) as client:
        project_id = create_project(client)
        created = client.post(
            "/api/v1/jobs",
            json={"project_id": project_id, "brief": {}},
            headers={"Idempotency-Key": "cancel-1"},
        ).json()
        response = client.post(f"/api/v1/jobs/{created['id']}/cancel")
        assert response.status_code == 200
        assert response.json()["cancellation_requested"] is True
        assert response.json()["status"] == "queued"


def test_room_brief_chat_plan_and_results_access(tmp_path):
    with client_for(tmp_path) as client:
        project_id = create_project(client)
        room = client.post(f"/api/v1/projects/{project_id}/rooms", json={"name": "Living room"})
        assert room.status_code == 201
        brief = client.post(
            f"/api/v1/projects/{project_id}/briefs",
            json={"room_id": room.json()["id"], "content": {"style": "Soft modern"}},
        )
        assert brief.status_code == 201
        assert brief.json()["version"] == 1
        plan = client.post(
            "/api/v1/chat",
            json={
                "project_id": project_id,
                "brief": {"style": "Soft modern"},
                "message": "Suggest a direction",
            },
        )
        assert plan.status_code == 200
        assert plan.json()["provider"] == "mock"
        assert plan.json()["plan"]["style"] == "Soft modern"
        assert plan.json()["plan"]["palette"][0]["hex"].startswith("#")
        assert client.get(f"/api/v1/projects/{project_id}/results").json() == []


def test_signed_local_upload_is_scoped_and_validates_signature(tmp_path):
    png = bytes.fromhex("89504e470d0a1a0a00000000") + b"test-image-data"
    with client_for(tmp_path) as client:
        project_id = create_project(client)
        room_id = client.post(
            f"/api/v1/projects/{project_id}/rooms", json={"name": "Office"}
        ).json()["id"]
        signed = client.post(
            f"/api/v1/projects/{project_id}/assets/upload-url",
            json={
                "room_id": room_id,
                "filename": "room.png",
                "mime_type": "image/png",
                "size_bytes": len(png),
            },
        )
        assert signed.status_code == 201
        upload = signed.json()
        headers = {**upload["headers"], "x-maya-upload-token": "0" * 64}
        bad = client.put(upload["upload_url"], content=png, headers=headers)
        assert bad.status_code == 403
        headers["x-maya-upload-token"] = upload["headers"]["x-maya-upload-token"]
        good = client.put(upload["upload_url"], content=png, headers=headers)
        assert good.status_code == 204


def test_mock_chat_provider_returns_schema_valid_plan(tmp_path):
    import asyncio

    from app.providers.chat.mock import MockChatProvider

    plan = asyncio.run(MockChatProvider().plan({"style": "Coastal"}))
    assert plan.style == "Coastal"
    assert len(plan.palette) == 3
    assert plan.model_dump()["scene_beats"]


def test_comfyui_provider_reports_degraded_state(tmp_path):
    import asyncio

    import pytest

    from app.core.errors import ProviderUnavailable
    from app.providers.media.comfyui import ComfyUIProvider

    with pytest.raises(ProviderUnavailable):
        asyncio.run(ComfyUIProvider(None).generate({"id": "mock"}))


def test_job_list_is_project_scoped(tmp_path):
    with client_for(tmp_path) as client:
        project_id = create_project(client)
        client.post(
            "/api/v1/jobs",
            json={"project_id": project_id, "brief": {"style": "Natural"}},
            headers={"Idempotency-Key": "list-1"},
        )
        listed = client.get(f"/api/v1/jobs?project_id={project_id}")
        assert listed.status_code == 200
        assert len(listed.json()) == 1


def test_projects_crud_and_membership_boundary(tmp_path):
    with client_for(tmp_path) as client:
        project_id = create_project(client)
        assert len(client.get("/api/v1/projects").json()) == 1
        assert client.get(f"/api/v1/projects/{project_id}").json()["name"] == "Reading nook"
        updated = client.patch(
            f"/api/v1/projects/{project_id}", json={"name": "Quiet reading room"}
        )
        assert updated.status_code == 200
        assert updated.json()["name"] == "Quiet reading room"

        from app.core.auth import get_current_user

        client.app.dependency_overrides[get_current_user] = lambda: {
            "id": "other-user",
            "email": "",
        }
        assert client.get(f"/api/v1/projects/{project_id}").status_code == 404
        client.app.dependency_overrides[get_current_user] = lambda: {"id": "dev-user", "email": ""}
        assert client.delete(f"/api/v1/projects/{project_id}").status_code == 204
        assert client.get(f"/api/v1/projects/{project_id}").status_code == 404


def test_brief_versions_and_room_validation(tmp_path):
    with client_for(tmp_path) as client:
        project_id = create_project(client)
        first = client.post(
            f"/api/v1/projects/{project_id}/briefs", json={"content": {"style": "Coastal"}}
        )
        second = client.post(
            f"/api/v1/projects/{project_id}/briefs", json={"content": {"style": "Modern"}}
        )
        assert first.json()["version"] == 1
        assert second.json()["version"] == 2
        assert len(client.get(f"/api/v1/projects/{project_id}/briefs").json()) == 2
        invalid_room = client.post(
            f"/api/v1/projects/{project_id}/briefs",
            json={"room_id": "00000000-0000-0000-0000-000000000001", "content": {}},
        )
        assert invalid_room.status_code == 404
        assert client.get(f"/api/v1/projects/{project_id}/rooms").json() == []


def test_job_status_not_found_and_invalid_room(tmp_path):
    with client_for(tmp_path) as client:
        project_id = create_project(client)
        invalid = client.post(
            "/api/v1/jobs",
            json={
                "project_id": project_id,
                "room_id": "00000000-0000-0000-0000-000000000001",
                "brief": {},
            },
            headers={"Idempotency-Key": "bad-room"},
        )
        assert invalid.status_code == 404
        missing = client.get("/api/v1/jobs/00000000-0000-0000-0000-000000000001")
        assert missing.status_code == 404
        created = client.post(
            "/api/v1/jobs",
            json={"project_id": project_id, "brief": {}},
            headers={"Idempotency-Key": "job-status"},
        ).json()
        assert client.get(f"/api/v1/jobs/{created['id']}").json()["status"] == "queued"


def test_result_list_select_and_unselect(tmp_path):
    with client_for(tmp_path) as client:
        project_id = create_project(client)
        job = client.post(
            "/api/v1/jobs",
            json={"project_id": project_id, "brief": {}},
            headers={"Idempotency-Key": "result-1"},
        ).json()

        async def insert_result() -> str:
            async with client.app.state.session_factory() as session:
                row = Result(
                    job_id=UUID(job["id"]),
                    prompt_version="design_plan_v1",
                    prompt_hash="0" * 64,
                    output_json={
                        "plan": {"style": "Warm modern"},
                        "media": {"kind": "placeholder_metadata"},
                    },
                )
                session.add(row)
                await session.commit()
                return str(row.id)

        result_id = asyncio.run(insert_result())
        assert len(client.get(f"/api/v1/projects/{project_id}/results").json()) == 1
        selected = client.post(f"/api/v1/results/{result_id}/select", json={"selected": True})
        assert selected.status_code == 200
        assert selected.json()["selected_by"] == "dev-user"
        unselected = client.post(f"/api/v1/results/{result_id}/select", json={"selected": False})
        assert unselected.json()["selected_by"] is None
        assert (
            client.post(
                "/api/v1/results/00000000-0000-0000-0000-000000000001/select", json={}
            ).status_code
            == 404
        )


def test_auth_hs256_and_jwks_validation(monkeypatch):
    from app.core.auth import _verify_supabase_token

    secret = "local-test-jwt-secret"
    claims = {
        "sub": "user-123",
        "aud": "authenticated",
        "exp": datetime.now(UTC) + timedelta(minutes=5),
    }
    hs_token = jwt.encode(claims, secret, algorithm="HS256")
    settings = Settings(supabase_url="https://project.supabase.co", supabase_jwt_secret=secret)
    assert asyncio.run(_verify_supabase_token(hs_token, settings))["sub"] == "user-123"
    with pytest.raises(AppError):
        asyncio.run(_verify_supabase_token("not.a.jwt", settings))

    jwks_secret = b"mock-jwks-secret"
    jwks_token = jwt.encode(claims, jwks_secret, algorithm="HS256", headers={"kid": "mock-key"})
    jwk = {
        "kty": "oct",
        "alg": "HS256",
        "use": "sig",
        "kid": "mock-key",
        "k": base64.urlsafe_b64encode(jwks_secret).decode().rstrip("="),
    }

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kwargs: FakeAsyncClient(
            get_response=lambda url, **_kwargs: httpx.Response(
                200, json={"keys": [jwk]}, request=httpx.Request("GET", url)
            )
        ),
    )
    jwks_settings = Settings(supabase_url="https://project.supabase.co")
    assert asyncio.run(_verify_supabase_token(jwks_token, jwks_settings))["sub"] == "user-123"


def test_auth_rejects_unknown_jwks_key(monkeypatch):
    from app.core.auth import _verify_supabase_token

    token = jwt.encode(
        {"sub": "user", "aud": "authenticated"},
        "secret",
        algorithm="HS256",
        headers={"kid": "missing"},
    )

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kwargs: FakeAsyncClient(
            get_response=lambda url, **_kwargs: httpx.Response(
                200, json={"keys": []}, request=httpx.Request("GET", url)
            )
        ),
    )
    with pytest.raises(AppError) as error:
        asyncio.run(
            _verify_supabase_token(token, Settings(supabase_url="https://project.supabase.co"))
        )
    assert error.value.status_code == 401


def test_gemini_provider_validates_response_and_handles_invalid_json(monkeypatch):
    from app.providers.chat.gemini import GeminiChatProvider

    plan = {
        "style": "Soft modern",
        "palette": [
            {"name": "Linen", "hex": "#E9E2D5", "role": "walls"},
            {"name": "Oak", "hex": "#A9784F", "role": "warm accent"},
            {"name": "Sage", "hex": "#879184", "role": "soft contrast"},
        ],
        "camera_moves": ["wide reveal"],
        "scene_beats": ["reveal the room", "show the palette", "close on material details"],
        "narration": "A calm concept.",
        "constraints": ["Visualisation only."],
    }

    def valid_post(url, **kwargs):
        assert "secret-key" not in url
        assert kwargs["headers"]["x-goog-api-key"] == "secret-key"
        response_format = kwargs["json"]["generationConfig"]["responseFormat"]["text"]
        assert response_format["mimeType"] == "application/json"
        assert response_format["schema"]["properties"]["palette"]["minItems"] == 3
        prompt = kwargs["json"]["contents"][0]["parts"][0]["text"]
        assert '"style": "Soft modern"' in prompt
        assert "untrusted user data" in prompt
        return httpx.Response(
            200,
            json={"candidates": [{"content": {"parts": [{"text": json.dumps(plan)}]}}]},
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kwargs: FakeAsyncClient(post_response=valid_post),
    )
    provider = GeminiChatProvider("secret-key", "test-model")
    assert asyncio.run(provider.plan({"style": "Soft modern"})).style == "Soft modern"

    def invalid_post(url, **kwargs):
        return httpx.Response(
            200,
            json={"candidates": [{"content": {"parts": [{"text": "{}"}]}}]},
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kwargs: FakeAsyncClient(post_response=invalid_post),
    )
    with pytest.raises(AppError):
        asyncio.run(provider.plan({}))


def test_provider_selection_and_keyless_media_metadata(tmp_path, monkeypatch):
    from app.providers.chat.gemini import GeminiChatProvider
    from app.providers.chat.mock import MockChatProvider
    from app.providers.media.comfyui import ComfyUIProvider
    from app.providers.media.mock import MockMediaProvider
    from app.services.providers import chat_provider, media_provider

    assert isinstance(chat_provider(Settings()), MockChatProvider)
    assert isinstance(chat_provider(Settings(gemini_api_key="configured")), GeminiChatProvider)
    assert isinstance(media_provider(Settings()), MockMediaProvider)
    assert isinstance(media_provider(Settings(comfyui_base_url="http://comfy")), ComfyUIProvider)
    monkeypatch.setattr("app.providers.media.mock._has_ffmpeg", lambda: False)

    class Job:
        id = "00000000-0000-0000-0000-000000000002"

    output = asyncio.run(MockMediaProvider(str(tmp_path / "media")).generate(Job()))
    assert output["kind"] == "placeholder_metadata"
    assert output["ffmpeg_available"] is False


def test_supabase_signed_upload_url_and_missing_service_key(tmp_path, monkeypatch):
    from app.core.auth import get_current_user

    settings = Settings(
        database_url=f"sqlite+aiosqlite:///{tmp_path / 'supabase-storage.db'}",
        upload_dir=str(tmp_path / "uploads"),
        environment="test",
        supabase_url="https://project.supabase.co",
        supabase_service_role_key="server-only-test",
    )
    app = create_app(settings)
    app.dependency_overrides[get_current_user] = lambda: {"id": "demo-user", "email": ""}

    def signed_upload(url, **kwargs):
        assert "server-only-test" not in url
        assert kwargs["headers"]["Authorization"] == "Bearer server-only-test"
        return httpx.Response(
            200,
            json={"url": "/object/upload/sign/maya-assets/project/file.png?token=temporary"},
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kwargs: FakeAsyncClient(post_response=signed_upload),
    )
    with TestClient(app) as client:
        project_id = client.post("/api/v1/projects", json={"name": "Private files"}).json()["id"]
        response = client.post(
            f"/api/v1/projects/{project_id}/assets/upload-url",
            json={
                "filename": "room.png",
                "mime_type": "image/png",
                "size_bytes": 99,
            },
        )
        assert response.status_code == 201
        assert response.json()["upload_url"].startswith(
            "https://project.supabase.co/storage/v1/object/upload/sign/"
        )

    settings_without_key = Settings(
        database_url=f"sqlite+aiosqlite:///{tmp_path / 'supabase-no-key.db'}",
        environment="test",
        supabase_url="https://project.supabase.co",
    )
    app_without_key = create_app(settings_without_key)
    app_without_key.dependency_overrides[get_current_user] = lambda: {
        "id": "demo-user",
        "email": "",
    }
    with TestClient(app_without_key) as client:
        project_id = client.post("/api/v1/projects", json={"name": "Private files"}).json()["id"]
        response = client.post(
            f"/api/v1/projects/{project_id}/assets/upload-url",
            json={
                "filename": "room.png",
                "mime_type": "image/png",
                "size_bytes": 99,
            },
        )
        assert response.status_code == 503


def test_upload_limits_room_scope_and_bad_image_bytes(tmp_path):
    with client_for(tmp_path, max_upload_bytes=10) as client:
        project_id = create_project(client)
        too_large = client.post(
            f"/api/v1/projects/{project_id}/assets/upload-url",
            json={
                "filename": "room.png",
                "mime_type": "image/png",
                "size_bytes": 11,
            },
        )
        assert too_large.status_code == 413
        wrong_room = client.post(
            f"/api/v1/projects/{project_id}/assets/upload-url",
            json={
                "room_id": "00000000-0000-0000-0000-000000000001",
                "filename": "room.png",
                "mime_type": "image/png",
                "size_bytes": 9,
            },
        )
        assert wrong_room.status_code == 404
        signed = client.post(
            f"/api/v1/projects/{project_id}/assets/upload-url",
            json={
                "filename": "room.png",
                "mime_type": "image/png",
                "size_bytes": 9,
            },
        ).json()
        bad_bytes = client.put(
            signed["upload_url"], content=b"not an image", headers=signed["headers"]
        )
        assert bad_bytes.status_code == 413


def test_unhandled_http_errors_keep_structured_envelope(tmp_path):
    with client_for(tmp_path) as client:
        response = client.get("/route-that-does-not-exist")
        assert response.status_code == 404
        assert response.json()["code"] == "http_error"
        assert response.json()["request_id"] == response.headers["x-request-id"]
````


---

## `.env.example`

````dotenv
# Frontend-safe publishable configuration
VITE_SUPABASE_URL=
VITE_SUPABASE_PUBLISHABLE_KEY=
VITE_API_BASE_URL=http://localhost:8000

# Local Docker Postgres only; never reuse this value in hosted environments
POSTGRES_PASSWORD=local-only

# Backend/server ONLY — never expose to browser or Git
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
SUPABASE_JWT_SECRET=
SUPABASE_STORAGE_BUCKET=maya-assets
GEMINI_API_KEY=
DATABASE_URL=sqlite+aiosqlite:///./maya.db
DEV_AUTH_ENABLED=true
# Set ENVIRONMENT=production in deployment. Production startup requires SUPABASE_URL
# and never enables the local dev-user, regardless of DEV_AUTH_ENABLED.

# Worker ONLY
COMFYUI_BASE_URL=
COMFYUI_API_TOKEN=
HF_TOKEN=

# CI / Deploy dashboard secrets only
CLOUDFLARE_API_TOKEN=
VERCEL_CRON_SECRET=
````


---

## `README.md`

````markdown
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
````


---

## Authentication milestone verification

Commands completed successfully in `backend/`:

````sh
uv sync --extra dev --locked
uv run --locked ruff check app migrations tests ../worker
uv run --locked mypy app ../worker
uv run --locked pytest tests --cov=app --cov-fail-under=80
DATABASE_URL=sqlite+aiosqlite:////tmp/maya-auth-milestone.db uv run --locked alembic upgrade head
DATABASE_URL=sqlite+aiosqlite:////tmp/maya-auth-milestone.db uv run --locked python -m app.seed
````

Results: Ruff passed; mypy passed for 35 source files; pytest passed all 26 tests at 87.33% coverage (80% minimum); migration and sample seed succeeded. No real Supabase, Gemini, GPU, or external provider calls were made. The production setting was verified with tests using an explicitly supplied Supabase URL and no network requests.
