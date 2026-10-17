from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.config import Settings, get_settings
from app.core.db import get_session
from app.models import AgentMessage
from app.schemas.api import ChatRequest, ChatResponse
from app.services.access import require_project_access
from app.services.providers import chat_provider

router = APIRouter()
Session = Annotated[AsyncSession, Depends(get_session)]
User = Annotated[dict[str, str], Depends(get_current_user)]
Config = Annotated[Settings, Depends(get_settings)]


@router.post("", response_model=ChatResponse)
async def plan_design(
    payload: ChatRequest, session: Session, user: User, settings: Config
) -> ChatResponse:
    await require_project_access(session, payload.project_id, user["id"])
    provider = chat_provider(settings)
    plan = await provider.plan(payload.brief, payload.message)
    session.add_all(
        [
            AgentMessage(
                project_id=payload.project_id,
                user_id=user["id"],
                role="user",
                content=payload.message,
            ),
            AgentMessage(
                project_id=payload.project_id,
                user_id=user["id"],
                role="assistant",
                content=plan.narration,
                structured=plan.model_dump(),
            ),
        ]
    )
    await session.commit()
    return ChatResponse(plan=plan, provider=provider.name)
