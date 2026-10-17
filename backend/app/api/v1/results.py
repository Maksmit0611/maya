from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db import get_session
from app.core.errors import AppError
from app.models import GenerationJob, Result
from app.schemas.api import ResultRead, SelectResult
from app.services.access import require_project_access

router = APIRouter()
Session = Annotated[AsyncSession, Depends(get_session)]
User = Annotated[dict[str, str], Depends(get_current_user)]


@router.get("/projects/{project_id}/results", response_model=list[ResultRead])
async def list_results(project_id: UUID, session: Session, user: User) -> list[Result]:
    await require_project_access(session, project_id, user["id"])
    return list(
        (
            await session.scalars(
                select(Result)
                .join(GenerationJob)
                .where(GenerationJob.project_id == project_id)
                .order_by(Result.created_at.desc())
            )
        ).all()
    )


@router.post("/results/{result_id}/select", response_model=ResultRead)
async def select_result(
    result_id: UUID, payload: SelectResult, session: Session, user: User
) -> Result:
    result = await session.get(Result, result_id)
    if result is None:
        raise AppError("not_found", "Result not found", 404)
    job = await session.get(GenerationJob, result.job_id)
    if job is None:
        raise AppError("not_found", "Result job not found", 404)
    await require_project_access(session, job.project_id, user["id"])
    result.selected_by = user["id"] if payload.selected else None
    result.selected_at = datetime.now(UTC) if payload.selected else None
    await session.commit()
    await session.refresh(result)
    return result
