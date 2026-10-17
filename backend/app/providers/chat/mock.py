from typing import Any

from app.schemas.api import DesignPlan, PaletteColor


class MockChatProvider:
    name = "mock"

    async def plan(self, brief: dict[str, Any], context: str = "") -> DesignPlan:
        style = str(brief.get("style") or "Warm contemporary").strip()[:80]
        return DesignPlan(
            style=style,
            palette=[
                PaletteColor(name="Linen", hex="#E9E2D5", role="wall and soft surfaces"),
                PaletteColor(name="Oak", hex="#A9784F", role="warm natural accent"),
                PaletteColor(name="Sage", hex="#879184", role="quiet secondary accent"),
            ],
            camera_moves=["slow wide reveal from the entry", "gentle pan across the seating zone"],
            scene_beats=[
                "show the existing room",
                "reveal the proposed palette",
                "close on material details",
            ],
            narration=(
                f"A {style.lower()} concept focused on comfort, natural texture, "
                "and clear circulation."
            ),
            constraints=[
                "Concept visualisation only; verify dimensions before purchasing or construction.",
                "No structural or code-compliance claims are made.",
            ],
        )
