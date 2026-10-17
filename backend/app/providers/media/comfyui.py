from typing import Any

from app.core.errors import ProviderUnavailable


class ComfyUIProvider:
    name = "comfyui"

    def __init__(self, base_url: str | None, api_token: str | None = None):
        self._base_url = base_url
        self._api_token = api_token

    async def generate(self, job: Any) -> dict[str, Any]:
        if not self._base_url:
            raise ProviderUnavailable("ComfyUI")
        raise ProviderUnavailable("ComfyUI adapter (workflow execution is not enabled in Phase 1)")
