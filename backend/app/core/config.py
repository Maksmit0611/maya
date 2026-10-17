from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    app_name: str = "MAYA AI"
    environment: str = "development"
    database_url: str = "sqlite+aiosqlite:///./maya.db"
    supabase_url: str | None = None
    supabase_service_role_key: str | None = None
    supabase_jwt_secret: str | None = None
    supabase_storage_bucket: str = "maya-assets"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.8-flash"
    comfyui_base_url: str | None = None
    comfyui_api_token: str | None = None
    hf_token: str | None = None
    dev_auth_enabled: bool = True
    upload_dir: str = "./uploads"
    max_upload_bytes: int = 20_000_000
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def supabase_configured(self) -> bool:
        return bool(self.supabase_url)


@lru_cache
def get_settings() -> Settings:
    return Settings()
