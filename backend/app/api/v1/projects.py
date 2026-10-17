from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db import get_session
from app.core.errors import AppError
from app.models import Project, ProjectMember
from app.schemas.api import ProjectCreate, ProjectRead
from app.services.access import require_project_access

router = APIRouter()
Session = Annotated[AsyncSession, Depends(get_session)]
User = Annotated[dict[str, str], Depends(get_current_user)]


@router.post("", response_model=ProjectRead, status_code=201)
async def create_project(payload: ProjectCreate, session: Session, user: User) -> Project:
    project = Project(owner_id=user["id"], name=payload.name)
    session.add(project)
    await session.flush()
    session.add(ProjectMember(project_id=project.id, user_id=user["id"], role="owner"))
    await session.commit()
    await session.refresh(project)
    return project


@router.get("", response_model=list[ProjectRead])
async def list_projects(session: Session, user: User) -> list[Project]:
    member_ids = select(ProjectMember.project_id).where(ProjectMember.user_id == user["id"])
    return list(
        (
            await session.scalars(
                select(Project)
                .where((Project.owner_id == user["id"]) | Project.id.in_(member_ids))
                .order_by(Project.created_at.desc())
            )
        ).all()
    )


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: UUID, session: Session, user: User) -> Project:
    return await require_project_access(session, project_id, user["id"])


@router.patch("/{project_id}", response_model=ProjectRead)
async def rename_project(
    project_id: UUID, payload: ProjectCreate, session: Session, user: User
) -> Project:
    project = await require_project_access(session, project_id, user["id"])
    if project.owner_id != user["id"]:
        raise AppError("forbidden", "Only the project owner can rename it", 403)
    project.name = payload.name
    await session.commit()
    await session.refresh(project)
    return project


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: UUID, session: Session, user: User) -> None:
    project = await require_project_access(session, project_id, user["id"])
    if project.owner_id != user["id"]:
        raise AppError("forbidden", "Only the project owner can delete it", 403)
    await session.delete(project)
    await session.commit()
