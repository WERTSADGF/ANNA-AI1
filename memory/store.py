from pathlib import Path
import json
from typing import Optional

from memory.models import Memory, MemoryStatus


class MemoryStore:

    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> list[dict]:
        if not self.path.exists():
            return []

        text = self.path.read_text(encoding="utf-8-sig").strip()

        if not text:
            return []

        return json.loads(text)

    def _save(self, records: list[dict]) -> None:
        temporary = self.path.with_suffix(".tmp")

        temporary.write_text(
            json.dumps(
                records,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        temporary.replace(self.path)

    def store(self, memory: Memory) -> Memory:
        records = self._load()
        records.append(memory.__dict__)
        self._save(records)
        return memory

    def get(self, memory_id: str) -> Optional[Memory]:
        records = self._load()

        for record in records:
            if record["id"] == memory_id:
                return Memory(**record)

        return None

    def all_active(self) -> list[Memory]:
        records = self._load()

        return [
            Memory(**record)
            for record in records
            if record["status"] == MemoryStatus.ACTIVE.value
        ]

    def update(self, memory: Memory) -> Memory:
        records = self._load()
        replaced = False

        for index, record in enumerate(records):
            if record["id"] == memory.id:
                records[index] = memory.__dict__
                replaced = True
                break

        if not replaced:
            raise KeyError(f"Memory not found: {memory.id}")

        self._save(records)

        return memory

    def delete(self, memory_id: str) -> None:
        records = self._load()

        remaining = [
            record
            for record in records
            if record["id"] != memory_id
        ]

        self._save(remaining)
