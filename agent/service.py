from pathlib import Path
from agent.executor import AgentExecutor
from agent.models import AgentPlan, AgentRun
from agent.planner import AgentPlanner
from agent.runner import AgentRunner
from security.audit import AuditLogger


class AgentService:

    def __init__(
        self,
        tool_service,
        planner: AgentPlanner | None = None,
        audit: AuditLogger | None = None,
    ):
        self.planner = planner or AgentPlanner()
        self.audit = audit or getattr(tool_service, "audit", None) or AuditLogger(str(Path(__file__).resolve().parents[1] / "data" / "audit.jsonl"))
        self.runner = AgentRunner(
            AgentExecutor(tool_service)
        )

    def plan(
        self,
        goal: str,
        max_steps: int = 8,
    ) -> AgentPlan:
        plan = self.planner.create(
            goal=goal,
            max_steps=max_steps,
        )

        self.audit.record(
            event="AGENT_PLAN",
            action="plan",
            status="CREATED",
            details={
                "goal": plan.goal,
                "steps": len(plan.steps),
                "max_steps": plan.max_steps,
            },
        )

        return plan

    def run(
        self,
        goal: str,
        max_steps: int = 8,
        confirmed: bool = False,
        dry_run: bool = False,
    ) -> AgentRun:

        plan = self.plan(
            goal=goal,
            max_steps=max_steps,
        )

        self.audit.record(
            event="AGENT_RUN",
            action="run",
            status="STARTED",
            details={
                "goal": plan.goal,
                "steps": len(plan.steps),
                "max_steps": plan.max_steps,
                "confirmed": confirmed,
                "dry_run": dry_run,
            },
        )

        try:
            result = self.runner.run(
                plan=plan,
                confirmed=confirmed,
                dry_run=dry_run,
            )
        except Exception as exc:
            self.audit.record(
                event="AGENT_RUN",
                action="run",
                status="ERROR",
                details={
                    "goal": plan.goal,
                    "error": str(exc),
                },
            )
            raise

        self.audit.record(
            event="AGENT_RUN",
            action="run",
            status=result.status.value.upper(),
            details={
                "goal": result.goal,
                "steps_used": result.steps_used,
                "stop_reason": (
                    result.stop_reason.value
                    if result.stop_reason
                    else None
                ),
                "current_step_index": result.current_step_index,
            },
        )

        return result

