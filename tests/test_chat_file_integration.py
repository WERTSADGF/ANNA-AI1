import tempfile
import unittest
from pathlib import Path

from chat.models import ChatRequest, ChatResponse, ChatMessage
from chat.service import ChatService
from files.authorization import FileAuthorizer
from files.service import FileService


class RecordingProvider:

    provider_name = "recording"
    model_name = "file-test"

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


class TestChatFileIntegration(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        self.authorizer = FileAuthorizer([
            str(self.root)
        ])

        self.files = FileService(
            authorizer=self.authorizer
        )

        self.provider = RecordingProvider()

    def tearDown(self):
        self.temp_dir.cleanup()

    def _file_context(self):
        return [
            message
            for message in self.provider.requests[-1].messages
            if message.role == "system"
            and "ANNA file context:" in message.content
        ]

    def test_relevant_file_is_sent_as_context(self):
        file_path = self.root / "python.txt"

        file_path.write_text(
            "Python variables store references to values.\n"
            "Variables can be reassigned during execution.",
            encoding="utf-8",
        )

        service = ChatService(
            provider=self.provider,
            files=self.files,
        )

        service.ingest_file(str(file_path))
        service.respond("Explain Python variables.")

        contexts = self._file_context()

        self.assertEqual(len(contexts), 1)
        self.assertIn(
            "Python variables store references to values.",
            contexts[0].content,
        )

    def test_unrelated_file_is_not_sent(self):
        file_path = self.root / "python.txt"

        file_path.write_text(
            "Python variables store references to values.",
            encoding="utf-8",
        )

        service = ChatService(
            provider=self.provider,
            files=self.files,
        )

        service.ingest_file(str(file_path))
        service.respond("What is the weather today?")

        self.assertEqual(
            self._file_context(),
            [],
        )

    def test_file_ingestion_respects_authorization(self):
        authorized = self.root / "authorized.txt"
        authorized.write_text(
            "Authorized ANNA note.",
            encoding="utf-8",
        )

        service = ChatService(
            provider=self.provider,
            files=self.files,
        )

        service.ingest_file(str(authorized))

        outside_dir = Path(tempfile.gettempdir())
        outside = outside_dir / "anna_outside_test.txt"

        try:
            outside.write_text(
                "This must not be indexed.",
                encoding="utf-8",
            )

            with self.assertRaises(PermissionError):
                service.ingest_file(str(outside))
        finally:
            if outside.exists():
                outside.unlink()


if __name__ == "__main__":
    unittest.main()
