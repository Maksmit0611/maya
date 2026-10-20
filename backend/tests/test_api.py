import asyncio
import base64
import json
from datetime import UTC, datetime, timedelta
from uuid import UUID

import httpx
import jwt
import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.core.errors import AppError
from app.main import create_app
from app.models import Result


class FakeAsyncClient:
    def __init__(self, *args, get_response=None, post_response=None, **kwargs):
        self.get_response = get_response
        self.post_response = post_response

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return None

    async def get(self, url, **kwargs):
        if callable(self.get_response):
            return self.get_response(url, **kwargs)
        return self.get_response

    async def post(self, url, **kwargs):
        if callable(self.post_response):
            return self.post_response(url, **kwargs)
        return self.post_response


def client_for(tmp_path, **overrides):
    options = {
        "database_url": f"sqlite+aiosqlite:///{tmp_path / 'test.db'}",
        "upload_dir": str(tmp_path / "uploads"),
        "environment": "test",
        **overrides,
    }
    settings = Settings(**options)
    return TestClient(create_app(settings))


def create_project(client: TestClient) -> str:
    response = client.post("/api/v1/projects", json={"name": "Reading nook"})
    assert response.status_code == 201
    return response.json()["id"]


def test_health_and_dev_auth_mode(tmp_path):
    with client_for(tmp_path) as client:
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json()["auth_mode"].startswith("dev-user")
        assert client.get("/api/v1/projects").json() == []


def test_auth_fails_closed_when_supabase_is_configured(tmp_path):
    with client_for(
        tmp_path, supabase_url="https://project.supabase.co", dev_auth_enabled=False
    ) as client:
        response = client.get("/api/v1/projects")
        assert response.status_code == 401
        assert response.json()["code"] == "unauthorized"


def test_production_startup_requires_supabase_auth_even_if_dev_auth_enabled(tmp_path):
    settings = Settings(
        database_url=f"sqlite+aiosqlite:///{tmp_path / 'production.db'}",
        environment="production",
        dev_auth_enabled=True,
    )

    with pytest.raises(ValueError, match="Supabase authentication must be configured"):
        create_app(settings)


def test_production_never_falls_back_to_dev_user(tmp_path):
    with client_for(
        tmp_path,
        environment="production",
        supabase_url="https://project.supabase.co",
        dev_auth_enabled=True,
    ) as client:
        response = client.get("/api/v1/projects")
        assert response.status_code == 401
        assert response.json()["code"] == "unauthorized"
        assert client.get("/healthz").json()["auth_mode"] == "supabase"


def test_dev_auth_can_be_disabled_outside_production(tmp_path):
    with client_for(tmp_path, environment="test", dev_auth_enabled=False) as client:
        response = client.get("/api/v1/projects")
        assert response.status_code == 401
        assert response.json()["code"] == "unauthorized"
        assert client.get("/healthz").json()["auth_mode"] == "disabled"


def test_error_envelope_has_request_id(tmp_path):
    with client_for(tmp_path) as client:
        response = client.post("/api/v1/projects", json={})
        body = response.json()
        assert response.status_code == 422
        assert body["code"] == "validation_error"
        assert body["request_id"] == response.headers["x-request-id"]
        assert body["details"]


def test_idempotency_replay_and_payload_conflict(tmp_path):
    with client_for(tmp_path) as client:
        project_id = create_project(client)
        headers = {"Idempotency-Key": "brief-run-001"}
        payload = {"project_id": project_id, "brief": {"style": "Japandi"}}
        first = client.post("/api/v1/jobs", json=payload, headers=headers)
        replay = client.post("/api/v1/jobs", json=payload, headers=headers)
        conflict = client.post(
            "/api/v1/jobs", json={**payload, "brief": {"style": "Industrial"}}, headers=headers
        )
        assert first.status_code == 202
        assert replay.status_code == 202
        assert first.json()["id"] == replay.json()["id"]
        assert conflict.status_code == 409
        assert conflict.json()["code"] == "idempotency_conflict"


def test_cancel_sets_flag_without_unbounded_status_transition(tmp_path):
    with client_for(tmp_path) as client:
        project_id = create_project(client)
        created = client.post(
            "/api/v1/jobs",
            json={"project_id": project_id, "brief": {}},
            headers={"Idempotency-Key": "cancel-1"},
        ).json()
        response = client.post(f"/api/v1/jobs/{created['id']}/cancel")
        assert response.status_code == 200
        assert response.json()["cancellation_requested"] is True
        assert response.json()["status"] == "queued"


def test_room_brief_chat_plan_and_results_access(tmp_path):
    with client_for(tmp_path) as client:
        project_id = create_project(client)
        room = client.post(f"/api/v1/projects/{project_id}/rooms", json={"name": "Living room"})
        assert room.status_code == 201
        brief = client.post(
            f"/api/v1/projects/{project_id}/briefs",
            json={"room_id": room.json()["id"], "content": {"style": "Soft modern"}},
        )
        assert brief.status_code == 201
        assert brief.json()["version"] == 1
        plan = client.post(
            "/api/v1/chat",
            json={
                "project_id": project_id,
                "brief": {"style": "Soft modern"},
                "message": "Suggest a direction",
            },
        )
        assert plan.status_code == 200
        assert plan.json()["provider"] == "mock"
        assert plan.json()["plan"]["style"] == "Soft modern"
        assert plan.json()["plan"]["palette"][0]["hex"].startswith("#")
        assert client.get(f"/api/v1/projects/{project_id}/results").json() == []


def test_signed_local_upload_is_scoped_and_validates_signature(tmp_path):
    png = bytes.fromhex("89504e470d0a1a0a00000000") + b"test-image-data"
    with client_for(tmp_path) as client:
        project_id = create_project(client)
        room_id = client.post(
            f"/api/v1/projects/{project_id}/rooms", json={"name": "Office"}
        ).json()["id"]
        signed = client.post(
            f"/api/v1/projects/{project_id}/assets/upload-url",
            json={
                "room_id": room_id,
                "filename": "room.png",
                "mime_type": "image/png",
                "size_bytes": len(png),
            },
        )
        assert signed.status_code == 201
        upload = signed.json()
        headers = {**upload["headers"], "x-maya-upload-token": "0" * 64}
        bad = client.put(upload["upload_url"], content=png, headers=headers)
        assert bad.status_code == 403
        headers["x-maya-upload-token"] = upload["headers"]["x-maya-upload-token"]
        good = client.put(upload["upload_url"], content=png, headers=headers)
        assert good.status_code == 204


def test_mock_chat_provider_returns_schema_valid_plan(tmp_path):
    import asyncio

    from app.providers.chat.mock import MockChatProvider

    plan = asyncio.run(MockChatProvider().plan({"style": "Coastal"}))
    assert plan.style == "Coastal"
    assert len(plan.palette) == 3
    assert plan.model_dump()["scene_beats"]


def test_comfyui_provider_reports_degraded_state(tmp_path):
    import asyncio

    import pytest

    from app.core.errors import ProviderUnavailable
    from app.providers.media.comfyui import ComfyUIProvider

    with pytest.raises(ProviderUnavailable):
        asyncio.run(ComfyUIProvider(None).generate({"id": "mock"}))


def test_job_list_is_project_scoped(tmp_path):
    with client_for(tmp_path) as client:
        project_id = create_project(client)
        client.post(
            "/api/v1/jobs",
            json={"project_id": project_id, "brief": {"style": "Natural"}},
            headers={"Idempotency-Key": "list-1"},
        )
        listed = client.get(f"/api/v1/jobs?project_id={project_id}")
        assert listed.status_code == 200
        assert len(listed.json()) == 1


def test_projects_crud_and_membership_boundary(tmp_path):
    with client_for(tmp_path) as client:
        project_id = create_project(client)
        assert len(client.get("/api/v1/projects").json()) == 1
        assert client.get(f"/api/v1/projects/{project_id}").json()["name"] == "Reading nook"
        updated = client.patch(
            f"/api/v1/projects/{project_id}", json={"name": "Quiet reading room"}
        )
        assert updated.status_code == 200
        assert updated.json()["name"] == "Quiet reading room"

        from app.core.auth import get_current_user

        client.app.dependency_overrides[get_current_user] = lambda: {
            "id": "other-user",
            "email": "",
        }
        assert client.get(f"/api/v1/projects/{project_id}").status_code == 404
        client.app.dependency_overrides[get_current_user] = lambda: {"id": "dev-user", "email": ""}
        assert client.delete(f"/api/v1/projects/{project_id}").status_code == 204
        assert client.get(f"/api/v1/projects/{project_id}").status_code == 404


def test_brief_versions_and_room_validation(tmp_path):
    with client_for(tmp_path) as client:
        project_id = create_project(client)
        first = client.post(
            f"/api/v1/projects/{project_id}/briefs", json={"content": {"style": "Coastal"}}
        )
        second = client.post(
            f"/api/v1/projects/{project_id}/briefs", json={"content": {"style": "Modern"}}
        )
        assert first.json()["version"] == 1
        assert second.json()["version"] == 2
        assert len(client.get(f"/api/v1/projects/{project_id}/briefs").json()) == 2
        invalid_room = client.post(
            f"/api/v1/projects/{project_id}/briefs",
            json={"room_id": "00000000-0000-0000-0000-000000000001", "content": {}},
        )
        assert invalid_room.status_code == 404
        assert client.get(f"/api/v1/projects/{project_id}/rooms").json() == []


def test_job_status_not_found_and_invalid_room(tmp_path):
    with client_for(tmp_path) as client:
        project_id = create_project(client)
        invalid = client.post(
            "/api/v1/jobs",
            json={
                "project_id": project_id,
                "room_id": "00000000-0000-0000-0000-000000000001",
                "brief": {},
            },
            headers={"Idempotency-Key": "bad-room"},
        )
        assert invalid.status_code == 404
        missing = client.get("/api/v1/jobs/00000000-0000-0000-0000-000000000001")
        assert missing.status_code == 404
        created = client.post(
            "/api/v1/jobs",
            json={"project_id": project_id, "brief": {}},
            headers={"Idempotency-Key": "job-status"},
        ).json()
        assert client.get(f"/api/v1/jobs/{created['id']}").json()["status"] == "queued"


def test_result_list_select_and_unselect(tmp_path):
    with client_for(tmp_path) as client:
        project_id = create_project(client)
        job = client.post(
            "/api/v1/jobs",
            json={"project_id": project_id, "brief": {}},
            headers={"Idempotency-Key": "result-1"},
        ).json()

        async def insert_result() -> str:
            async with client.app.state.session_factory() as session:
                row = Result(
                    job_id=UUID(job["id"]),
                    prompt_version="design_plan_v1",
                    prompt_hash="0" * 64,
                    output_json={
                        "plan": {"style": "Warm modern"},
                        "media": {"kind": "placeholder_metadata"},
                    },
                )
                session.add(row)
                await session.commit()
                return str(row.id)

        result_id = asyncio.run(insert_result())
        assert len(client.get(f"/api/v1/projects/{project_id}/results").json()) == 1
        selected = client.post(f"/api/v1/results/{result_id}/select", json={"selected": True})
        assert selected.status_code == 200
        assert selected.json()["selected_by"] == "dev-user"
        unselected = client.post(f"/api/v1/results/{result_id}/select", json={"selected": False})
        assert unselected.json()["selected_by"] is None
        assert (
            client.post(
                "/api/v1/results/00000000-0000-0000-0000-000000000001/select", json={}
            ).status_code
            == 404
        )


def test_auth_hs256_and_jwks_validation(monkeypatch):
    from app.core.auth import _verify_supabase_token

    secret = "local-test-jwt-secret"
    claims = {
        "sub": "user-123",
        "aud": "authenticated",
        "exp": datetime.now(UTC) + timedelta(minutes=5),
    }
    hs_token = jwt.encode(claims, secret, algorithm="HS256")
    settings = Settings(supabase_url="https://project.supabase.co", supabase_jwt_secret=secret)
    assert asyncio.run(_verify_supabase_token(hs_token, settings))["sub"] == "user-123"
    with pytest.raises(AppError):
        asyncio.run(_verify_supabase_token("not.a.jwt", settings))

    jwks_secret = b"mock-jwks-secret"
    jwks_token = jwt.encode(claims, jwks_secret, algorithm="HS256", headers={"kid": "mock-key"})
    jwk = {
        "kty": "oct",
        "alg": "HS256",
        "use": "sig",
        "kid": "mock-key",
        "k": base64.urlsafe_b64encode(jwks_secret).decode().rstrip("="),
    }

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kwargs: FakeAsyncClient(
            get_response=lambda url, **_kwargs: httpx.Response(
                200, json={"keys": [jwk]}, request=httpx.Request("GET", url)
            )
        ),
    )
    jwks_settings = Settings(supabase_url="https://project.supabase.co")
    assert asyncio.run(_verify_supabase_token(jwks_token, jwks_settings))["sub"] == "user-123"


def test_auth_rejects_unknown_jwks_key(monkeypatch):
    from app.core.auth import _verify_supabase_token

    token = jwt.encode(
        {"sub": "user", "aud": "authenticated"},
        "secret",
        algorithm="HS256",
        headers={"kid": "missing"},
    )

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kwargs: FakeAsyncClient(
            get_response=lambda url, **_kwargs: httpx.Response(
                200, json={"keys": []}, request=httpx.Request("GET", url)
            )
        ),
    )
    with pytest.raises(AppError) as error:
        asyncio.run(
            _verify_supabase_token(token, Settings(supabase_url="https://project.supabase.co"))
        )
    assert error.value.status_code == 401


def test_gemini_provider_validates_response_and_handles_invalid_json(monkeypatch):
    from app.providers.chat.gemini import GeminiChatProvider

    plan = {
        "style": "Soft modern",
        "palette": [
            {"name": "Linen", "hex": "#E9E2D5", "role": "walls"},
            {"name": "Oak", "hex": "#A9784F", "role": "warm accent"},
            {"name": "Sage", "hex": "#879184", "role": "soft contrast"},
        ],
        "camera_moves": ["wide reveal"],
        "scene_beats": ["reveal the room", "show the palette", "close on material details"],
        "narration": "A calm concept.",
        "constraints": ["Visualisation only."],
    }

    def valid_post(url, **kwargs):
        assert "secret-key" not in url
        assert kwargs["headers"]["x-goog-api-key"] == "secret-key"
        response_format = kwargs["json"]["generationConfig"]["responseFormat"]["text"]
        assert response_format["mimeType"] == "application/json"
        assert response_format["schema"]["properties"]["palette"]["minItems"] == 3
        prompt = kwargs["json"]["contents"][0]["parts"][0]["text"]
        assert '"style": "Soft modern"' in prompt
        assert "untrusted user data" in prompt
        return httpx.Response(
            200,
            json={"candidates": [{"content": {"parts": [{"text": json.dumps(plan)}]}}]},
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kwargs: FakeAsyncClient(post_response=valid_post),
    )
    provider = GeminiChatProvider("secret-key", "test-model")
    assert asyncio.run(provider.plan({"style": "Soft modern"})).style == "Soft modern"

    def invalid_post(url, **kwargs):
        return httpx.Response(
            200,
            json={"candidates": [{"content": {"parts": [{"text": "{}"}]}}]},
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kwargs: FakeAsyncClient(post_response=invalid_post),
    )
    with pytest.raises(AppError):
        asyncio.run(provider.plan({}))


def test_provider_selection_and_keyless_media_metadata(tmp_path, monkeypatch):
    from app.providers.chat.gemini import GeminiChatProvider
    from app.providers.chat.mock import MockChatProvider
    from app.providers.media.comfyui import ComfyUIProvider
    from app.providers.media.mock import MockMediaProvider
    from app.services.providers import chat_provider, media_provider

    assert isinstance(chat_provider(Settings()), MockChatProvider)
    assert isinstance(chat_provider(Settings(gemini_api_key="configured")), GeminiChatProvider)
    assert isinstance(media_provider(Settings()), MockMediaProvider)
    assert isinstance(media_provider(Settings(comfyui_base_url="http://comfy")), ComfyUIProvider)
    monkeypatch.setattr("app.providers.media.mock._has_ffmpeg", lambda: False)

    class Job:
        id = "00000000-0000-0000-0000-000000000002"

    output = asyncio.run(MockMediaProvider(str(tmp_path / "media")).generate(Job()))
    assert output["kind"] == "placeholder_metadata"
    assert output["ffmpeg_available"] is False


def test_supabase_signed_upload_url_and_missing_service_key(tmp_path, monkeypatch):
    from app.core.auth import get_current_user

    settings = Settings(
        database_url=f"sqlite+aiosqlite:///{tmp_path / 'supabase-storage.db'}",
        upload_dir=str(tmp_path / "uploads"),
        environment="test",
        supabase_url="https://project.supabase.co",
        supabase_service_role_key="server-only-test",
    )
    app = create_app(settings)
    app.dependency_overrides[get_current_user] = lambda: {"id": "demo-user", "email": ""}

    def signed_upload(url, **kwargs):
        assert "server-only-test" not in url
        assert kwargs["headers"]["Authorization"] == "Bearer server-only-test"
        return httpx.Response(
            200,
            json={"url": "/object/upload/sign/maya-assets/project/file.png?token=temporary"},
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kwargs: FakeAsyncClient(post_response=signed_upload),
    )
    with TestClient(app) as client:
        project_id = client.post("/api/v1/projects", json={"name": "Private files"}).json()["id"]
        response = client.post(
            f"/api/v1/projects/{project_id}/assets/upload-url",
            json={
                "filename": "room.png",
                "mime_type": "image/png",
                "size_bytes": 99,
            },
        )
        assert response.status_code == 201
        assert response.json()["upload_url"].startswith(
            "https://project.supabase.co/storage/v1/object/upload/sign/"
        )

    settings_without_key = Settings(
        database_url=f"sqlite+aiosqlite:///{tmp_path / 'supabase-no-key.db'}",
        environment="test",
        supabase_url="https://project.supabase.co",
    )
    app_without_key = create_app(settings_without_key)
    app_without_key.dependency_overrides[get_current_user] = lambda: {
        "id": "demo-user",
        "email": "",
    }
    with TestClient(app_without_key) as client:
        project_id = client.post("/api/v1/projects", json={"name": "Private files"}).json()["id"]
        response = client.post(
            f"/api/v1/projects/{project_id}/assets/upload-url",
            json={
                "filename": "room.png",
                "mime_type": "image/png",
                "size_bytes": 99,
            },
        )
        assert response.status_code == 503


def test_upload_limits_room_scope_and_bad_image_bytes(tmp_path):
    with client_for(tmp_path, max_upload_bytes=10) as client:
        project_id = create_project(client)
        too_large = client.post(
            f"/api/v1/projects/{project_id}/assets/upload-url",
            json={
                "filename": "room.png",
                "mime_type": "image/png",
                "size_bytes": 11,
            },
        )
        assert too_large.status_code == 413
        wrong_room = client.post(
            f"/api/v1/projects/{project_id}/assets/upload-url",
            json={
                "room_id": "00000000-0000-0000-0000-000000000001",
                "filename": "room.png",
                "mime_type": "image/png",
                "size_bytes": 9,
            },
        )
        assert wrong_room.status_code == 404
        signed = client.post(
            f"/api/v1/projects/{project_id}/assets/upload-url",
            json={
                "filename": "room.png",
                "mime_type": "image/png",
                "size_bytes": 9,
            },
        ).json()
        bad_bytes = client.put(
            signed["upload_url"], content=b"not an image", headers=signed["headers"]
        )
        assert bad_bytes.status_code == 413


def test_unhandled_http_errors_keep_structured_envelope(tmp_path):
    with client_for(tmp_path) as client:
        response = client.get("/route-that-does-not-exist")
        assert response.status_code == 404
        assert response.json()["code"] == "http_error"
        assert response.json()["request_id"] == response.headers["x-request-id"]
