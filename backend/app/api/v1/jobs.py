from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db import get_session
from app.core.errors import AppError
from app.models import GenerationJob, Room
from app.schemas.api import JobCreate, JobRead
from app.services.access import require_project_access
from app.services.provenance import record_provenance

router = APIRouter()
Session = Annotated[AsyncSession, Depends(get_session)]
User = Annotated[dict[str, str], Depends(get_current_user)]


@router.post("", response_model=JobRead, status_code=202)
async def create_job(
    payload: JobCreate,
    session: Session,
    user: User,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=1, max_length=200)],
) -> GenerationJob:
    await require_project_access(session, payload.project_id, user["id"])
    if (
        payload.room_id
        and await session.scalar(
            select(Room.id).where(Room.id == payload.room_id, Room.project_id == payload.project_id)
        )
        is None
    ):
        raise AppError("not_found", "Room not found", 404)
    stored_input = {
        "brief": payload.brief,
        "room_id": str(payload.room_id) if payload.room_id else None,
    }
    existing = await session.scalar(
        select(GenerationJob).where(
            GenerationJob.project_id == payload.project_id,
            GenerationJob.idempotency_key == idempotency_key,
        )
    )
    if existing:
        if existing.input_json != stored_input:
            raise AppError(
                "idempotency_conflict",
                "This Idempotency-Key was already used for a different request",
                409,
            )
        return existing
    job = GenerationJob(
        project_id=payload.project_id,
        room_id=payload.room_id,
        requested_by=user["id"],
        idempotency_key=idempotency_key,
        input_json=stored_input,
        provenance=record_provenance("pending", "pending"),
    )
    session.add(job)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        existing = await session.scalar(
            select(GenerationJob).where(
                GenerationJob.project_id == payload.project_id,
                GenerationJob.idempotency_key == idempotency_key,
            )
        )
        if existing is None:
            raise
        if existing.input_json != stored_input:
            raise AppError(
                "idempotency_conflict",
                "This Idempotency-Key was already used for a different request",
                409,
            ) from exc
        return existing
    await session.refresh(job)
    return job


@router.get("", response_model=list[JobRead])
async def list_jobs(
    project_id: Annotated[UUID, Query()], session: Session, user: User
) -> list[GenerationJob]:
    await require_project_access(session, project_id, user["id"])
    return list(
        (
            await session.scalars(
                select(GenerationJob)
                .where(GenerationJob.project_id == project_id)
                .order_by(GenerationJob.created_at.desc())
            )
        ).all()
    )


@router.get("/{job_id}", response_model=JobRead)
async def get_job(job_id: UUID, session: Session, user: User) -> GenerationJob:
    job = await session.get(GenerationJob, job_id)
    if job is None:
        raise AppError("not_found", "Job not found", 404)
    await require_project_access(session, job.project_id, user["id"])
    return job


@router.post("/{job_id}/cancel", response_model=JobRead)
async def cancel_job(job_id: UUID, session: Session, user: User) -> GenerationJob:
    job = await session.get(GenerationJob, job_id)
    if job is None:
        raise AppError("not_found", "Job not found", 404)
    await require_project_access(session, job.project_id, user["id"])
    if job.status in {"queued", "running"}:
        job.cancellation_requested = True
        job.updated_at = datetime.now(UTC)
        await session.commit()
        await session.refresh(job)
    return job
