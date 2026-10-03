import re

from memory.models import Memory, MemoryType, PrivacyLevel
from memory.store import MemoryStore
from memory.policy import MemoryPolicy


class MemoryRetriever:

    _STOPWORDS = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "been",
        "being",
        "but",
        "by",
        "can",
        "did",
        "do",
        "does",
        "for",
        "from",
        "had",
        "has",
        "have",
        "how",
        "i",
        "if",
        "in",
        "is",
        "it",
        "me",
        "my",
        "of",
        "on",
        "or",
        "please",
        "that",
        "the",
        "this",
        "to",
        "was",
        "we",
        "were",
        "what",
        "when",
        "where",
        "which",
        "who",
        "why",
        "with",
        "you",
        "your",
    }

    def __init__(
        self,
        store: MemoryStore,
        policy: MemoryPolicy | None = None,
    ):
        self.store = store
        self.policy = policy or MemoryPolicy()

    @classmethod
    def _tokenize(cls, text: str) -> set[str]:
        tokens = {
            token
            for token in re.findall(r"\w+", text.lower(), flags=re.UNICODE)
            if token not in cls._STOPWORDS
        }
        return tokens

    def retrieve(
        self,
        query: str,
        memory_types: tuple[MemoryType, ...] | None = None,
        minimum_confidence: float = 0.50,
        allow_sensitive: bool = False,
        limit: int = 5,
    ) -> list[Memory]:

        terms = self._tokenize(query)

        if not terms:
            return []

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

            memory_terms = self._tokenize(memory.content)

            matches = len(terms & memory_terms)

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
