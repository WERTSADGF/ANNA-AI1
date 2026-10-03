from dataclasses import FrozenInstanceError

import pytest

from agent.models import (
    AgentPlan,
    AgentRun,
    AgentRunStatus,
    AgentStep,
    AgentStepStatus,
    AgentStopReason,
)


def test_agent_step_defaults_are_safe():
    step = AgentStep(
        step_id="step-1",
        description="Inspect project",
    )

    assert step.status == AgentStepStatus.PENDING
    assert step.verified is False
    assert step.requires_confirmation is False
    assert step.action_type is None


def test_agent_plan_has_bounded_default_budget():
    plan = AgentPlan(
        goal="Inspect project",
        steps=(
            AgentStep(
                step_id="step-1",
                description="Inspect project",
            ),
        ),
    )

    assert plan.max_steps == 8
    assert len(plan.steps) == 1


def test_agent_run_tracks_stop_reason_and_usage():
    plan = AgentPlan(
        goal="Run bounded task",
        steps=(),
        max_steps=3,
    )

    run = AgentRun(
        run_id="run-1",
        goal="Run bounded task",
        status=AgentRunStatus.STOPPED,
        plan=plan,
        steps_used=3,
        stop_reason=AgentStopReason.STEP_BUDGET_EXHAUSTED,
    )

    assert run.steps_used == 3
    assert run.stop_reason == AgentStopReason.STEP_BUDGET_EXHAUSTED
    assert run.status == AgentRunStatus.STOPPED


def test_agent_models_are_immutable():
    step = AgentStep(
        step_id="step-1",
        description="Inspect project",
    )

    with pytest.raises(FrozenInstanceError):
        step.status = AgentStepStatus.COMPLETED
