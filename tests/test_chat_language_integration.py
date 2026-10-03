import unittest
import tempfile
from pathlib import Path

from chat.models import ChatMessage, ChatRequest, ChatResponse
from chat.service import ChatService
from language.models import Language, LanguagePreference
from memory.manager import MemoryManager
from memory.store import MemoryStore


class RecordingProvider:

    provider_name = "recording"
    model_name = "language-test"

    def __init__(self):
        self.requests = []

    def generate(self, request: ChatRequest) -> ChatResponse:
        self.requests.append(request)
        return ChatResponse(
            message=ChatMessage(
                role="assistant",
                content="recorded",
            ),
            provider=self.provider_name,
            model=self.model_name,
        )


class TestChatLanguageIntegration(unittest.TestCase):

    def setUp(self):
        self.provider = RecordingProvider()

    def _system_messages(self):
        return [
            message
            for message in self.provider.requests[-1].messages
            if message.role == "system"
        ]

    def test_explicit_language_request_controls_chat(self):
        service = ChatService(provider=self.provider)

        service.respond(
            "Please explain this in Malayalam."
        )

        system_text = "\n".join(
            message.content
            for message in self._system_messages()
        )

        self.assertIn(
            "response_language=malayalam",
            system_text,
        )
        self.assertIn(
            "language_source=explicit",
            system_text,
        )

    def test_current_manglish_controls_chat(self):
        service = ChatService(provider=self.provider)

        service.respond(
            "Anna ithu simple ayi explain cheyyu"
        )

        system_text = "\n".join(
            message.content
            for message in self._system_messages()
        )

        self.assertIn(
            "response_language=manglish",
            system_text,
        )

    def test_language_preference_is_used_when_input_is_unknown(self):
        service = ChatService(
            provider=self.provider,
            language_preference=LanguagePreference(
                preferred_language=Language.MALAYALAM,
            ),
        )

        service.respond("?")

        system_text = "\n".join(
            message.content
            for message in self._system_messages()
        )

        self.assertIn(
            "response_language=malayalam",
            system_text,
        )
        self.assertIn(
            "language_source=user_preference",
            system_text,
        )

    def test_previous_response_language_is_carried_forward(self):
        service = ChatService(provider=self.provider)

        service.respond(
            "Please reply in Malayalam."
        )

        service.respond("?")

        system_text = "\n".join(
            message.content
            for message in self._system_messages()
        )

        self.assertIn(
            "response_language=malayalam",
            system_text,
        )
        self.assertIn(
            "language_source=context",
            system_text,
        )


if __name__ == "__main__":
    unittest.main()
