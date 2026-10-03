import unittest

from chat.models import ChatMessage, ChatRequest, ChatResponse
from chat.service import ChatService


class RecordingProvider:
    @property
    def provider_name(self) -> str:
        return "recording"

    @property
    def model_name(self) -> str:
        return "recording-test"

    def __init__(self):
        self.requests = []

    def generate(self, request: ChatRequest) -> ChatResponse:
        self.requests.append(request)

        return ChatResponse(
            message=ChatMessage(
                role="assistant",
                content="recorded response",
            ),
            provider=self.provider_name,
            model=self.model_name,
        )


class TestChatPhase2Integration(unittest.TestCase):

    def test_session_is_created_and_retains_messages(self):
        provider = RecordingProvider()
        service = ChatService(provider)

        service.respond("My name is Alex.")
        service.respond("What is my name?")

        history = service.session.history()

        self.assertEqual(len(history), 4)
        self.assertEqual(history[0].role, "user")
        self.assertEqual(history[0].content, "My name is Alex.")
        self.assertEqual(history[1].role, "assistant")
        self.assertEqual(history[1].content, "recorded response")
        self.assertEqual(history[2].role, "user")
        self.assertEqual(history[2].content, "What is my name?")
        self.assertEqual(history[3].role, "assistant")
        self.assertEqual(history[3].content, "recorded response")

    def test_companion_guidance_is_sent_as_system_context(self):
        provider = RecordingProvider()
        service = ChatService(provider)

        service.respond("Anna innu entha cheyyanam")

        request = provider.requests[0]

        system_messages = [
            message
            for message in request.messages
            if message.role == "system"
        ]

        self.assertEqual(len(system_messages), 1)
        self.assertIn("ANNA companion guidance:", system_messages[0].content)
        self.assertIn("response_language=manglish", system_messages[0].content)
        self.assertIn("tone=warm-natural", system_messages[0].content)
        self.assertIn("style=natural-conversational", system_messages[0].content)

    def test_session_history_is_used_when_previous_messages_are_not_supplied(self):
        provider = RecordingProvider()
        service = ChatService(provider)

        service.respond("My name is Alex.")
        service.respond("What is my name?")

        request = provider.requests[1]

        self.assertEqual(request.messages[1].content, "My name is Alex.")
        self.assertEqual(request.messages[2].content, "recorded response")
        self.assertEqual(request.messages[3].content, "What is my name?")

    def test_explicit_previous_messages_override_session_history(self):
        provider = RecordingProvider()
        service = ChatService(provider)

        service.respond("Stored session message.")

        previous = (
            ChatMessage(
                role="user",
                content="Caller supplied message.",
            ),
            ChatMessage(
                role="assistant",
                content="Caller supplied response.",
            ),
        )

        service.respond(
            "Current question.",
            previous_messages=previous,
        )

        request = provider.requests[1]

        self.assertEqual(request.messages[1].content, "Caller supplied message.")
        self.assertEqual(request.messages[2].content, "Caller supplied response.")
        self.assertEqual(request.messages[3].content, "Current question.")
        self.assertNotIn(
            "Stored session message.",
            [message.content for message in request.messages],
        )


if __name__ == "__main__":
    unittest.main()
