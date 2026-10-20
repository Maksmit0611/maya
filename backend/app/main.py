import logging
import secrets
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import api_router
from app.core.config import Settings, get_settings
from app.core.db import make_session_factory
from app.core.errors import AppError
from app.models import Base

logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved = settings or get_settings()
    if resolved.is_production and not resolved.supabase_configured:
        raise ValueError("Supabase authentication must be configured when ENVIRONMENT=production")
    engine, session_factory = make_session_factory(resolved.database_url)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.engine = engine
        app.state.session_factory = session_factory
        app.state.upload_signing_key = secrets.token_bytes(32)
        if resolved.database_url.startswith("sqlite") and resolved.environment != "production":
            async with engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)
        yield
        await engine.dispose()

    app = FastAPI(title="MAYA AI API", version="1.0.0", lifespan=lifespan)
    app.dependency_overrides[get_settings] = lambda: resolved
    app.state.engine = engine
    app.state.session_factory = session_factory
    app.state.upload_signing_key = secrets.token_bytes(32)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved.cors_origin_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "Idempotency-Key", "x-maya-upload-token"],
    )

    @app.middleware("http")
    async def request_id_middleware(request: Request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        return response

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
                "request_id": getattr(request.state, "request_id", "unknown"),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        safe_details = [
            {"loc": item.get("loc"), "msg": item.get("msg"), "type": item.get("type")}
            for item in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content={
                "code": "validation_error",
                "message": "Request validation failed",
                "details": safe_details,
                "request_id": getattr(request.state, "request_id", "unknown"),
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_error_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": "http_error",
                "message": str(exc.detail),
                "details": None,
                "request_id": getattr(request.state, "request_id", "unknown"),
            },
            headers=exc.headers,
        )

    @app.exception_handler(Exception)
    async def unexpected_error_handler(request: Request, exc: Exception):
        logger.error(
            "Unhandled API error request_id=%s error_type=%s",
            getattr(request.state, "request_id", "unknown"),
            type(exc).__name__,
        )
        return JSONResponse(
            status_code=500,
            content={
                "code": "internal_error",
                "message": "An unexpected error occurred",
                "details": None,
                "request_id": getattr(request.state, "request_id", "unknown"),
            },
        )

    @app.get("/healthz", tags=["health"])
    async def healthz():
        return {
            "status": "ok",
            "auth_mode": (
                "supabase"
                if resolved.supabase_configured
                else "dev-user (LOCAL/TEST ONLY)"
                if resolved.dev_auth_allowed
                else "disabled"
            ),
        }

    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
