import unittest

from security.permissions import PermissionLevel
from security.tool_allowlist import ToolAllowlist
from tools.service import ToolService


class TestToolAllowlistHardening(unittest.TestCase):

    def test_supported_tools_are_explicitly_allowlisted(self):
        allowlist = ToolAllowlist()

        expected = {
            "system_info": PermissionLevel.READ_ONLY,
            "code_inspection": PermissionLevel.READ_ONLY,
            "list_directory": PermissionLevel.READ_ONLY,
            "run_tests": PermissionLevel.LOW_RISK,
            "create_directory": PermissionLevel.LOW_RISK,
            "launch_application": PermissionLevel.IMPORTANT_CHANGE,
        }

        for name, level in expected.items():
            self.assertTrue(allowlist.is_allowed(name))
            self.assertEqual(
                allowlist.get_rule(name).permission_level,
                int(level),
            )

    def test_unsafe_tools_remain_denied(self):
        allowlist = ToolAllowlist()

        self.assertFalse(allowlist.is_allowed("terminal"))
        self.assertFalse(allowlist.is_allowed("shell"))
        self.assertFalse(allowlist.is_allowed("pc_control"))
        self.assertFalse(allowlist.is_allowed("delete_everything"))

    def test_tool_service_uses_allowlist(self):
        service = ToolService()

        self.assertTrue(
            service.allowlist.is_allowed("system_info")
        )
        self.assertTrue(
            service.allowlist.is_allowed("launch_application")
        )
        self.assertFalse(
            service.allowlist.is_allowed("terminal")
        )


if __name__ == "__main__":
    unittest.main()
