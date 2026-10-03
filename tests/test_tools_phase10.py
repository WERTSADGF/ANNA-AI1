import tempfile
import unittest
from pathlib import Path

from chat.models import ChatMessage, ChatResponse
from chat.service import ChatService
from security.permissions import PermissionLevel
from tools.models import ToolActionType
from tools.service import ToolService


class RecordingProvider:

    def generate(self, request):
        return ChatResponse(
            message=ChatMessage(
                role="assistant",
                content="tool test response",
            ),
            provider="recording",
            model="test-model",
        )


class TestToolService(unittest.TestCase):

    def make_service(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)

        return ToolService(
            project_root=Path(directory.name)
        )

    def test_system_info_is_read_only(self):
        service = self.make_service()

        result = service.system_info()

        self.assertTrue(result.success)
        self.assertTrue(result.verified)
        self.assertTrue(result.executed)
        self.assertEqual(
            result.action.permission_level,
            PermissionLevel.READ_ONLY,
        )

    def test_python_inspection_is_read_only(self):
        service = self.make_service()

        path = (
            service.project_root
            / "sample.py"
        )

        path.write_text(
            "import os\nprint('hello')\n",
            encoding="utf-8",
        )

        result = service.inspect_python(
            "sample.py"
        )

        self.assertTrue(result.success)
        self.assertTrue(result.verified)
        self.assertIn(
            "Syntax: valid",
            result.output,
        )
        self.assertEqual(
            result.action.action_type,
            ToolActionType.CODE_INSPECTION,
        )

    def test_python_inspection_detects_syntax_error(self):
        service = self.make_service()

        path = (
            service.project_root
            / "broken.py"
        )

        path.write_text(
            "def broken(:\n",
            encoding="utf-8",
        )

        result = service.inspect_python(
            "broken.py"
        )

        self.assertFalse(result.success)
        self.assertTrue(result.verified)
        self.assertEqual(
            result.return_code,
            1,
        )

    def test_path_outside_project_is_rejected(self):
        service = self.make_service()

        with self.assertRaises(PermissionError):
            service.list_directory(
                str(
                    Path(service.project_root).parent
                )
            )

    def test_run_tests_supports_dry_run(self):
        service = self.make_service()

        result = service.run_tests(
            dry_run=True
        )

        self.assertTrue(result.success)
        self.assertFalse(result.executed)
        self.assertFalse(result.verified)
        self.assertIn(
            "DRY-RUN",
            result.output,
        )

    def test_directory_creation_supports_dry_run(self):
        service = self.make_service()

        result = service.create_directory(
            "safe-zone",
            dry_run=True,
        )

        self.assertTrue(result.success)
        self.assertFalse(result.executed)
        self.assertFalse(
            (service.project_root / "safe-zone").exists()
        )

    def test_application_launch_is_allowlisted(self):
        service = self.make_service()

        result = service.launch_application(
            "notepad",
            dry_run=True,
        )

        self.assertTrue(result.success)
        self.assertFalse(result.executed)
        self.assertEqual(
            result.action.action_type,
            ToolActionType.LAUNCH_APPLICATION,
        )

    def test_application_launch_requires_confirmation(self):
        service = self.make_service()

        with self.assertRaises(PermissionError):
            service.launch_application(
                "notepad",
                dry_run=False,
                confirmed=False,
            )


class TestChatToolIntegration(unittest.TestCase):

    def test_chat_service_has_tool_service(self):
        service = ChatService(
            provider=RecordingProvider()
        )

        self.assertIsInstance(
            service.tool_service,
            ToolService,
        )

    def test_chat_service_exposes_tool_operations(self):
        service = ChatService(
            provider=RecordingProvider()
        )

        result = service.tool_run_tests(
            dry_run=True
        )

        self.assertTrue(
            result.success
        )

        system = service.tool_system_info()

        self.assertTrue(
            system.success
        )


if __name__ == "__main__":
    unittest.main()
