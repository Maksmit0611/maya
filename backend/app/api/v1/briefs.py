from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db import get_session
from app.core.errors import AppError
from app.models import Brief, Room
from app.schemas.api import BriefCreate, BriefRead
from app.services.access import require_project_access

router = APIRouter()
Session = Annotated[AsyncSession, Depends(get_session)]
User = Annotated[dict[str, str], Depends(get_current_user)]


@router.post("/projects/{project_id}/briefs", response_model=BriefRead, status_code=201)
async def create_brief(
    project_id: UUID, payload: BriefCreate, session: Session, user: User
) -> Brief:
    await require_project_access(session, project_id, user["id"])
    if payload.room_id:
        room = await session.scalar(
            select(Room).where(Room.id == payload.room_id, Room.project_id == project_id)
        )
        if room is None:
            raise AppError("not_found", "Room not found", 404)
    latest = await session.scalar(
        select(Brief.version)
        .where(Brief.project_id == project_id)
        .order_by(Brief.version.desc())
        .limit(1)
    )
    brief = Brief(
        project_id=project_id,
        room_id=payload.room_id,
        version=(latest or 0) + 1,
        content=payload.content,
        created_by=user["id"],
    )
    session.add(brief)
    await session.commit()
    await session.refresh(brief)
    return brief


@router.get("/projects/{project_id}/briefs", response_model=list[BriefRead])
async def list_briefs(project_id: UUID, session: Session, user: User) -> list[Brief]:
    await require_project_access(session, project_id, user["id"])
    return list(
        (
            await session.scalars(
                select(Brief).where(Brief.project_id == project_id).order_by(Brief.version.desc())
            )
        ).all()
    )
