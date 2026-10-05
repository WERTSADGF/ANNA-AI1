from datetime import datetime, timezone
from pathlib import Path

from assistant.models import (
    AssistantState,
    Project,
    Reminder,
    Task,
    TaskStatus,
)
from assistant.store import AssistantStore
from security.permissions import (
    PermissionLevel,
    PermissionManager,
    PermissionRequest,
)


class AssistantService:

    def __init__(
        self,
        store: AssistantStore | None = None,
        permissions: PermissionManager | None = None,
    ):
        self.store = store or AssistantStore(
            Path(__file__).resolve().parents[1]
            / "data"
            / "assistant.json"
        )

        self.permissions = (
            permissions
            or PermissionManager()
        )

    def _require(
        self,
        action: str,
        level: PermissionLevel,
        resource: str = "",
        confirmed: bool = False,
    ) -> None:

        result = self.permissions.evaluate(
            PermissionRequest(
                action=action,
                level=level,
                resource=resource,
            ),
            confirmed=confirmed,
        )

        if not result.allowed:
            raise PermissionError(
                result.reason
            )

    def _load(self) -> AssistantState:
        return self.store.load()

    def _save(
        self,
        state: AssistantState,
    ) -> None:
        self.store.save(state)

    def create_task(
        self,
        title: str,
        description: str = "",
        project_id: str | None = None,
        due_at: datetime | None = None,
    ) -> Task:

        title = title.strip()

        if not title:
            raise ValueError(
                "Task title cannot be empty."
            )

        self._require(
            "create_task",
            PermissionLevel.LOW_RISK,
            title,
        )

        state = self._load()

        if project_id is not None:
            project = next(
                (
                    item
                    for item in state.projects
                    if item.project_id == project_id
                ),
                None,
            )

            if project is None:
                raise ValueError(
                    "Project does not exist."
                )

        task = Task(
            title=title,
            description=description.strip(),
            project_id=project_id,
            due_at=due_at,
        )

        state.tasks.append(task)

        if project_id is not None:
            for project in state.projects:
                if project.project_id == project_id:
                    project.task_ids.append(
                        task.task_id
                    )
                    project.updated_at = (
                        datetime.now(timezone.utc)
                    )
                    break

        self._save(state)

        return task

    def set_task_status(
        self,
        task_id: str,
        status: TaskStatus,
    ) -> Task:

        self._require(
            "set_task_status",
            PermissionLevel.LOW_RISK,
            task_id,
        )

        state = self._load()

        for task in state.tasks:
            if task.task_id == task_id:
                task.status = status
                task.updated_at = (
                    datetime.now(timezone.utc)
                )

                self._save(state)
                return task

        raise ValueError(
            "Task does not exist."
        )

    def create_reminder(
        self,
        title: str,
        due_at: datetime,
    ) -> Reminder:

        title = title.strip()

        if not title:
            raise ValueError(
                "Reminder title cannot be empty."
            )

        self._require(
            "create_reminder",
            PermissionLevel.LOW_RISK,
            title,
        )

        reminder = Reminder(
            title=title,
            due_at=due_at,
        )

        state = self._load()
        state.reminders.append(reminder)

        self._save(state)

        return reminder

    def complete_reminder(
        self,
        reminder_id: str,
    ) -> Reminder:

        self._require(
            "complete_reminder",
            PermissionLevel.LOW_RISK,
            reminder_id,
        )

        state = self._load()

        for reminder in state.reminders:
            if reminder.reminder_id == reminder_id:
                reminder.completed = True
                self._save(state)
                return reminder

        raise ValueError(
            "Reminder does not exist."
        )

    def create_project(
        self,
        name: str,
        description: str = "",
    ) -> Project:

        name = name.strip()

        if not name:
            raise ValueError(
                "Project name cannot be empty."
            )

        self._require(
            "create_project",
            PermissionLevel.LOW_RISK,
            name,
        )

        project = Project(
            name=name,
            description=description.strip(),
        )

        state = self._load()
        state.projects.append(project)

        self._save(state)

        return project

    def delete_project(
        self,
        project_id: str,
        confirmed: bool = False,
    ) -> None:

        self._require(
            "delete_project",
            PermissionLevel.IMPORTANT_CHANGE,
            project_id,
            confirmed=confirmed,
        )

        state = self._load()

        project = next(
            (
                item
                for item in state.projects
                if item.project_id == project_id
            ),
            None,
        )

        if project is None:
            raise ValueError(
                "Project does not exist."
            )

        for task in state.tasks:
            if task.project_id == project_id:
                task.project_id = None

        state.projects = [
            item
            for item in state.projects
            if item.project_id != project_id
        ]

        self._save(state)

    def list_tasks(self) -> tuple[Task, ...]:
        return tuple(
            self._load().tasks
        )

    def list_reminders(
        self,
    ) -> tuple[Reminder, ...]:
        return tuple(
            self._load().reminders
        )

    def list_projects(
        self,
    ) -> tuple[Project, ...]:
        return tuple(
            self._load().projects
        )

    def due_reminders(
        self,
        now: datetime | None = None,
    ) -> tuple[Reminder, ...]:

        current = (
            now
            or datetime.now(timezone.utc)
        )

        reminders = []

        for reminder in self._load().reminders:
            if reminder.completed:
                continue

            due_at = reminder.due_at
            if due_at.tzinfo is None:
                due_at = due_at.replace(tzinfo=timezone.utc)

            if due_at <= current:
                reminders.append(reminder)

        return tuple(reminders)
