import hashlib
import hmac
import re
from pathlib import Path
from typing import Annotated
from urllib.parse import quote
from uuid import UUID, uuid4

import httpx
from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.config import Settings, get_settings
from app.core.db import get_session
from app.core.errors import AppError, ProviderUnavailable
from app.models import Asset, Room
from app.schemas.api import RoomCreate, RoomRead, UploadURLRequest, UploadURLResponse
from app.services.access import require_project_access

router = APIRouter()
Session = Annotated[AsyncSession, Depends(get_session)]
User = Annotated[dict[str, str], Depends(get_current_user)]
Config = Annotated[Settings, Depends(get_settings)]


@router.get("/projects/{project_id}/rooms", response_model=list[RoomRead])
async def list_rooms(project_id: UUID, session: Session, user: User) -> list[Room]:
    await require_project_access(session, project_id, user["id"])
    return list(
        (
            await session.scalars(
                select(Room).where(Room.project_id == project_id).order_by(Room.created_at)
            )
        ).all()
    )


@router.post("/projects/{project_id}/rooms", response_model=RoomRead, status_code=201)
async def create_room(project_id: UUID, payload: RoomCreate, session: Session, user: User) -> Room:
    await require_project_access(session, project_id, user["id"])
    room = Room(
        project_id=project_id,
        name=payload.name,
        room_type=payload.room_type,
        dimensions=payload.dimensions,
    )
    session.add(room)
    await session.commit()
    await session.refresh(room)
    return room


@router.post(
    "/projects/{project_id}/assets/upload-url", response_model=UploadURLResponse, status_code=201
)
async def create_upload_url(
    project_id: UUID,
    payload: UploadURLRequest,
    request: Request,
    session: Session,
    user: User,
    settings: Config,
) -> UploadURLResponse:
    await require_project_access(session, project_id, user["id"])
    if payload.size_bytes > settings.max_upload_bytes:
        raise AppError("file_too_large", "Upload exceeds the configured size limit", 413)
    if payload.room_id is not None:
        room = await session.scalar(
            select(Room).where(Room.id == payload.room_id, Room.project_id == project_id)
        )
        if room is None:
            raise AppError("not_found", "Room not found", 404)

    asset_id = uuid4()
    suffix = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}[payload.mime_type]
    storage_path = f"{project_id}/{payload.room_id or 'unassigned'}/{asset_id}{suffix}"
    asset = Asset(
        id=asset_id,
        project_id=project_id,
        room_id=payload.room_id,
        owner_id=user["id"],
        storage_path=storage_path,
        mime_type=payload.mime_type,
        size_bytes=payload.size_bytes,
    )
    session.add(asset)
    await session.commit()

    if settings.supabase_url and settings.supabase_service_role_key:
        encoded_path = quote(storage_path, safe="/")
        storage_base = f"{settings.supabase_url.rstrip('/')}/storage/v1/object/upload/sign"
        endpoint = f"{storage_base}/{settings.supabase_storage_bucket}/{encoded_path}"
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    endpoint,
                    headers={
                        "apikey": settings.supabase_service_role_key,
                        "Authorization": f"Bearer {settings.supabase_service_role_key}",
                        "Content-Type": "application/json",
                    },
                    json={"contentType": payload.mime_type},
                )
                response.raise_for_status()
            signed_path = response.json().get("url") or response.json().get("signedURL")
            if not signed_path:
                raise ValueError("missing signed URL")
            if signed_path.startswith("http"):
                signed_url = signed_path
            else:
                suffix = signed_path if signed_path.startswith("/") else f"/{signed_path}"
                signed_url = f"{settings.supabase_url.rstrip('/')}/storage/v1{suffix}"
            return UploadURLResponse(
                asset_id=asset_id,
                upload_url=signed_url,
                headers={"Content-Type": payload.mime_type},
            )
        except (httpx.HTTPError, ValueError) as exc:
            raise ProviderUnavailable("Supabase Storage signed upload") from exc
    if settings.supabase_configured:
        raise ProviderUnavailable("Supabase Storage (service-role key missing)")

    signature = hmac.new(
        request.app.state.upload_signing_key, str(asset_id).encode(), hashlib.sha256
    ).hexdigest()
    return UploadURLResponse(
        asset_id=asset_id,
        upload_url=f"/api/v1/assets/{asset_id}/content",
        headers={"Content-Type": payload.mime_type, "x-maya-upload-token": signature},
    )


@router.put("/assets/{asset_id}/content", status_code=204)
async def local_upload(
    asset_id: UUID,
    request: Request,
    token: Annotated[str, Header(alias="x-maya-upload-token", min_length=64, max_length=64)],
    session: Session,
    settings: Config,
) -> None:
    if settings.supabase_configured:
        raise AppError("not_found", "Local upload endpoint is disabled", 404)
    expected = hmac.new(
        request.app.state.upload_signing_key, str(asset_id).encode(), hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected, token):
        raise AppError("invalid_upload_token", "Upload URL is invalid or expired", 403)
    asset = await session.get(Asset, asset_id)
    if asset is None:
        raise AppError("not_found", "Asset not found", 404)
    if request.headers.get("content-type", "").split(";")[0] != asset.mime_type:
        raise AppError(
            "invalid_file_type", "Uploaded content type differs from the signed request", 415
        )
    suffix = Path(asset.storage_path).suffix
    safe_id = re.sub(r"[^a-f0-9-]", "", str(asset_id))
    target = Path(settings.upload_dir) / f"{safe_id}{suffix}"
    target.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    prefix = bytearray()
    with target.open("wb") as output:
        async for chunk in request.stream():
            total += len(chunk)
            if total > settings.max_upload_bytes or total > asset.size_bytes:
                target.unlink(missing_ok=True)
                raise AppError("file_too_large", "Upload exceeds its signed size limit", 413)
            if len(prefix) < 12:
                prefix.extend(chunk[: 12 - len(prefix)])
            output.write(chunk)
    valid_signature = (
        (asset.mime_type == "image/jpeg" and prefix.startswith(b"\xff\xd8\xff"))
        or (asset.mime_type == "image/png" and prefix.startswith(b"\x89PNG\r\n\x1a\n"))
        or (
            asset.mime_type == "image/webp"
            and prefix.startswith(b"RIFF")
            and prefix[8:12] == b"WEBP"
        )
    )
    if not valid_signature:
        target.unlink(missing_ok=True)
        raise AppError("invalid_file_content", "File bytes do not match an allowed image type", 415)
    asset.size_bytes = total
    await session.commit()
