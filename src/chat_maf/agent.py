from azure.identity import DefaultAzureCredential
from agent_framework import Agent, InMemoryHistoryProvider
from agent_framework.openai import OpenAIChatClient

from .config import Settings
from .tools import get_current_time


def create_agent(settings: Settings) -> Agent:
    client_kwargs: dict[str, object] = {
        "model": settings.chat_model,
        "azure_endpoint": settings.azure_endpoint,
    }
    if settings.api_key:
        client_kwargs["api_key"] = settings.api_key
    else:
        client_kwargs["credential"] = DefaultAzureCredential()
    if settings.api_version:
        client_kwargs["api_version"] = settings.api_version

    client = OpenAIChatClient(**client_kwargs)
    return Agent(
        client,
        name="ChatMAF",
        instructions=(
            "You are a helpful assistant. Be concise and clear. "
            "Use the get_current_time tool when the user asks about the current time."
        ),
        tools=[get_current_time],
        context_providers=[InMemoryHistoryProvider()],
    )
