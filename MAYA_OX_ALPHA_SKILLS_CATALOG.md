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
