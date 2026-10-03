import json
import tempfile
import unittest
from pathlib import Path

from security.audit import AuditLogger
from tools.service import ToolService


class TestToolAuditHardening(unittest.TestCase):

    def test_tool_execution_is_audited(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "project"
            project_root.mkdir()

            audit_path = Path(temp_dir) / "audit.jsonl"
            logger = AuditLogger(str(audit_path))

            service = ToolService(
                project_root=project_root,
                audit=logger,
            )

            result = service.system_info()

            self.assertTrue(result.success)
            self.assertTrue(result.verified)
            self.assertTrue(result.executed)

            lines = audit_path.read_text(
                encoding="utf-8"
            ).splitlines()

            self.assertEqual(len(lines), 2)

            entries = [
                json.loads(line)
                for line in lines
            ]

            self.assertEqual(
                entries[0]["event"],
                "PERMISSION",
            )
            self.assertEqual(
                entries[0]["status"],
                "ALLOWED",
            )
            self.assertEqual(
                entries[1]["event"],
                "TOOL_EXECUTION",
            )
            self.assertEqual(
                entries[1]["status"],
                "SUCCESS",
            )
            self.assertTrue(
                entries[1]["details"]["executed"]
            )
            self.assertTrue(
                entries[1]["details"]["verified"]
            )

    def test_dry_run_is_audited_without_claiming_execution(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "project"
            project_root.mkdir()

            audit_path = Path(temp_dir) / "audit.jsonl"
            logger = AuditLogger(str(audit_path))

            service = ToolService(
                project_root=project_root,
                audit=logger,
            )

            result = service.run_tests(
                dry_run=True
            )

            self.assertTrue(result.success)
            self.assertFalse(result.executed)
            self.assertFalse(result.verified)

            entries = [
                json.loads(line)
                for line in audit_path.read_text(
                    encoding="utf-8"
                ).splitlines()
            ]

            self.assertEqual(
                entries[-1]["event"],
                "TOOL_EXECUTION",
            )
            self.assertEqual(
                entries[-1]["status"],
                "DRY_RUN",
            )
            self.assertFalse(
                entries[-1]["details"]["executed"]
            )
            self.assertFalse(
                entries[-1]["details"]["verified"]
            )

    def test_denied_action_is_audited(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "project"
            project_root.mkdir()

            audit_path = Path(temp_dir) / "audit.jsonl"
            logger = AuditLogger(str(audit_path))

            service = ToolService(
                project_root=project_root,
                audit=logger,
            )

            with self.assertRaises(PermissionError):
                service.launch_application(
                    "notepad",
                    dry_run=False,
                    confirmed=False,
                )

            entries = [
                json.loads(line)
                for line in audit_path.read_text(
                    encoding="utf-8"
                ).splitlines()
            ]

            self.assertEqual(
                entries[-2]["event"],
                "PERMISSION",
            )
            self.assertEqual(
                entries[-2]["status"],
                "DENIED",
            )
            self.assertEqual(
                entries[-1]["event"],
                "TOOL_EXECUTION",
            )
            self.assertEqual(
                entries[-1]["status"],
                "ERROR",
            )


if __name__ == "__main__":
    unittest.main()
