from typing import Any


class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400, details: Any = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class ProviderUnavailable(AppError):
    def __init__(self, provider: str):
        super().__init__("provider_unavailable", f"{provider} is not configured or available", 503)
