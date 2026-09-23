import tempfile
import unittest
from pathlib import Path

from memory.models import (
    MemoryType,
    PrivacyLevel,
    MemoryStatus,
)
from memory.store import MemoryStore
from memory.manager import MemoryManager


class TestMemoryFoundation(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.store_path = (
            Path(self.temp_dir.name) / "memory.json"
        )

        self.store = MemoryStore(
            str(self.store_path)
        )

        self.manager = MemoryManager(
            self.store
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_store_memory(self):
        memory = self.manager.store_memory(
            content="The owner prefers Python examples.",
            memory_type=MemoryType.PERSONAL,
            source="conversation",
            confidence=0.95,
            importance=0.80,
        )

        self.assertTrue(memory.id)
        self.assertEqual(
            memory.memory_type,
            MemoryType.PERSONAL,
        )

        loaded = self.store.get(memory.id)

        self.assertIsNotNone(loaded)
        self.assertEqual(
            loaded.content,
            "The owner prefers Python examples.",
        )

    def test_low_confidence_memory_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.store_memory(
                content="Possibly useful fact",
                memory_type=MemoryType.UNCERTAIN,
                source="unknown",
                confidence=0.20,
                importance=0.80,
            )

    def test_low_importance_memory_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.store_memory(
                content="Tiny unimportant detail",
                memory_type=MemoryType.PERSONAL,
                source="conversation",
                confidence=0.90,
                importance=0.10,
            )

    def test_sensitive_memory_requires_sensitive_privacy(self):
        with self.assertRaises(ValueError):
            self.manager.store_memory(
                content="Sensitive information",
                memory_type=MemoryType.SENSITIVE,
                source="conversation",
                confidence=0.90,
                importance=0.90,
                privacy_level=PrivacyLevel.NORMAL,
            )

    def test_retrieve_relevant_memory(self):
        self.manager.store_memory(
            content="The owner is learning Python programming.",
            memory_type=MemoryType.LEARNING,
            source="lesson",
            confidence=0.95,
            importance=0.85,
        )

        self.manager.store_memory(
            content="The owner is planning a website project.",
            memory_type=MemoryType.PROJECT,
            source="project discussion",
            confidence=0.95,
            importance=0.85,
        )

        results = self.manager.retrieve(
            query="Python learning",
            limit=5,
        )

        self.assertEqual(len(results), 1)
        self.assertIn(
            "Python",
            results[0].content,
        )

    def test_sensitive_memory_hidden_by_default(self):
        memory = self.manager.store_memory(
            content="Sensitive approved memory",
            memory_type=MemoryType.SENSITIVE,
            source="conversation",
            confidence=0.95,
            importance=0.95,
            privacy_level=PrivacyLevel.SENSITIVE,
            confirmed=True,
        )

        hidden = self.manager.retrieve(
            query="Sensitive approved memory",
            allow_sensitive=False,
        )

        self.assertEqual(hidden, [])

        visible = self.manager.retrieve(
            query="Sensitive approved memory",
            allow_sensitive=True,
        )

        self.assertEqual(len(visible), 1)
        self.assertEqual(visible[0].id, memory.id)

    def test_update_memory(self):
        memory = self.manager.store_memory(
            content="Learning Python.",
            memory_type=MemoryType.LEARNING,
            source="lesson",
            confidence=0.90,
            importance=0.80,
        )

        updated = self.manager.update(
            memory.id,
            content="Learning advanced Python.",
            confidence=0.95,
        )

        self.assertEqual(
            updated.content,
            "Learning advanced Python.",
        )

        self.assertEqual(
            updated.confidence,
            0.95,
        )

    def test_archive_memory(self):
        memory = self.manager.store_memory(
            content="Archived project memory.",
            memory_type=MemoryType.PROJECT,
            source="project",
            confidence=0.90,
            importance=0.80,
        )

        archived = self.manager.archive(memory.id)

        self.assertEqual(
            archived.status,
            MemoryStatus.ARCHIVED,
        )

        results = self.manager.retrieve(
            query="Archived project memory",
        )

        self.assertEqual(results, [])

    def test_forget_memory(self):
        memory = self.manager.store_memory(
            content="Forget this memory.",
            memory_type=MemoryType.PERSONAL,
            source="conversation",
            confidence=0.90,
            importance=0.80,
        )

        forgotten = self.manager.forget(memory.id)

        self.assertEqual(
            forgotten.status,
            MemoryStatus.FORGOTTEN,
        )

        results = self.manager.retrieve(
            query="Forget this memory",
        )

        self.assertEqual(results, [])

    def test_confirm_memory(self):
        memory = self.manager.store_memory(
            content="Confirmed preference.",
            memory_type=MemoryType.PERSONAL,
            source="conversation",
            confidence=0.90,
            importance=0.80,
        )

        self.assertFalse(memory.confirmed)

        confirmed = self.manager.confirm(
            memory.id
        )

        self.assertTrue(confirmed.confirmed)

    def test_delete_memory(self):
        memory = self.manager.store_memory(
            content="Delete this memory.",
            memory_type=MemoryType.PERSONAL,
            source="conversation",
            confidence=0.90,
            importance=0.80,
        )

        self.manager.delete(memory.id)

        self.assertIsNone(
            self.store.get(memory.id)
        )


if __name__ == "__main__":
    unittest.main()
