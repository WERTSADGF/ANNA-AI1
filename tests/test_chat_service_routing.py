import unittest

from chat.models import ChatRequest, ChatResponse, ChatMessage
from chat.service import ChatService
from config.chat_settings import ChatSettings
from core.model_router import ModelRouter


class RecordingProvider:
    @property
    def provider_name(self) -> str:
        return "recording"

    @property
    def model_name(self) -> str:
        return "recording-test"

    def generate(self, request: ChatRequest) -> ChatResponse:
        return ChatResponse(
            message=ChatMessage(
                role="assistant",
                content="recorded response",
            ),
            provider=self.provider_name,
            model=self.model_name,
        )


class TestChatServiceRouting(unittest.TestCase):

    def test_service_can_use_router_when_provider_is_not_injected(self):
        settings = ChatSettings(
            provider="mock",
            model="mock-foundation-v1",
        )
        router = ModelRouter(settings=settings)

        service = ChatService(router=router)

        response = service.respond("Hello Anna.")

        self.assertEqual(response.provider, "mock")
        self.assertEqual(response.model, "mock-foundation-v1")

    def test_explicit_provider_still_overrides_router(self):
        settings = ChatSettings(
            provider="mock",
            model="mock-foundation-v1",
        )
        router = ModelRouter(settings=settings)

        provider = RecordingProvider()
        service = ChatService(
            provider=provider,
            router=router,
        )

        response = service.respond("Hello Anna.")

        self.assertEqual(response.provider, "recording")
        self.assertEqual(response.model, "recording-test")


if __name__ == "__main__":
    unittest.main()
