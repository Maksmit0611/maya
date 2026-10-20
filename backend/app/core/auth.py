from functools import lru_cache
from typing import Annotated, Any

import httpx
import jwt
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import Settings, get_settings
from app.core.errors import AppError

bearer = HTTPBearer(auto_error=False)


@lru_cache(maxsize=16)
def _jwks_url(supabase_url: str) -> str:
    return f"{supabase_url.rstrip('/')}/auth/v1/.well-known/jwks.json"


async def _verify_supabase_token(token: str, settings: Settings) -> dict[str, Any]:
    if settings.supabase_jwt_secret:
        try:
            return jwt.decode(
                token, settings.supabase_jwt_secret, algorithms=["HS256"], audience="authenticated"
            )
        except jwt.PyJWTError as exc:
            raise AppError("invalid_token", "The bearer token is invalid", 401) from exc

    if not settings.supabase_url:
        raise AppError("auth_unavailable", "Supabase authentication is not configured", 503)
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(_jwks_url(settings.supabase_url))
            response.raise_for_status()
            keys = response.json().get("keys", [])
        header = jwt.get_unverified_header(token)
        matching = next((key for key in keys if key.get("kid") == header.get("kid")), None)
        if matching is None:
            raise AppError("invalid_token", "The bearer token signing key is unknown", 401)
        algorithms = {"EC": "ES256", "RSA": "RS256", "OKP": "EdDSA"}
        expected_algorithm = matching.get("alg") or algorithms.get(matching.get("kty"))
        if not expected_algorithm or header.get("alg") != expected_algorithm:
            raise AppError("invalid_token", "The bearer token algorithm is not allowed", 401)
        signing_key = jwt.PyJWK.from_dict(matching).key
        return jwt.decode(
            token, signing_key, algorithms=[expected_algorithm], audience="authenticated"
        )
    except AppError:
        raise
    except (httpx.HTTPError, ValueError, jwt.PyJWTError) as exc:
        raise AppError("invalid_token", "The bearer token could not be verified", 401) from exc


async def get_current_user(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> dict[str, str]:
    if credentials is None:
        if settings.dev_auth_allowed:
            request.state.auth_mode = "dev-user (LOCAL/TEST ONLY)"
            return {"id": "dev-user", "email": "dev-user@local.invalid"}
        if settings.is_production and not settings.supabase_configured:
            raise AppError(
                "auth_unavailable",
                "Supabase authentication must be configured in production",
                503,
            )
        raise AppError("unauthorized", "A bearer token is required", 401)
    claims = await _verify_supabase_token(credentials.credentials, settings)
    subject = claims.get("sub")
    if not isinstance(subject, str) or not subject:
        raise AppError("invalid_token", "The bearer token has no user subject", 401)
    return {"id": subject, "email": str(claims.get("email", ""))}
