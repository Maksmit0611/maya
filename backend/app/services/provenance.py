import hashlib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PROMPT_PATH = (
    Path(__file__).resolve().parents[1] / "prompts" / "versions" / "v1" / "design_plan_v1.md"
)


def record_provenance(provider: str, model: str, seed: int | None = None) -> dict[str, Any]:
    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    return {
        "provider": provider,
        "model": model,
        "prompt_version": "design_plan_v1",
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "seed": seed,
        "created_at": datetime.now(UTC).isoformat(),
    }
