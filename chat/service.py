from chat.models import ChatMessage, ChatRequest, ChatResponse
from chat.providers import ChatModelProvider
from companion.engine import CompanionEngine


class ChatService:

    def __init__(
        self,
        provider: ChatModelProvider,
        companion: CompanionEngine | None = None,
    ):
        self.provider = provider
        self.companion = companion or CompanionEngine()

    def respond(
        self,
        user_text: str,
        previous_messages: tuple[ChatMessage, ...] = (),
    ) -> ChatResponse:

        cleaned_text = user_text.strip()

        if not cleaned_text:
            raise ValueError("User message cannot be empty.")

        # Build companion context before sending the conversation
        # through the model-provider abstraction.
        self.companion.build_context(cleaned_text)

        messages = previous_messages + (
            ChatMessage(
                role="user",
                content=cleaned_text,
            ),
        )

        request = ChatRequest(messages=messages)

        return self.provider.generate(request)
