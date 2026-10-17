# Paste This into Ox Alpha

You are implementing MAYA AI, a cloud-hosted interior-design visualisation agent for homeowners, builders, and designers.

Read these files in order:

1. `skills.sh` — run `./skills.sh` and `./skills.sh --discover`.
2. `MAYA_OX_ALPHA_IMPLEMENTATION.md` — full implementation requirements.
3. `MAYA_OX_ALPHA_SKILLS_CATALOG.md` and `MAYA_OX_ALPHA_SKILLS_CATALOG.json` — curated skills.
4. `MAYA_OX_ALPHA_SKILLS_TOOL_REGISTRY.md` and JSON — live discovery and tool governance.
5. `MAYA_FREE_STACK_AND_TOOLS.md` and JSON — free-first tools, secrets, MCPs, and phase order.

Start immediately with Phase 1. Preserve existing repository conventions. If the repository is empty, create a monorepo with React + TypeScript frontend and FastAPI Python backend.

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

Do not stop at a plan. Implement Phase 1, run tests, and report the files changed, commands run, tests passing/failing, and the exact secrets the owner must place in deployment settings.
