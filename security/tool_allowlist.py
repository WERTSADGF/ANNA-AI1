from dataclasses import dataclass


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
                permission_level=0,
            ),
        }

    def is_allowed(self, tool_name: str) -> bool:
        rule = self._rules.get(tool_name)
        return bool(rule and rule.enabled)

    def get_rule(self, tool_name: str):
        return self._rules.get(tool_name)
