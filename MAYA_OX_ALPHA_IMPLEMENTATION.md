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
