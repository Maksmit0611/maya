"""Direct async route tests complement the HTTP contract tests without network access."""

from types import SimpleNamespace
from uuid import UUID

import httpx
import pytest

from app.api.v1 import briefs, chat, jobs, projects, results, rooms
from app.core.config import Settings
from app.core.db import make_session_factory
from app.core.errors import AppError
from app.models import Asset, Base, Result
from app.schemas.api import (
    BriefCreate,
    ChatRequest,
    JobCreate,
    ProjectCreate,
    RoomCreate,
    SelectResult,
    UploadURLRequest,
)
from tests.test_api import FakeAsyncClient

USER = {"id": "direct-user", "email": "direct-user@local.invalid"}


class LocalRequest:
    def __init__(self, signing_key: bytes, content_type: str, content: bytes):
        self.app = SimpleNamespace(state=SimpleNamespace(upload_signing_key=signing_key))
        self.headers = {"content-type": content_type}
        self.content = content

    async def stream(self):
        yield self.content


@pytest.mark.asyncio
async def test_direct_project_brief_chat_jobs_and_results(tmp_path):
    database_url = f"sqlite+aiosqlite:///{tmp_path / 'direct.db'}"
    engine, factory = make_session_factory(database_url)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    async with factory() as session:
        project = await projects.create_project(ProjectCreate(name="Direct project"), session, USER)
        assert (await projects.list_projects(session, USER))[0].id == project.id
        assert (await projects.get_project(project.id, session, USER)).id == project.id

        room = await rooms.create_room(
            project.id, RoomCreate(name="Dining room", room_type="dining"), session, USER
        )
        assert (await rooms.list_rooms(project.id, session, USER))[0].id == room.id
        first = await briefs.create_brief(
            project.id,
            BriefCreate(room_id=room.id, content={"style": "Soft modern"}),
            session,
            USER,
        )
        second = await briefs.create_brief(
            project.id, BriefCreate(content={"style": "Natural"}), session, USER
        )
        assert (first.version, second.version) == (1, 2)
        assert len(await briefs.list_briefs(project.id, session, USER)) == 2

        chat_result = await chat.plan_design(
            ChatRequest(
                project_id=project.id, brief={"style": "Soft modern"}, message="Give me a plan"
            ),
            session,
            USER,
            Settings(),
        )
        assert chat_result.provider == "mock"
        payload = JobCreate(project_id=project.id, room_id=room.id, brief={"style": "Soft modern"})
        job = await jobs.create_job(payload, session, USER, "direct-idem")
        replay = await jobs.create_job(payload, session, USER, "direct-idem")
        assert job.id == replay.id
        assert (await jobs.list_jobs(project.id, session, USER))[0].id == job.id
        assert (await jobs.get_job(job.id, session, USER)).id == job.id
        assert (await jobs.cancel_job(job.id, session, USER)).cancellation_requested

        result = Result(
            job_id=job.id,
            prompt_version="design_plan_v1",
            prompt_hash="1" * 64,
            output_json={
                "plan": chat_result.plan.model_dump(),
                "media": {"kind": "placeholder_metadata"},
            },
        )
        session.add(result)
        await session.commit()
        assert (await results.list_results(project.id, session, USER))[0].id == result.id
        selected = await results.select_result(result.id, SelectResult(), session, USER)
        assert selected.selected_by == USER["id"]
        await projects.rename_project(project.id, ProjectCreate(name="Renamed"), session, USER)
        assert (await projects.get_project(project.id, session, USER)).name == "Renamed"
        await projects.delete_project(project.id, session, USER)
    await engine.dispose()


@pytest.mark.asyncio
async def test_direct_local_and_supabase_upload_adapters(tmp_path, monkeypatch):
    database_url = f"sqlite+aiosqlite:///{tmp_path / 'upload.db'}"
    engine, factory = make_session_factory(database_url)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    key = b"local-upload-signing-key"
    settings = Settings(
        database_url=database_url, upload_dir=str(tmp_path / "uploads"), max_upload_bytes=64
    )
    request = LocalRequest(key, "application/json", b"")
    async with factory() as session:
        project = await projects.create_project(ProjectCreate(name="Upload project"), session, USER)
        room = await rooms.create_room(project.id, RoomCreate(name="Study"), session, USER)
        upload = await rooms.create_upload_url(
            project.id,
            UploadURLRequest(
                room_id=room.id, filename="study.png", mime_type="image/png", size_bytes=12
            ),
            request,
            session,
            USER,
            settings,
        )
        png = b"\x89PNG\r\n\x1a\n" + b"1234"
        local_request = LocalRequest(key, "image/png", png)
        await rooms.local_upload(
            upload.asset_id,
            local_request,
            upload.headers["x-maya-upload-token"],
            session,
            settings,
        )
        asset = await session.get(Asset, upload.asset_id)
        assert asset is not None and asset.size_bytes == len(png)

        supabase_settings = Settings(
            supabase_url="https://project.supabase.co",
            supabase_service_role_key="server-only",
        )
        def response_factory(url, **kwargs):
            return httpx.Response(
                200,
                json={"url": "/object/upload/sign/maya-assets/project/file.png?token=temporary"},
                request=httpx.Request("POST", url),
            )
        monkeypatch.setattr(
            httpx,
            "AsyncClient",
            lambda **kwargs: FakeAsyncClient(post_response=response_factory),
        )
        signed = await rooms.create_upload_url(
            project.id,
            UploadURLRequest(filename="another.png", mime_type="image/png", size_bytes=12),
            request,
            session,
            USER,
            supabase_settings,
        )
        assert signed.upload_url.startswith("https://project.supabase.co/storage/v1/")

        with pytest.raises(AppError):
            await rooms.create_upload_url(
                project.id,
                UploadURLRequest(
                    room_id=UUID("00000000-0000-0000-0000-000000000001"),
                    filename="missing.png",
                    mime_type="image/png",
                    size_bytes=12,
                ),
                request,
                session,
                USER,
                settings,
            )

        with pytest.raises(AppError):
            await rooms.local_upload(
                upload.asset_id,
                LocalRequest(key, "image/png", b"not an image"),
                upload.headers["x-maya-upload-token"],
                session,
                settings,
            )
    await engine.dispose()
