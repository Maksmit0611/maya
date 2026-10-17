from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ErrorEnvelope(BaseModel):
    code: str
    message: str
    details: Any = None
    request_id: str


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=180)


class ProjectRead(ORMModel):
    id: UUID
    owner_id: str
    name: str
    created_at: datetime


class RoomCreate(BaseModel):
    name: str = Field(min_length=1, max_length=180)
    room_type: str = Field(default="living room", max_length=80)
    dimensions: dict[str, Any] = Field(default_factory=dict)


class RoomRead(ORMModel):
    id: UUID
    project_id: UUID
    name: str
    room_type: str
    dimensions: dict[str, Any]
    created_at: datetime


class BriefCreate(BaseModel):
    room_id: UUID | None = None
    content: dict[str, Any]


class BriefRead(ORMModel):
    id: UUID
    project_id: UUID
    room_id: UUID | None
    version: int
    content: dict[str, Any]
    created_at: datetime


class PaletteColor(BaseModel):
    name: str = Field(min_length=1, max_length=60, description="Human-readable color name")
    hex: str = Field(
        pattern=r"^#[0-9A-Fa-f]{6}$", description="Six-digit RGB hexadecimal color"
    )
    role: str = Field(min_length=1, max_length=120, description="Where or how this color is used")


class DesignPlan(BaseModel):
    style: str = Field(min_length=1, max_length=120, description="Concise interior design style")
    palette: list[PaletteColor] = Field(
        min_length=3, max_length=6, description="Three to six coordinated colors"
    )
    camera_moves: list[str] = Field(
        min_length=1, max_length=4, description="Simple camera moves for the visualisation"
    )
    scene_beats: list[str] = Field(
        min_length=3, max_length=6, description="Visual sequence for the concept reveal"
    )
    narration: str = Field(min_length=1, max_length=600, description="One to three short sentences")
    constraints: list[str] = Field(
        min_length=1,
        max_length=8,
        description="Known constraints, assumptions, and safety or verification notes",
    )


class ChatRequest(BaseModel):
    project_id: UUID
    brief: dict[str, Any]
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    plan: DesignPlan
    provider: str


class JobCreate(BaseModel):
    project_id: UUID
    room_id: UUID | None = None
    brief: dict[str, Any]


class JobRead(ORMModel):
    id: UUID
    project_id: UUID
    status: str
    cancellation_requested: bool
    provenance: dict[str, Any]
    error_json: dict[str, Any] | None
    created_at: datetime


class ResultRead(ORMModel):
    id: UUID
    job_id: UUID
    output_json: dict[str, Any]
    selected_by: str | None
    selected_at: datetime | None
    created_at: datetime


class SelectResult(BaseModel):
    selected: bool = True


class UploadURLResponse(BaseModel):
    asset_id: UUID
    upload_url: str
    method: Literal["PUT"] = "PUT"
    headers: dict[str, str] = Field(default_factory=dict)


class UploadURLRequest(BaseModel):
    room_id: UUID | None = None
    filename: str = Field(min_length=1, max_length=255)
    mime_type: str = Field(pattern=r"^image/(jpeg|png|webp)$")
    size_bytes: int = Field(gt=0, le=20_000_000)
