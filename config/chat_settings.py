import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ChatSettings:
    provider: str = os.getenv("ANNA_CHAT_PROVIDER", "mock")
    model: str = os.getenv("ANNA_CHAT_MODEL", "mock-foundation-v1")


def load_chat_settings() -> ChatSettings:
    return ChatSettings()
