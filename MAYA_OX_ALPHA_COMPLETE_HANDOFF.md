# MAYA AI — complete handoff for Ox Alpha

## How to use this file

This is the single handoff file for continuing MAYA AI. Give this entire file to Ox Alpha together with access to the repository:

- Repository: https://github.com/Maksmit0611/maya
- Branch: `main`
- Handoff commit: `ea547fe8dc47e4d88c52d8dd16c5bec75a30c098`
- Latest verified CI run: https://github.com/Maksmit0611/maya/actions/runs/39009745419

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
git clone https://github.com/Maksmit0611/maya.git
cd maya
cp .env.example .env
docker compose up --build
```

Open `http://localhost:5173`. Create a project and room, upload a photo, submit a brief, request a mock plan, queue a mock job, and select the result. API health is `http://localhost:8000/healthz`; OpenAPI is `http://localhost:8000/openapi.json`. Run `./skills.sh --discover` to inspect the reviewed skill catalog. No external model, Supabase, or GPU call is required for this walkthrough.

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
  "$schema": "https://json-schema.org/draft/2020-12/schema",
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

