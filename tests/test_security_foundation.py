import tempfile
import unittest
from pathlib import Path

from security.permissions import (
    PermissionLevel,
    PermissionManager,
    PermissionRequest,
)
from security.policy import (
    PermissionLevel as PolicyPermissionLevel,
    evaluate_permission,
)
from security.tool_allowlist import ToolAllowlist
from security.directory_allowlist import DirectoryAllowlist
from security.audit import AuditLogger


class TestSecurityFoundation(unittest.TestCase):

    def test_read_only_permission(self):
        manager = PermissionManager()

        result = manager.evaluate(
            PermissionRequest(
                action="inspect",
                level=PermissionLevel.READ_ONLY,
            )
        )

        self.assertTrue(result.allowed)
        self.assertFalse(result.requires_confirmation)

    def test_high_impact_requires_confirmation(self):
        manager = PermissionManager()

        result = manager.evaluate(
            PermissionRequest(
                action="critical_change",
                level=PermissionLevel.HIGH_IMPACT,
            )
        )

        self.assertFalse(result.allowed)
        self.assertTrue(result.requires_confirmation)

    def test_high_impact_with_confirmation(self):
        manager = PermissionManager()

        result = manager.evaluate(
            PermissionRequest(
                action="critical_change",
                level=PermissionLevel.HIGH_IMPACT,
            ),
            confirmed=True,
        )

        self.assertTrue(result.allowed)

    def test_policy_and_permission_share_one_permission_enum(self):
        self.assertIs(
            PermissionLevel,
            PolicyPermissionLevel,
        )

        result = evaluate_permission(
            PermissionLevel.IMPORTANT_CHANGE,
            confirmed=False,
        )

        self.assertFalse(result.allowed)
        self.assertTrue(result.requires_confirmation)

    def test_tool_allowlist(self):
        allowlist = ToolAllowlist()

        self.assertTrue(allowlist.is_allowed("read_only"))
        self.assertFalse(allowlist.is_allowed("terminal"))
        self.assertFalse(allowlist.is_allowed("pc_control"))

    def test_directory_allowlist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            allowed = DirectoryAllowlist([temp_dir])

            inside = Path(temp_dir) / "example.txt"
            outside = Path(temp_dir).parent / "outside-example.txt"

            self.assertTrue(allowed.is_allowed(str(inside)))
            self.assertFalse(allowed.is_allowed(str(outside)))

    def test_audit_logger(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "audit.jsonl"

            logger = AuditLogger(str(log_path))

            logger.record(
                event="TEST",
                action="security_check",
                status="SUCCESS",
            )

            self.assertTrue(log_path.exists())
            self.assertEqual(
                len(
                    log_path
                    .read_text(encoding="utf-8")
                    .splitlines()
                ),
                1,
            )


if __name__ == "__main__":
    unittest.main()
