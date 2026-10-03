import json
import tempfile
import unittest
from pathlib import Path

from agent.service import AgentService
from security.audit import AuditLogger
from security.permissions import PermissionLevel
from tools.models import ToolAction, ToolActionType, ToolResult


class FakeToolService:

    def __init__(self, audit):
        self.audit = audit

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


def test_agent_service_plan_exposes_bounded_plan():
    with tempfile.TemporaryDirectory() as temp_dir:
        audit = AuditLogger(
            str(Path(temp_dir) / "audit.jsonl")
        )
        service = AgentService(
            FakeToolService(audit)
        )

        plan = service.plan(
            "system information",
            max_steps=2,
        )

        assert plan.goal == "system information"
        assert plan.max_steps == 2
        assert len(plan.steps) == 1


def test_agent_service_run_uses_planner_and_runner():
    with tempfile.TemporaryDirectory() as temp_dir:
        audit = AuditLogger(
            str(Path(temp_dir) / "audit.jsonl")
        )
        service = AgentService(
            FakeToolService(audit)
        )

        run = service.run(
            "system information",
            max_steps=2,
        )

        assert run.status.value == "completed"
        assert run.stop_reason.value == "goal_complete"
        assert run.steps_used == 1
        assert run.plan.steps[0].verified is True


def test_agent_service_rejects_unbounded_invalid_budget():
    with tempfile.TemporaryDirectory() as temp_dir:
        audit = AuditLogger(
            str(Path(temp_dir) / "audit.jsonl")
        )
        service = AgentService(
            FakeToolService(audit)
        )

        try:
            service.plan(
                "system information",
                max_steps=0,
            )
        except ValueError as exc:
            assert "greater than zero" in str(exc)
        else:
            raise AssertionError("Expected invalid budget to be rejected")


def test_agent_plan_and_run_are_audited():
    with tempfile.TemporaryDirectory() as temp_dir:
        audit_path = Path(temp_dir) / "audit.jsonl"
        audit = AuditLogger(str(audit_path))

        service = AgentService(
            FakeToolService(audit)
        )

        run = service.run(
            "system information",
            max_steps=2,
        )

        entries = [
            json.loads(line)
            for line in audit_path.read_text(
                encoding="utf-8"
            ).splitlines()
        ]

        assert any(
            entry["event"] == "AGENT_PLAN"
            and entry["status"] == "CREATED"
            for entry in entries
        )

        assert any(
            entry["event"] == "AGENT_RUN"
            and entry["status"] == "STARTED"
            for entry in entries
        )

        assert any(
            entry["event"] == "AGENT_RUN"
            and entry["status"] == "COMPLETED"
            and entry["details"]["steps_used"] == 1
            and entry["details"]["stop_reason"] == "goal_complete"
            for entry in entries
        )

        assert run.status.value == "completed"


if __name__ == "__main__":
    unittest.main()
