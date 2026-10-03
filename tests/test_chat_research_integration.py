import unittest

from chat.models import ChatMessage, ChatRequest, ChatResponse
from chat.service import ChatService
from research.engine import ResearchEngine
from research.models import ResearchMode
from research.providers import MockSourceProvider


class RecordingProvider:

    provider_name = "recording"
    model_name = "research-test"

    def __init__(self):
        self.requests = []

    def generate(self, request: ChatRequest) -> ChatResponse:
        self.requests.append(request)

        return ChatResponse(
            message=ChatMessage(
                role="assistant",
                content="research recorded",
            ),
            provider=self.provider_name,
            model=self.model_name,
        )


class TestChatResearchIntegration(unittest.TestCase):

    def setUp(self):
        self.provider = RecordingProvider()
        self.research = ResearchEngine(
            provider=MockSourceProvider()
        )

    def test_normal_research_sends_collected_sources(self):
        service = ChatService(
            provider=self.provider,
            research=self.research,
        )

        response = service.research(
            "Explain Python.",
            mode=ResearchMode.NORMAL,
        )

        self.assertEqual(
            response.message.role,
            "assistant",
        )

        messages = self.provider.requests[-1].messages

        research_context = [
            message
            for message in messages
            if message.role == "system"
            and "ANNA research context:" in message.content
        ]

        source_context = [
            message
            for message in messages
            if message.role == "system"
            and "ANNA research source:" in message.content
        ]

        self.assertEqual(len(research_context), 1)
        self.assertEqual(len(source_context), 2)
        self.assertTrue(
            all(
                "accessed=True" in message.content
                for message in source_context
            )
        )

    def test_research_requires_engine(self):
        service = ChatService(
            provider=self.provider,
        )

        with self.assertRaises(RuntimeError):
            service.research("Explain Python.")


if __name__ == "__main__":
    unittest.main()
