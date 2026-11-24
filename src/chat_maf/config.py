from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    azure_endpoint: str
    chat_model: str
    api_version: str | None
    api_key: str | None
    one_shot_message: str | None


def load_settings() -> Settings:
    load_dotenv()

    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip()
    chat_model = os.getenv("AZURE_OPENAI_CHAT_MODEL", "").strip()
    if not azure_endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINT is required")
    if not chat_model:
        raise ValueError("AZURE_OPENAI_CHAT_MODEL is required")

    api_key = os.getenv("AZURE_OPENAI_API_KEY", "").strip() or None
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "").strip() or None
    one_shot_message = os.getenv("CHAT_MAF_MESSAGE", "").strip() or None

    return Settings(
        azure_endpoint=azure_endpoint,
        chat_model=chat_model,
        api_version=api_version,
        api_key=api_key,
        one_shot_message=one_shot_message,
    )
