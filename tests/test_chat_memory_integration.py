import tempfile
import unittest
from pathlib import Path

from chat.models import ChatRequest, ChatResponse, ChatMessage
from chat.service import ChatService
from memory.manager import MemoryManager
from memory.models import MemoryType
from memory.store import MemoryStore


class RecordingProvider:
    @property
    def provider_name(self) -> str:
        return "recording"

    @property
    def model_name(self) -> str:
        return "recording-memory-test"

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


class TestChatMemoryIntegration(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        store_path = Path(self.temp_dir.name) / "memory.json"

        self.memory = MemoryManager(
            MemoryStore(str(store_path))
        )

        self.memory.store_memory(
            content="The owner prefers Python examples.",
            memory_type=MemoryType.PERSONAL,
            source="conversation",
            confidence=0.95,
            importance=0.85,
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_relevant_memory_is_sent_as_context(self):
        provider = RecordingProvider()

        service = ChatService(
            provider=provider,
            memory=self.memory,
        )

        service.respond("Please use Python examples.")

        request = provider.requests[0]

        memory_messages = [
            message
            for message in request.messages
            if message.role == "system"
            and "ANNA memory context:" in message.content
        ]

        self.assertEqual(len(memory_messages), 1)
        self.assertIn(
            "The owner prefers Python examples.",
            memory_messages[0].content,
        )

    def test_unrelated_memory_is_not_sent(self):
        provider = RecordingProvider()

        service = ChatService(
            provider=provider,
            memory=self.memory,
        )

        service.respond("What is the weather?")

        memory_messages = [
            message
            for message in provider.requests[0].messages
            if message.role == "system"
            and "ANNA memory context:" in message.content
        ]

        self.assertEqual(memory_messages, [])

    def test_chat_does_not_automatically_store_user_message(self):
        provider = RecordingProvider()

        service = ChatService(
            provider=provider,
            memory=self.memory,
        )

        service.respond("This should remain session-only.")

        results = self.memory.retrieve(
            query="This should remain session-only.",
        )

        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
