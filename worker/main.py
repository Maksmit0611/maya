import asyncio
from datetime import UTC, datetime
from types import SimpleNamespace
from uuid import UUID

from sqlalchemy import select

from app.core.config import get_settings
from app.core.db import make_session_factory
from app.core.errors import AppError
from app.models import GenerationJob, Result
from app.services.provenance import record_provenance
from app.services.providers import chat_provider, media_provider

POLL_SECONDS = 2
HEARTBEAT_SECONDS = 10


async def claim_job(factory) -> UUID | None:
    async with factory() as session:
        job = await session.scalar(
            select(GenerationJob)
            .where(GenerationJob.status == "queued")
            .order_by(GenerationJob.created_at)
            .limit(1)
            .with_for_update(skip_locked=True)
        )
        if job is None:
            return None
        job.status = "running"
        job.started_at = datetime.now(UTC)
        job.heartbeat_at = job.started_at
        job.updated_at = job.started_at
        await session.commit()
        return job.id


async def heartbeat(factory, job_id: UUID, stop: asyncio.Event) -> None:
    while not stop.is_set():
        try:
            await asyncio.wait_for(stop.wait(), timeout=HEARTBEAT_SECONDS)
        except TimeoutError:
            async with factory() as session:
                job = await session.get(GenerationJob, job_id)
                if job is None or job.status != "running":
                    return
                job.heartbeat_at = datetime.now(UTC)
                job.updated_at = job.heartbeat_at
                await session.commit()


async def process_job(factory, job_id: UUID) -> None:
    settings = get_settings()
    stop = asyncio.Event()
    heartbeat_task = asyncio.create_task(heartbeat(factory, job_id, stop))
    try:
        async with factory() as session:
            job = await session.get(GenerationJob, job_id)
            if job is None:
                return
            if job.cancellation_requested:
                job.status = "cancelled"
                job.finished_at = datetime.now(UTC)
                await session.commit()
                return
            brief = dict(job.input_json.get("brief", job.input_json))
        plan_provider = chat_provider(settings)
        plan = await plan_provider.plan(brief)
        async with factory() as session:
            job = await session.get(GenerationJob, job_id)
            if job is None:
                return
            if job.cancellation_requested:
                job.status = "cancelled"
                job.finished_at = datetime.now(UTC)
                await session.commit()
                return
        media = media_provider(settings)
        media_result = await media.generate(SimpleNamespace(id=job_id, input_json=brief))
        async with factory() as session:
            job = await session.get(GenerationJob, job_id)
            if job is None:
                return
            if job.cancellation_requested:
                job.status = "cancelled"
                job.finished_at = datetime.now(UTC)
                await session.commit()
                return
            provenance = record_provenance(
                plan_provider.name, getattr(plan_provider, "_model", "mock")
            )
            provenance.update(
                {"media_provider": media.name, "completed_at": datetime.now(UTC).isoformat()}
            )
            job.provenance = provenance
            result = Result(
                job_id=job.id,
                prompt_version=provenance["prompt_version"],
                prompt_hash=provenance["prompt_sha256"],
                output_json={"plan": plan.model_dump(), "media": media_result},
            )
            session.add(result)
            job.status = "succeeded"
            job.finished_at = datetime.now(UTC)
            job.updated_at = job.finished_at
            await session.commit()
    except Exception as exc:  # worker boundary: persist a safe, structured failure
        async with factory() as session:
            job = await session.get(GenerationJob, job_id)
            if job is not None:
                job.status = "failed"
                job.error_json = {
                    "code": exc.code if isinstance(exc, AppError) else "generation_failed",
                    "message": exc.message
                    if isinstance(exc, AppError)
                    else "Generation failed in a provider stage",
                }
                job.finished_at = datetime.now(UTC)
                job.updated_at = job.finished_at
                await session.commit()
    finally:
        stop.set()
        await heartbeat_task


async def run() -> None:
    settings = get_settings()
    engine, factory = make_session_factory(settings.database_url)
    try:
        while True:
            job_id = await claim_job(factory)
            if job_id is None:
                await asyncio.sleep(POLL_SECONDS)
            else:
                await process_job(factory, job_id)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run())
