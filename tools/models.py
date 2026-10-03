from dataclasses import dataclass
from enum import Enum

from security.permissions import PermissionLevel


class ToolActionType(str, Enum):
    SYSTEM_INFO = "system_info"
    CODE_INSPECTION = "code_inspection"
    RUN_TESTS = "run_tests"
    LIST_DIRECTORY = "list_directory"
    CREATE_DIRECTORY = "create_directory"
    LAUNCH_APPLICATION = "launch_application"


@dataclass(frozen=True)
class ToolAction:
    action_type: ToolActionType
    target: str
    permission_level: PermissionLevel
    description: str
    dry_run: bool = True


@dataclass(frozen=True)
class ToolResult:
    action: ToolAction
    executed: bool
    verified: bool
    success: bool
    output: str = ""
    error: str = ""
    return_code: int | None = None
