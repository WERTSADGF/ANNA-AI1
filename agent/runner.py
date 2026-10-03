from dataclasses import replace
from uuid import uuid4

from agent.executor import AgentExecutor
from agent.models import (
    AgentPlan,
    AgentRun,
    AgentRunStatus,
    AgentStepStatus,
    AgentStopReason,
)


class AgentRunner:

    def __init__(self, executor: AgentExecutor):
        self.executor = executor

    def run(
        self,
        plan: AgentPlan,
        confirmed: bool = False,
        dry_run: bool = False,
    ) -> AgentRun:

        if not plan.steps:
            return AgentRun(
                run_id=str(uuid4()),
                goal=plan.goal,
                status=AgentRunStatus.STOPPED,
                plan=plan,
                stop_reason=AgentStopReason.PLAN_EXHAUSTED,
            )

        steps = list(plan.steps)
        steps_used = 0

        for index, step in enumerate(steps):

            if steps_used >= plan.max_steps:
                return AgentRun(
                    run_id=str(uuid4()),
                    goal=plan.goal,
                    status=AgentRunStatus.STOPPED,
                    plan=replace(plan, steps=tuple(steps)),
                    current_step_index=index,
                    steps_used=steps_used,
                    stop_reason=AgentStopReason.STEP_BUDGET_EXHAUSTED,
                )

            if step.status != AgentStepStatus.PENDING:
                continue

            result = self.executor.execute_step(
                step,
                confirmed=confirmed,
                dry_run=dry_run,
            )

            steps[index] = result.step
            steps_used += 1

            updated_plan = replace(
                plan,
                steps=tuple(steps),
            )

            if result.blocked:
                return AgentRun(
                    run_id=str(uuid4()),
                    goal=plan.goal,
                    status=AgentRunStatus.BLOCKED,
                    plan=updated_plan,
                    current_step_index=index,
                    steps_used=steps_used,
                    stop_reason=AgentStopReason.PERMISSION_REQUIRED,
                )

            if (
                result.executed
                and not result.verified
            ):
                return AgentRun(
                    run_id=str(uuid4()),
                    goal=plan.goal,
                    status=AgentRunStatus.STOPPED,
                    plan=updated_plan,
                    current_step_index=index,
                    steps_used=steps_used,
                    stop_reason=AgentStopReason.VERIFICATION_FAILED,
                )

            if not result.success:
                return AgentRun(
                    run_id=str(uuid4()),
                    goal=plan.goal,
                    status=AgentRunStatus.FAILED,
                    plan=updated_plan,
                    current_step_index=index,
                    steps_used=steps_used,
                    stop_reason=AgentStopReason.ERROR,
                    error=result.error,
                )

        final_plan = replace(
            plan,
            steps=tuple(steps),
        )

        if all(
            step.status == AgentStepStatus.COMPLETED
            for step in steps
        ):
            return AgentRun(
                run_id=str(uuid4()),
                goal=plan.goal,
                status=AgentRunStatus.COMPLETED,
                plan=final_plan,
                current_step_index=len(steps),
                steps_used=steps_used,
                stop_reason=AgentStopReason.GOAL_COMPLETE,
            )

        if steps_used >= plan.max_steps:
            return AgentRun(
                run_id=str(uuid4()),
                goal=plan.goal,
                status=AgentRunStatus.STOPPED,
                plan=final_plan,
                current_step_index=len(steps),
                steps_used=steps_used,
                stop_reason=AgentStopReason.STEP_BUDGET_EXHAUSTED,
            )

        return AgentRun(
            run_id=str(uuid4()),
            goal=plan.goal,
            status=AgentRunStatus.STOPPED,
            plan=final_plan,
            current_step_index=len(steps),
            steps_used=steps_used,
            stop_reason=AgentStopReason.PLAN_EXHAUSTED,
        )
