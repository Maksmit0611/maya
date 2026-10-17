import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import httpx

from app.core.errors import AppError
from app.schemas.api import DesignPlan

PROMPT_MANIFEST = Path(__file__).resolve().parents[2] / "prompts" / "manifest.json"

DESIGN_PLAN_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "style": {
            "type": "string",
            "description": "Concise interior design style",
        },
        "palette": {
            "type": "array",
            "minItems": 3,
            "maxItems": 6,
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "hex": {"type": "string"},
                    "role": {"type": "string"},
                },
                "required": ["name", "hex", "role"],
                "additionalProperties": False,
            },
        },
        "camera_moves": {
            "type": "array",
            "minItems": 1,
            "maxItems": 4,
            "items": {"type": "string"},
        },
        "scene_beats": {
            "type": "array",
            "minItems": 3,
            "maxItems": 6,
            "items": {"type": "string"},
        },
        "narration": {"type": "string"},
        "constraints": {
            "type": "array",
            "minItems": 1,
            "maxItems": 8,
            "items": {"type": "string"},
        },
    },
    "required": ["style", "palette", "camera_moves", "scene_beats", "narration", "constraints"],
    "additionalProperties": False,
}


@lru_cache(maxsize=1)
def _load_design_prompt() -> str:
    manifest = json.loads(PROMPT_MANIFEST.read_text(encoding="utf-8"))
    prompt_path = PROMPT_MANIFEST.parent / manifest["design_plan_v1"]["file"]
    if not prompt_path.resolve().is_relative_to(PROMPT_MANIFEST.parent.resolve()):
        raise ValueError("Prompt manifest path must remain inside the prompts directory")
    return prompt_path.read_text(encoding="utf-8")


class GeminiChatProvider:
    name = "gemini"
    base_url = "https://generativelanguage.googleapis.com/v1beta"

    def __init__(self, api_key: str, model: str):
        self._api_key = api_key
        self._model = model

    async def plan(self, brief: dict[str, Any], context: str = "") -> DesignPlan:
        prompt = _load_design_prompt().format(
            brief=json.dumps(brief, ensure_ascii=False, sort_keys=True),
            context=json.dumps(context[:2000], ensure_ascii=False),
        )
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseFormat": {
                    "text": {
                        "mimeType": "application/json",
                        "schema": DESIGN_PLAN_SCHEMA,
                    }
                },
                "maxOutputTokens": 1600,
            },
        }
        url = f"{self.base_url}/models/{self._model}:generateContent"
        try:
            async with httpx.AsyncClient(timeout=45) as client:
                response = await client.post(
                    url, headers={"x-goog-api-key": self._api_key}, json=payload
                )
                response.raise_for_status()
            text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return DesignPlan.model_validate_json(text)
        except (httpx.HTTPError, KeyError, IndexError, ValueError) as exc:
            raise AppError(
                "chat_provider_error", "Gemini could not produce a valid design plan", 502
            ) from exc
