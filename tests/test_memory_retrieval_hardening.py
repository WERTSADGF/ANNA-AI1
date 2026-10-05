import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from memory.manager import MemoryManager
from memory.models import MemoryType
from memory.store import MemoryStore


class TestMemoryRetrievalHardening(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.store = MemoryStore(
            str(Path(self.temp_dir.name) / "memory.json")
        )
        self.manager = MemoryManager(self.store)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_expired_memory_is_not_retrieved(self):
        expired_at = (
            datetime.now(timezone.utc) - timedelta(minutes=1)
        ).isoformat()

        self.manager.store_memory(
            content="Expired Python preference",
            memory_type=MemoryType.PERSONAL,
            source="test",
            confidence=0.95,
            importance=0.90,
            expires_at=expired_at,
        )

        results = self.manager.retrieve(
            query="Python preference"
        )

        self.assertEqual(results, [])

    def test_negative_limit_is_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.retrieve(
                query="Python preference",
                limit=-1,
            )

    def test_future_expiration_memory_is_retrieved(self):
        future_at = (
            datetime.now(timezone.utc) + timedelta(minutes=1)
        ).isoformat()

        memory = self.manager.store_memory(
            content="Future Python preference",
            memory_type=MemoryType.PERSONAL,
            source="test",
            confidence=0.95,
            importance=0.90,
            expires_at=future_at,
        )

        results = self.manager.retrieve(
            query="Python preference"
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, memory.id)


if __name__ == "__main__":
    unittest.main()
