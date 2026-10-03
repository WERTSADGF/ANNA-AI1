from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    DONE = "done"


@dataclass
class Task:
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    project_id: str | None = None
    due_at: datetime | None = None
    task_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)


@dataclass
class Reminder:
    title: str
    due_at: datetime
    reminder_id: str = field(default_factory=lambda: str(uuid4()))
    completed: bool = False
    created_at: datetime = field(default_factory=utc_now)


@dataclass
class Project:
    name: str
    description: str = ""
    project_id: str = field(default_factory=lambda: str(uuid4()))
    task_ids: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)


@dataclass
class AssistantState:
    tasks: list[Task] = field(default_factory=list)
    reminders: list[Reminder] = field(default_factory=list)
    projects: list[Project] = field(default_factory=list)
