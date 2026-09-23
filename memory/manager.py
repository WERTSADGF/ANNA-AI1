from datetime import datetime, timezone

from memory.models import (
    Memory,
    MemoryStatus,
    MemoryType,
    PrivacyLevel,
)
from memory.store import MemoryStore
from memory.policy import MemoryPolicy
from memory.retrieval import MemoryRetriever


class MemoryManager:

    def __init__(self, store: MemoryStore):
        self.store = store
        self.policy = MemoryPolicy()
        self.retriever = MemoryRetriever(
            store=store,
            policy=self.policy,
        )

    def store_memory(
        self,
        content: str,
        memory_type: MemoryType,
        source: str,
        confidence: float,
        importance: float,
        privacy_level: PrivacyLevel = PrivacyLevel.NORMAL,
        project_id: str | None = None,
        expires_at: str | None = None,
        confirmed: bool = False,
    ) -> Memory:

        allowed = self.policy.should_store(
            content=content,
            memory_type=memory_type,
            confidence=confidence,
            importance=importance,
            privacy_level=privacy_level,
        )

        if not allowed:
            raise ValueError(
                "Memory did not pass storage policy."
            )

        memory = Memory(
            content=content,
            memory_type=memory_type,
            source=source,
            confidence=confidence,
            importance=importance,
            privacy_level=privacy_level,
            project_id=project_id,
            expires_at=expires_at,
            confirmed=confirmed,
        )

        return self.store.store(memory)

    def retrieve(
        self,
        query: str,
        memory_types=None,
        minimum_confidence: float = 0.50,
        allow_sensitive: bool = False,
        limit: int = 5,
    ):

        return self.retriever.retrieve(
            query=query,
            memory_types=memory_types,
            minimum_confidence=minimum_confidence,
            allow_sensitive=allow_sensitive,
            limit=limit,
        )

    def update(
        self,
        memory_id: str,
        content: str | None = None,
        confidence: float | None = None,
        importance: float | None = None,
        confirmed: bool | None = None,
    ) -> Memory:

        memory = self.store.get(memory_id)

        if memory is None:
            raise KeyError(
                f"Memory not found: {memory_id}"
            )

        if content is not None:
            memory.content = content

        if confidence is not None:
            memory.confidence = confidence

        if importance is not None:
            memory.importance = importance

        if confirmed is not None:
            memory.confirmed = confirmed

        memory.updated_at = datetime.now(
            timezone.utc
        ).isoformat()

        return self.store.update(memory)

    def archive(self, memory_id: str) -> Memory:
        memory = self.store.get(memory_id)

        if memory is None:
            raise KeyError(
                f"Memory not found: {memory_id}"
            )

        memory.status = MemoryStatus.ARCHIVED
        memory.updated_at = datetime.now(
            timezone.utc
        ).isoformat()

        return self.store.update(memory)

    def forget(self, memory_id: str) -> Memory:
        memory = self.store.get(memory_id)

        if memory is None:
            raise KeyError(
                f"Memory not found: {memory_id}"
            )

        memory.status = MemoryStatus.FORGOTTEN
        memory.updated_at = datetime.now(
            timezone.utc
        ).isoformat()

        return self.store.update(memory)

    def delete(self, memory_id: str) -> None:
        self.store.delete(memory_id)

    def confirm(self, memory_id: str) -> Memory:
        memory = self.store.get(memory_id)

        if memory is None:
            raise KeyError(
                f"Memory not found: {memory_id}"
            )

        memory.confirmed = True
        memory.updated_at = datetime.now(
            timezone.utc
        ).isoformat()

        return self.store.update(memory)
