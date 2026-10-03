from types import SimpleNamespace

from agent.executor import AgentExecutor
from agent.models import AgentStep, AgentStepStatus
from tools.models import ToolAction, ToolActionType, ToolResult
from security.permissions import PermissionLevel


class FakeToolService:

    def __init__(self):
        self.calls = []

    def system_info(self):
        self.calls.append("system_info")
        action = ToolAction(
            action_type=ToolActionType.SYSTEM_INFO,
            target="local-system",
            permission_level=PermissionLevel.READ_ONLY,
            description="system info",
            dry_run=False,
        )
        return ToolResult(
            action=action,
            executed=True,
            verified=True,
            success=True,
            output="OS: test",
            return_code=0,
        )

    def launch_application(
        self,
        name,
        dry_run=True,
        confirmed=False,
    ):
        self.calls.append(("launch_application", name, dry_run, confirmed))
        action = ToolAction(
            action_type=ToolActionType.LAUNCH_APPLICATION,
            target=name,
            permission_level=PermissionLevel.IMPORTANT_CHANGE,
            description="launch",
            dry_run=dry_run,
        )
        return ToolResult(
            action=action,
            executed=not dry_run,
            verified=not dry_run,
            success=True,
            output="DRY-RUN" if dry_run else "Launched",
        )


def test_executor_executes_exactly_one_safe_step():
    tools = FakeToolService()
    executor = AgentExecutor(tools)

    step = AgentStep(
        step_id="step-1",
        description="Read system information",
        action_type="system_info",
        target="local-system",
    )

    result = executor.execute_step(step)

    assert tools.calls == ["system_info"]
    assert result.executed is True
    assert result.verified is True
    assert result.success is True
    assert result.blocked is False
    assert result.step.status == AgentStepStatus.COMPLETED


def test_executor_blocks_confirmation_required_step():
    tools = FakeToolService()
    executor = AgentExecutor(tools)

    step = AgentStep(
        step_id="step-1",
        description="Launch calculator",
        action_type="launch_application",
        target="calculator",
        requires_confirmation=True,
    )

    result = executor.execute_step(step)

    assert tools.calls == []
    assert result.blocked is True
    assert result.executed is False
    assert result.step.status == AgentStepStatus.BLOCKED


def test_executor_allows_confirmed_dry_run_without_execution():
    tools = FakeToolService()
    executor = AgentExecutor(tools)

    step = AgentStep(
        step_id="step-1",
        description="Launch calculator",
        action_type="launch_application",
        target="calculator",
        requires_confirmation=True,
    )

    result = executor.execute_step(
        step,
        confirmed=True,
        dry_run=True,
    )

    assert tools.calls == [
        ("launch_application", "calculator", True, True)
    ]
    assert result.executed is False
    assert result.success is True
    assert result.step.status == AgentStepStatus.SKIPPED


def test_executor_rejects_unknown_action_without_tool_call():
    tools = FakeToolService()
    executor = AgentExecutor(tools)

    step = AgentStep(
        step_id="step-1",
        description="Unknown operation",
        action_type="delete_everything",
    )

    result = executor.execute_step(step)

    assert tools.calls == []
    assert result.success is False
    assert result.step.status == AgentStepStatus.FAILED
