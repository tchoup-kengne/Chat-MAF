import asyncio

from .agent import create_agent
from .config import load_settings


async def stream_message(agent, session, message: str) -> None:
    print("Assistant: ", end="", flush=True)
    stream = agent.run(message, stream=True, session=session)
    async for update in stream:
        if update.text:
            print(update.text, end="", flush=True)
    print()


async def chat() -> None:
    settings = load_settings()
    agent = create_agent(settings)
    session = agent.create_session()

    try:
        if settings.one_shot_message:
            await stream_message(agent, session, settings.one_shot_message)
            return

        print("Chat-MAF is ready. Type 'exit', 'quit', or 'q' to stop.")
        while True:
            try:
                message = await asyncio.to_thread(input, "You: ")
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not message.strip():
                continue
            if message.strip().lower() in {"exit", "quit", "q"}:
                break
            if message.strip().lower() == "clear":
                session = agent.create_session()
                print("Conversation cleared.")
                continue

            await stream_message(agent, session, message)
    finally:
        await agent.close()


def main() -> None:
    asyncio.run(chat())


if __name__ == "__main__":
    main()
