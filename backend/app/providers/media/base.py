from typing import Any, Protocol


class MediaProvider(Protocol):
    name: str

    async def generate(self, job: Any) -> dict[str, Any]: ...
