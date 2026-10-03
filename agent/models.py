from dataclasses import dataclass
from enum import Enum


class AgentRunStatus(str, Enum):
    PLANNED = "planned"
    RUNNING = "running"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    STOPPED = "stopped"
    FAILED = "failed"


class AgentStepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"
    SKIPPED = "skipped"


class AgentStopReason(str, Enum):
    GOAL_COMPLETE = "goal_complete"
    PLAN_EXHAUSTED = "plan_exhausted"
    STEP_BUDGET_EXHAUSTED = "step_budget_exhausted"
    PERMISSION_REQUIRED = "permission_required"
    VERIFICATION_FAILED = "verification_failed"
    NO_PROGRESS = "no_progress"
    USER_STOPPED = "user_stopped"
    ERROR = "error"


@dataclass(frozen=True)
class AgentStep:
    step_id: str
    description: str
    action_type: str | None = None
    target: str = ""
    status: AgentStepStatus = AgentStepStatus.PENDING
    requires_confirmation: bool = False
    verified: bool = False
    result_summary: str = ""


@dataclass(frozen=True)
class AgentPlan:
    goal: str
    steps: tuple[AgentStep, ...]
    max_steps: int = 8


@dataclass(frozen=True)
class AgentRun:
    run_id: str
    goal: str
    status: AgentRunStatus
    plan: AgentPlan
    current_step_index: int = 0
    steps_used: int = 0
    stop_reason: AgentStopReason | None = None
    error: str = ""
