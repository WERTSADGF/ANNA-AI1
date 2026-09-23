from memory.models import Memory, MemoryType, PrivacyLevel
from memory.store import MemoryStore
from memory.policy import MemoryPolicy


class MemoryRetriever:

    def __init__(
        self,
        store: MemoryStore,
        policy: MemoryPolicy | None = None,
    ):
        self.store = store
        self.policy = policy or MemoryPolicy()

    def retrieve(
        self,
        query: str,
        memory_types: tuple[MemoryType, ...] | None = None,
        minimum_confidence: float = 0.50,
        allow_sensitive: bool = False,
        limit: int = 5,
    ) -> list[Memory]:

        terms = {
            term.lower()
            for term in query.split()
            if term.strip()
        }

        candidates = self.store.all_active()
        results: list[tuple[float, Memory]] = []

        for memory in candidates:

            if memory.confidence < minimum_confidence:
                continue

            if not self.policy.can_retrieve(
                memory.memory_type,
                memory.privacy_level,
                allow_sensitive=allow_sensitive,
            ):
                continue

            if memory_types and memory.memory_type not in memory_types:
                continue

            text = memory.content.lower()

            matches = sum(
                1
                for term in terms
                if term in text
            )

            if matches == 0:
                continue

            score = (
                matches
                + memory.importance
                + memory.confidence
            )

            results.append((score, memory))

        results.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            memory
            for _, memory in results[:limit]
        ]
