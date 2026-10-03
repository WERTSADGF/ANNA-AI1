from chat.service import ChatService
from tools.models import ToolAction, ToolActionType, ToolResult
from security.permissions import PermissionLevel


class FakeToolService:

    def system_info(self):
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


def test_chat_service_agent_plan():
    service = ChatService(
        tool_service=FakeToolService(),
    )

    plan = service.agent_plan(
        "system information",
        max_steps=2,
    )

    assert plan.goal == "system information"
    assert plan.max_steps == 2
    assert plan.steps[0].action_type == "system_info"


def test_chat_service_agent_run():
    service = ChatService(
        tool_service=FakeToolService(),
    )

    run = service.agent_run(
        "system information",
        max_steps=2,
    )

    assert run.status.value == "completed"
    assert run.stop_reason.value == "goal_complete"
    assert run.steps_used == 1
    assert run.plan.steps[0].verified is True


def test_chat_service_agent_confirmation_boundary():
    service = ChatService()

    run = service.agent_run(
        "launch calculator",
        max_steps=1,
        confirmed=False,
        dry_run=False,
    )

    assert run.status.value == "blocked"
    assert run.stop_reason.value == "permission_required"
    assert run.plan.steps[0].status.value == "blocked"
