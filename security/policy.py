from dataclasses import dataclass

from security.permissions import PermissionLevel


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    requires_confirmation: bool
    reason: str


def evaluate_permission(
    level: PermissionLevel,
    confirmed: bool = False,
) -> PolicyDecision:

    if level == PermissionLevel.READ_ONLY:
        return PolicyDecision(
            allowed=True,
            requires_confirmation=False,
            reason="Read-only operation.",
        )

    if level == PermissionLevel.LOW_RISK:
        return PolicyDecision(
            allowed=True,
            requires_confirmation=False,
            reason="Low-risk operation.",
        )

    if level == PermissionLevel.IMPORTANT_CHANGE:
        return PolicyDecision(
            allowed=confirmed,
            requires_confirmation=True,
            reason="Important change requires confirmation.",
        )

    return PolicyDecision(
        allowed=confirmed,
        requires_confirmation=True,
        reason="High-impact operation requires explicit confirmation.",
    )
