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
