from dataclasses import dataclass, field

from chat.models import ChatMessage


@dataclass
class ChatSession:
    """
    Short-lived conversation state for the current chat session.

    This is intentionally separate from persistent ANNA memory.
    """

    messages: list[ChatMessage] = field(default_factory=list)

    def add_message(self, message: ChatMessage) -> None:
        self.messages.append(message)

    def history(self) -> tuple[ChatMessage, ...]:
        return tuple(self.messages)

    def clear(self) -> None:
        self.messages.clear()
