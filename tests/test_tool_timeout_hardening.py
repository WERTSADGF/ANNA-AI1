import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from security.audit import AuditLogger
from tools.service import ToolService


class TestToolTimeoutHardening(unittest.TestCase):

    def test_timeout_returns_structured_failed_result(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "project"
            project_root.mkdir()

            audit_path = Path(temp_dir) / "audit.jsonl"
            logger = AuditLogger(str(audit_path))

            service = ToolService(
                project_root=project_root,
                audit=logger,
            )

            timeout = subprocess.TimeoutExpired(
                cmd=["fake"],
                timeout=120,
                output="partial output",
            )

            with patch(
                "tools.service.subprocess.run",
                side_effect=timeout,
            ):
                result = service.run_tests(
                    dry_run=False
                )

            self.assertTrue(result.executed)
            self.assertFalse(result.verified)
            self.assertFalse(result.success)
            self.assertEqual(
                result.error,
                "Tool execution timed out after 120 seconds.",
            )

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
                "FAILED",
            )
            self.assertTrue(
                entries[-1]["details"]["executed"]
            )
            self.assertFalse(
                entries[-1]["details"]["verified"]
            )
            self.assertFalse(
                entries[-1]["details"]["success"]
            )


if __name__ == "__main__":
    unittest.main()
