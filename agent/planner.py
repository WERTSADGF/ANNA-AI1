from agent.models import AgentPlan, AgentStep
from tools.models import ToolActionType


class AgentPlanner:

    def create(
        self,
        goal: str,
        max_steps: int = 8,
    ) -> AgentPlan:

        cleaned = goal.strip()

        if not cleaned:
            raise ValueError("Agent goal cannot be empty.")

        if max_steps <= 0:
            raise ValueError("Agent max_steps must be greater than zero.")

        requests = [
            item.strip()
            for item in __import__("re").split(
                r"\s+(?:then|and then)\s+",
                cleaned,
                flags=__import__("re").IGNORECASE,
            )
            if item.strip()
        ]

        steps: list[AgentStep] = []

        for index, request in enumerate(requests, start=1):
            lowered = request.lower()

            if lowered in {
                "system info",
                "system information",
                "check system info",
                "check system information",
            }:
                action = ToolActionType.SYSTEM_INFO.value
                target = "local-system"
                description = "Read local Python/runtime and operating-system information."
                confirmation = False

            elif lowered in {
                "run tests",
                "run test suite",
                "run the tests",
                "test the project",
            }:
                action = ToolActionType.RUN_TESTS.value
                target = "project-test-suite"
                description = "Run the ANNA Python test suite with cache provider disabled."
                confirmation = False

            elif lowered.startswith("inspect python "):
                path = request[len("inspect python "):].strip()
                if not path:
                    raise ValueError("Python inspection requires a path.")
                action = ToolActionType.CODE_INSPECTION.value
                target = path
                description = f"Inspect Python source syntax and structure: {path}"
                confirmation = False

            elif lowered.startswith("list directory"):
                path = request[len("list directory"):].strip() or "."
                action = ToolActionType.LIST_DIRECTORY.value
                target = path
                description = f"List files under authorized project path: {path}"
                confirmation = False

            elif lowered.startswith("create directory "):
                path = request[len("create directory "):].strip()
                if not path:
                    raise ValueError("Directory creation requires a path.")
                action = ToolActionType.CREATE_DIRECTORY.value
                target = path
                description = f"Create authorized project directory: {path}"
                confirmation = False

            elif lowered.startswith("launch "):
                name = request[len("launch "):].strip()
                if not name:
                    raise ValueError("Application launch requires an application name.")
                action = ToolActionType.LAUNCH_APPLICATION.value
                target = name
                description = f"Launch allowlisted application: {name}"
                confirmation = True

            else:
                raise ValueError(
                    f"Unsupported agent action request: {request}"
                )

            steps.append(
                AgentStep(
                    step_id=f"step-{index}",
                    description=description,
                    action_type=action,
                    target=target,
                    requires_confirmation=confirmation,
                )
            )

        if len(steps) > max_steps:
            raise ValueError(
                f"Agent plan requires {len(steps)} steps, exceeding max_steps={max_steps}."
            )

        return AgentPlan(
            goal=cleaned,
            steps=tuple(steps),
            max_steps=max_steps,
        )
