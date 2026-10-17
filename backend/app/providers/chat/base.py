from typing import Any, Protocol

from app.schemas.api import DesignPlan


class ChatProvider(Protocol):
    name: str

    async def plan(self, brief: dict[str, Any], context: str = "") -> DesignPlan: ...
