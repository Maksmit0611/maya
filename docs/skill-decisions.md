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
