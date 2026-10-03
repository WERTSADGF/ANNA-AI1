from agent.models import (
    AgentPlan,
    AgentRunStatus,
    AgentStep,
    AgentStepStatus,
    AgentStopReason,
)
from agent.executor import AgentExecutor
from agent.runner import AgentRunner


class FakeToolService:

    def __init__(self):
        self.calls = []

    def system_info(self):
        self.calls.append("system_info")

        from tools.models import ToolAction, ToolResult, ToolActionType
        from security.permissions import PermissionLevel

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
        self.calls.append(
            ("launch_application", name, dry_run, confirmed)
        )

        from tools.models import ToolAction, ToolResult, ToolActionType
        from security.permissions import PermissionLevel

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
            output="dry-run" if dry_run else "launched",
        )


def test_runner_completes_all_verified_steps():
    tools = FakeToolService()
    runner = AgentRunner(AgentExecutor(tools))

    plan = AgentPlan(
        goal="Check system",
        steps=(
            AgentStep(
                step_id="step-1",
                description="Read system information",
                action_type="system_info",
                target="local-system",
            ),
        ),
        max_steps=2,
    )

    run = runner.run(plan)

    assert run.status == AgentRunStatus.COMPLETED
    assert run.stop_reason == AgentStopReason.GOAL_COMPLETE
    assert run.steps_used == 1
    assert run.plan.steps[0].status == AgentStepStatus.COMPLETED
    assert run.plan.steps[0].verified is True


def test_runner_stops_on_confirmation_boundary():
    tools = FakeToolService()
    runner = AgentRunner(AgentExecutor(tools))

    plan = AgentPlan(
        goal="Launch calculator",
        steps=(
            AgentStep(
                step_id="step-1",
                description="Launch calculator",
                action_type="launch_application",
                target="calculator",
                requires_confirmation=True,
            ),
        ),
        max_steps=2,
    )

    run = runner.run(plan)

    assert run.status == AgentRunStatus.BLOCKED
    assert run.stop_reason == AgentStopReason.PERMISSION_REQUIRED
    assert run.steps_used == 1
    assert run.plan.steps[0].status == AgentStepStatus.BLOCKED
    assert tools.calls == []


def test_runner_enforces_step_budget():
    tools = FakeToolService()
    runner = AgentRunner(AgentExecutor(tools))

    plan = AgentPlan(
        goal="Repeated check",
        steps=(
            AgentStep(
                step_id="step-1",
                description="First check",
                action_type="system_info",
                target="local-system",
            ),
            AgentStep(
                step_id="step-2",
                description="Second check",
                action_type="system_info",
                target="local-system",
            ),
        ),
        max_steps=1,
    )

    run = runner.run(plan)

    assert run.steps_used == 1
    assert run.status == AgentRunStatus.STOPPED
    assert run.stop_reason == AgentStopReason.STEP_BUDGET_EXHAUSTED
    assert tools.calls == ["system_info"]


def test_runner_does_not_claim_completion_for_dry_run():
    tools = FakeToolService()
    runner = AgentRunner(AgentExecutor(tools))

    plan = AgentPlan(
        goal="Launch calculator",
        steps=(
            AgentStep(
                step_id="step-1",
                description="Launch calculator",
                action_type="launch_application",
                target="calculator",
                requires_confirmation=True,
            ),
        ),
        max_steps=1,
    )

    run = runner.run(
        plan,
        confirmed=True,
        dry_run=True,
    )

    assert run.status == AgentRunStatus.STOPPED
    assert run.stop_reason == AgentStopReason.STEP_BUDGET_EXHAUSTED
    assert run.plan.steps[0].status == AgentStepStatus.SKIPPED
    assert run.plan.steps[0].verified is False

