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
