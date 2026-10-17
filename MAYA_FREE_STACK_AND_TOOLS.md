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
