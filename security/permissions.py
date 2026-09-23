from dataclasses import dataclass
from enum import IntEnum


class PermissionLevel(IntEnum):
    READ_ONLY = 0
    LOW_RISK = 1
    IMPORTANT_CHANGE = 2
    HIGH_IMPACT = 3


@dataclass(frozen=True)
class PermissionRequest:
    action: str
    level: PermissionLevel
    resource: str = ""


@dataclass(frozen=True)
class PermissionResult:
    allowed: bool
    requires_confirmation: bool
    reason: str


class PermissionManager:
    def evaluate(
        self,
        request: PermissionRequest,
        confirmed: bool = False,
    ) -> PermissionResult:

        if request.level == PermissionLevel.READ_ONLY:
            return PermissionResult(
                allowed=True,
                requires_confirmation=False,
                reason="Read-only operation.",
            )

        if request.level == PermissionLevel.LOW_RISK:
            return PermissionResult(
                allowed=True,
                requires_confirmation=False,
                reason="Low-risk operation.",
            )

        if request.level == PermissionLevel.IMPORTANT_CHANGE:
            return PermissionResult(
                allowed=confirmed,
                requires_confirmation=True,
                reason="Important change requires explicit confirmation.",
            )

        return PermissionResult(
            allowed=confirmed,
            requires_confirmation=True,
            reason="High-impact operation requires explicit confirmation.",
        )
