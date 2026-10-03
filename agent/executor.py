from dataclasses import dataclass, replace

from agent.models import AgentStep, AgentStepStatus
from tools.models import ToolResult


@dataclass(frozen=True)
class AgentExecutionResult:
    step: AgentStep
    tool_result: ToolResult | None
    executed: bool
    verified: bool
    success: bool
    blocked: bool = False
    error: str = ""


class AgentExecutor:

    def __init__(self, tool_service):
        self.tool_service = tool_service

    def execute_step(
        self,
        step: AgentStep,
        confirmed: bool = False,
        dry_run: bool = False,
    ) -> AgentExecutionResult:

        if not step.action_type:
            updated = replace(
                step,
                status=AgentStepStatus.FAILED,
                result_summary="No tool action is assigned to this step.",
            )
            return AgentExecutionResult(
                step=updated,
                tool_result=None,
                executed=False,
                verified=False,
                success=False,
                error="No tool action is assigned to this step.",
            )

        if step.requires_confirmation and not confirmed:
            updated = replace(
                step,
                status=AgentStepStatus.BLOCKED,
                result_summary="Explicit confirmation is required before execution.",
            )
            return AgentExecutionResult(
                step=updated,
                tool_result=None,
                executed=False,
                verified=False,
                success=False,
                blocked=True,
                error="Explicit confirmation is required before execution.",
            )

        try:
            if step.action_type == "system_info":
                result = self.tool_service.system_info()

            elif step.action_type == "code_inspection":
                result = self.tool_service.inspect_python(step.target)

            elif step.action_type == "run_tests":
                result = self.tool_service.run_tests(
                    dry_run=dry_run,
                )

            elif step.action_type == "list_directory":
                result = self.tool_service.list_directory(step.target)

            elif step.action_type == "create_directory":
                result = self.tool_service.create_directory(
                    step.target,
                    dry_run=dry_run,
                )

            elif step.action_type == "launch_application":
                result = self.tool_service.launch_application(
                    step.target,
                    dry_run=dry_run,
                    confirmed=confirmed,
                )

            else:
                updated = replace(
                    step,
                    status=AgentStepStatus.FAILED,
                    result_summary=(
                        f"Unsupported tool action: {step.action_type}"
                    ),
                )
                return AgentExecutionResult(
                    step=updated,
                    tool_result=None,
                    executed=False,
                    verified=False,
                    success=False,
                    error=f"Unsupported tool action: {step.action_type}",
                )

            if result.executed and result.verified and result.success:
                status = AgentStepStatus.COMPLETED
            elif not result.executed and result.success:
                status = AgentStepStatus.SKIPPED
            elif result.executed and not result.verified:
                status = AgentStepStatus.FAILED
            else:
                status = AgentStepStatus.FAILED

            updated = replace(
                step,
                status=status,
                verified=result.verified,
                result_summary=result.output or result.error,
            )

            return AgentExecutionResult(
                step=updated,
                tool_result=result,
                executed=result.executed,
                verified=result.verified,
                success=result.success,
                error=result.error,
            )

        except PermissionError as exc:
            updated = replace(
                step,
                status=AgentStepStatus.BLOCKED,
                result_summary=str(exc),
            )
            return AgentExecutionResult(
                step=updated,
                tool_result=None,
                executed=False,
                verified=False,
                success=False,
                blocked=True,
                error=str(exc),
            )

        except Exception as exc:
            updated = replace(
                step,
                status=AgentStepStatus.FAILED,
                result_summary=str(exc),
            )
            return AgentExecutionResult(
                step=updated,
                tool_result=None,
                executed=False,
                verified=False,
                success=False,
                error=str(exc),
            )
