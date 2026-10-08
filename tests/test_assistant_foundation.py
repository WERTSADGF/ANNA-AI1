import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from assistant.models import Reminder, TaskStatus
from assistant.service import AssistantService
from assistant.store import AssistantStore
from chat.models import ChatMessage, ChatResponse
from chat.service import ChatService


class RecordingProvider:

    def generate(self, request):
        return ChatResponse(
            message=ChatMessage(
                role="assistant",
                content="assistant test response",
            ),
            provider="recording",
            model="test-model",
        )


class TestAssistantFoundation(unittest.TestCase):

    def make_service(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)

        return AssistantService(
            store=AssistantStore(
                Path(directory.name)
                / "assistant.json"
            )
        )

    def test_invalid_persisted_root_shape_recovers_empty_state(self):
        service = self.make_service()

        service.store.path.write_text(
            json.dumps(["not", "an", "assistant", "state"]),
            encoding="utf-8",
        )

        state = service.store.load()

        self.assertEqual(state.tasks, [])
        self.assertEqual(state.reminders, [])
        self.assertEqual(state.projects, [])

    def test_invalid_persisted_collection_shape_recovers_empty_section(self):
        service = self.make_service()

        payload = {
            "tasks": {"invalid": "shape"},
            "reminders": [],
            "projects": [],
        }

        service.store.path.write_text(
            json.dumps(payload),
            encoding="utf-8",
        )

        state = service.store.load()

        self.assertEqual(state.tasks, [])
        self.assertEqual(state.reminders, [])
        self.assertEqual(state.projects, [])

    def test_task_persists_and_status_changes(self):
        service = self.make_service()

        task = service.create_task(
            "Build ANNA UI"
        )

        service.set_task_status(
            task.task_id,
            TaskStatus.IN_PROGRESS,
        )

        tasks = service.list_tasks()

        self.assertEqual(
            len(tasks),
            1,
        )

        self.assertEqual(
            tasks[0].status,
            TaskStatus.IN_PROGRESS,
        )

    def test_reminder_persists_and_becomes_due(self):
        service = self.make_service()

        due = (
            datetime.now(timezone.utc)
            - timedelta(minutes=1)
        )

        reminder = service.create_reminder(
            "Study ANNA",
            due,
        )

        due_items = service.due_reminders()

        self.assertEqual(
            len(due_items),
            1,
        )

        self.assertEqual(
            due_items[0].reminder_id,
            reminder.reminder_id,
        )

    def test_naive_reminder_datetime_is_handled(self):
        service = self.make_service()

        state = service.store.load()
        state.reminders.append(
            Reminder(
                title="Naive reminder",
                due_at=(datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(minutes=1)),
            )
        )
        service.store.save(state)

        due_items = service.due_reminders()

        self.assertEqual(len(due_items), 1)
        self.assertEqual(
            due_items[0].title,
            "Naive reminder",
        )

    def test_invalid_persisted_task_status_is_ignored(self):
        service = self.make_service()

        payload = {
            "tasks": [
                {
                    "title": "Broken task",
                    "status": "invalid_status"
                },
                {
                    "title": "Valid task",
                    "status": "todo"
                }
            ]
        }

        service.store.path.write_text(
            json.dumps(payload),
            encoding="utf-8",
        )

        tasks = service.list_tasks()

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Valid task")

    def test_invalid_persisted_reminder_is_ignored(self):
        service = self.make_service()

        payload = {
            "reminders": [
                {
                    "due_at": "2026-10-08T10:00:00+00:00"
                },
                {
                    "title": "Valid reminder",
                    "due_at": "2026-10-08T10:00:00+00:00"
                }
            ]
        }

        service.store.path.write_text(
            json.dumps(payload),
            encoding="utf-8",
        )

        reminders = service.list_reminders()

        self.assertEqual(len(reminders), 1)
        self.assertEqual(reminders[0].title, "Valid reminder")

    def test_invalid_persisted_project_is_ignored(self):
        service = self.make_service()

        payload = {
            "projects": [
                {
                    "description": "Broken project"
                },
                {
                    "name": "Valid project"
                }
            ]
        }

        service.store.path.write_text(
            json.dumps(payload),
            encoding="utf-8",
        )

        projects = service.list_projects()

        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0].name, "Valid project")

    def test_project_links_tasks(self):
        service = self.make_service()

        project = service.create_project(
            "ANNA Phase 9"
        )

        task = service.create_task(
            "Implement tasks",
            project_id=project.project_id,
        )

        loaded_project = (
            service.list_projects()[0]
        )

        loaded_task = (
            service.list_tasks()[0]
        )

        self.assertEqual(
            loaded_project.task_ids,
            [task.task_id],
        )

        self.assertEqual(
            loaded_task.project_id,
            project.project_id,
        )

    def test_project_deletion_requires_confirmation(self):
        service = self.make_service()

        project = service.create_project(
            "Protected project"
        )

        with self.assertRaises(PermissionError):
            service.delete_project(
                project.project_id
            )

        service.delete_project(
            project.project_id,
            confirmed=True,
        )

        self.assertEqual(
            len(service.list_projects()),
            0,
        )


class TestChatAssistantIntegration(unittest.TestCase):

    def test_chat_service_has_assistant(self):
        service = ChatService(
            provider=RecordingProvider()
        )

        self.assertIsInstance(
            service.assistant,
            AssistantService,
        )

    def test_chat_service_exposes_assistant_operations(self):
        service = ChatService(
            provider=RecordingProvider()
        )

        project = service.create_assistant_project(
            "ANNA Project"
        )

        task = service.create_assistant_task(
            "Build task",
            project_id=project.project_id,
        )

        service.set_assistant_task_status(
            task.task_id,
            TaskStatus.DONE,
        )

        self.assertEqual(
            service.assistant_tasks()[0].status,
            TaskStatus.DONE,
        )

        self.assertEqual(
            service.assistant_projects()[0].name,
            "ANNA Project",
        )


if __name__ == "__main__":
    unittest.main()
