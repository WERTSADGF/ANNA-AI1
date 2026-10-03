from dataclasses import dataclass

from security.permissions import PermissionLevel


@dataclass(frozen=True)
class ToolRule:
    name: str
    enabled: bool
    permission_level: int


class ToolAllowlist:
    def __init__(self):
        self._rules = {
            "read_only": ToolRule(
                name="read_only",
                enabled=True,
                permission_level=int(PermissionLevel.READ_ONLY),
            ),
            "system_info": ToolRule(
                name="system_info",
                enabled=True,
                permission_level=int(PermissionLevel.READ_ONLY),
            ),
            "code_inspection": ToolRule(
                name="code_inspection",
                enabled=True,
                permission_level=int(PermissionLevel.READ_ONLY),
            ),
            "list_directory": ToolRule(
                name="list_directory",
                enabled=True,
                permission_level=int(PermissionLevel.READ_ONLY),
            ),
            "run_tests": ToolRule(
                name="run_tests",
                enabled=True,
                permission_level=int(PermissionLevel.LOW_RISK),
            ),
            "create_directory": ToolRule(
                name="create_directory",
                enabled=True,
                permission_level=int(PermissionLevel.LOW_RISK),
            ),
            "launch_application": ToolRule(
                name="launch_application",
                enabled=True,
                permission_level=int(PermissionLevel.IMPORTANT_CHANGE),
            ),
        }

    def is_allowed(self, tool_name: str) -> bool:
        rule = self._rules.get(tool_name)
        return bool(rule and rule.enabled)

    def get_rule(self, tool_name: str):
        return self._rules.get(tool_name)
