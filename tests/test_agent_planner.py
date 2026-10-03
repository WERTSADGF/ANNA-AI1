import pytest

from agent.models import AgentStepStatus
from agent.planner import AgentPlanner


def test_planner_creates_system_info_step():
    plan = AgentPlanner().create("system information")

    assert len(plan.steps) == 1
    assert plan.steps[0].action_type == "system_info"
    assert plan.steps[0].target == "local-system"
    assert plan.steps[0].status == AgentStepStatus.PENDING
    assert plan.steps[0].requires_confirmation is False


def test_planner_creates_bounded_multi_step_plan():
    plan = AgentPlanner().create(
        "inspect python tools/service.py then run tests",
        max_steps=3,
    )

    assert len(plan.steps) == 2
    assert plan.steps[0].action_type == "code_inspection"
    assert plan.steps[0].target == "tools/service.py"
    assert plan.steps[1].action_type == "run_tests"


def test_planner_marks_application_launch_for_confirmation():
    plan = AgentPlanner().create("launch calculator")

    assert plan.steps[0].action_type == "launch_application"
    assert plan.steps[0].requires_confirmation is True


def test_planner_rejects_unsupported_actions():
    with pytest.raises(ValueError, match="Unsupported agent action request"):
        AgentPlanner().create("delete the project")


def test_planner_enforces_step_budget():
    with pytest.raises(ValueError, match="exceeding max_steps"):
        AgentPlanner().create(
            "system information then run tests",
            max_steps=1,
        )
