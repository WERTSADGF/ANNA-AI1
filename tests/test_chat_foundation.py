import unittest

from chat.models import ChatMessage, ChatRequest
from chat.providers import MockModelProvider
from chat.service import ChatService
from core.model_router import ModelRouter


class TestChatFoundation(unittest.TestCase):

    def test_message_model(self):
        message = ChatMessage(
            role="user",
            content="Hello Anna",
        )

        self.assertEqual(message.role, "user")
        self.assertEqual(message.content, "Hello Anna")

    def test_mock_provider(self):
        provider = MockModelProvider()

        request = ChatRequest(
            messages=(
                ChatMessage(
                    role="user",
                    content="Hello Anna",
                ),
            )
        )

        response = provider.generate(request)

        self.assertEqual(response.provider, "mock")
        self.assertEqual(response.model, "mock-foundation-v1")
        self.assertEqual(response.message.role, "assistant")
        self.assertIn("Hello Anna", response.message.content)

    def test_chat_service(self):
        service = ChatService(MockModelProvider())

        response = service.respond("Teach me Python.")

        self.assertEqual(response.message.role, "assistant")
        self.assertIn("Teach me Python.", response.message.content)

    def test_empty_message_rejected(self):
        service = ChatService(MockModelProvider())

        with self.assertRaises(ValueError):
            service.respond("   ")

    def test_previous_context_is_preserved(self):
        service = ChatService(MockModelProvider())

        previous = (
            ChatMessage(
                role="user",
                content="My name is Alex.",
            ),
            ChatMessage(
                role="assistant",
                content="Nice to meet you.",
            ),
        )

        response = service.respond(
            "What did I say?",
            previous_messages=previous,
        )

        self.assertIn("What did I say?", response.message.content)

    def test_model_router(self):
        router = ModelRouter()

        provider = router.get_chat_provider("mock")

        self.assertEqual(provider.provider_name, "mock")

    def test_unknown_provider_rejected(self):
        router = ModelRouter()

        with self.assertRaises(ValueError):
            router.get_chat_provider("unknown-provider")


if __name__ == "__main__":
    unittest.main()
