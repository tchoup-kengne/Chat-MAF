import pytest

from chat_maf.config import load_settings


def test_load_settings_requires_endpoint(monkeypatch):
    monkeypatch.delenv("AZURE_OPENAI_ENDPOINT", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_CHAT_MODEL", raising=False)

    with pytest.raises(ValueError, match="AZURE_OPENAI_ENDPOINT"):
        load_settings()


def test_load_settings_reads_environment(monkeypatch):
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://example.openai.azure.com")
    monkeypatch.setenv("AZURE_OPENAI_CHAT_MODEL", "chat")
    monkeypatch.setenv("AZURE_OPENAI_API_VERSION", "2025-04-01-preview")
    monkeypatch.setenv("CHAT_MAF_MESSAGE", "Hello")

    settings = load_settings()

    assert settings.azure_endpoint.endswith(".openai.azure.com")
    assert settings.chat_model == "chat"
    assert settings.api_version == "2025-04-01-preview"
    assert settings.one_shot_message == "Hello"
