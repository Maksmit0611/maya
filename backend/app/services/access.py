from uuid import UUID

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.models import Project, ProjectMember


async def require_project_access(session: AsyncSession, project_id: UUID, user_id: str) -> Project:
    member = exists().where(
        ProjectMember.project_id == Project.id,
        ProjectMember.user_id == user_id,
    )
    project = await session.scalar(
        select(Project).where(
            Project.id == project_id,
            (Project.owner_id == user_id) | member,
        )
    )
    if project is None:
        raise AppError("not_found", "Project not found", 404)
    return project
