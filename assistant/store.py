import json
from datetime import datetime, timezone
from pathlib import Path

from assistant.models import (
    AssistantState,
    Project,
    Reminder,
    Task,
    TaskStatus,
)


class AssistantStore:

    def __init__(self, path: Path | str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self.save(AssistantState())

    def load(self) -> AssistantState:
        try:
            data = json.loads(
                self.path.read_text(
                    encoding="utf-8-sig"
                )
            )
        except (OSError, json.JSONDecodeError):
            return AssistantState()

        if not isinstance(data, dict):
            return AssistantState()

        tasks_data = data.get("tasks", [])
        if not isinstance(tasks_data, list):
            tasks_data = []
        tasks = []

        for item in tasks_data:
            if not isinstance(item, dict):
                continue
            try:
                created_at = self._parse_datetime(
                    item.get("created_at")
                )
                updated_at = self._parse_datetime(
                    item.get("updated_at")
                )

                tasks.append(
                    Task(
                        title=item["title"],
                        description=item.get("description", ""),
                        status=TaskStatus(
                            item.get(
                                "status",
                                TaskStatus.TODO.value,
                            )
                        ),
                        project_id=item.get("project_id"),
                        due_at=self._parse_datetime(
                            item.get("due_at")
                        ),
                        task_id=item.get("task_id") or "",
                        created_at=created_at or self._default_time(),
                        updated_at=updated_at or self._default_time(),
                    )
                )
            except (KeyError, TypeError, ValueError):
                continue

        reminders_data = data.get("reminders", [])
        if not isinstance(reminders_data, list):
            reminders_data = []
        reminders = []

        for item in reminders_data:
            if not isinstance(item, dict):
                continue
            try:
                due_at = self._parse_datetime(
                    item.get("due_at")
                )

                if due_at is None:
                    continue

                reminders.append(
                    Reminder(
                        title=item["title"],
                        due_at=due_at,
                        reminder_id=item.get("reminder_id") or "",
                        completed=bool(
                            item.get("completed", False)
                        ),
                        created_at=(
                            self._parse_datetime(
                                item.get("created_at")
                            )
                            or self._default_time()
                        ),
                    )
                )
            except (KeyError, TypeError, ValueError):
                continue

        projects_data = data.get("projects", [])
        if not isinstance(projects_data, list):
            projects_data = []
        projects = []

        for item in projects_data:
            if not isinstance(item, dict):
                continue
            try:
                projects.append(
                    Project(
                        name=item["name"],
                        description=item.get("description", ""),
                        project_id=item.get("project_id") or "",
                        task_ids=list(
                            item.get("task_ids", [])
                        ),
                        created_at=(
                            self._parse_datetime(
                                item.get("created_at")
                            )
                            or self._default_time()
                        ),
                        updated_at=(
                            self._parse_datetime(
                                item.get("updated_at")
                            )
                            or self._default_time()
                        ),
                    )
                )
            except (KeyError, TypeError, ValueError):
                continue

        return AssistantState(
            tasks=tasks,
            reminders=reminders,
            projects=projects,
        )

    def save(self, state: AssistantState) -> None:
        payload = {
            "tasks": [
                self._task_to_dict(task)
                for task in state.tasks
            ],
            "reminders": [
                self._reminder_to_dict(reminder)
                for reminder in state.reminders
            ],
            "projects": [
                self._project_to_dict(project)
                for project in state.projects
            ],
        }

        temporary = self.path.with_suffix(
            self.path.suffix + ".tmp"
        )

        temporary.write_text(
            json.dumps(
                payload,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        temporary.replace(self.path)

    @staticmethod
    def _default_time() -> datetime:
        return datetime.fromtimestamp(
            0,
            tz=timezone.utc,
        )

    @staticmethod
    def _parse_datetime(
        value: str | None,
    ) -> datetime | None:
        if not value:
            return None

        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None

    @staticmethod
    def _task_to_dict(task: Task) -> dict:
        return {
            "title": task.title,
            "description": task.description,
            "status": task.status.value,
            "project_id": task.project_id,
            "due_at": (
                task.due_at.isoformat()
                if task.due_at
                else None
            ),
            "task_id": task.task_id,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat(),
        }

    @staticmethod
    def _reminder_to_dict(
        reminder: Reminder,
    ) -> dict:
        return {
            "title": reminder.title,
            "due_at": reminder.due_at.isoformat(),
            "reminder_id": reminder.reminder_id,
            "completed": reminder.completed,
            "created_at": reminder.created_at.isoformat(),
        }

    @staticmethod
    def _project_to_dict(
        project: Project,
    ) -> dict:
        return {
            "name": project.name,
            "description": project.description,
            "project_id": project.project_id,
            "task_ids": project.task_ids,
            "created_at": project.created_at.isoformat(),
            "updated_at": project.updated_at.isoformat(),
        }
