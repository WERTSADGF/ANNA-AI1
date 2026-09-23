from typing import Protocol

from chat.models import ChatRequest, ChatResponse, ChatMessage


class ChatModelProvider(Protocol):

    @property
    def provider_name(self) -> str:
        ...

    @property
    def model_name(self) -> str:
        ...

    def generate(self, request: ChatRequest) -> ChatResponse:
        ...


class MockModelProvider:
    """
    Deterministic provider used for foundation testing.

    This is intentionally not a real AI provider.
    A real provider can be added later through the same interface.
    """

    @property
    def provider_name(self) -> str:
        return "mock"

    @property
    def model_name(self) -> str:
        return "mock-foundation-v1"

    def generate(self, request: ChatRequest) -> ChatResponse:

        user_messages = [
            message
            for message in request.messages
            if message.role == "user"
        ]

        if not user_messages:
            content = "No user message was provided."
        else:
            content = (
                "ANNA chat foundation received: "
                + user_messages[-1].content
            )

        return ChatResponse(
            message=ChatMessage(
                role="assistant",
                content=content,
            ),
            provider=self.provider_name,
            model=self.model_name,
        )
