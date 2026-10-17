from app.core.config import Settings
from app.providers.chat.gemini import GeminiChatProvider
from app.providers.chat.mock import MockChatProvider
from app.providers.media.comfyui import ComfyUIProvider
from app.providers.media.mock import MockMediaProvider


def chat_provider(settings: Settings):
    if settings.gemini_api_key:
        return GeminiChatProvider(settings.gemini_api_key, settings.gemini_model)
    return MockChatProvider()


def media_provider(settings: Settings):
    if settings.comfyui_base_url:
        return ComfyUIProvider(settings.comfyui_base_url, settings.comfyui_api_token)
    return MockMediaProvider()
