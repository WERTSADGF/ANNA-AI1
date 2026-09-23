from collections import Counter
import re

from files.models import FileChunk, FileSearchResult


class LocalTextIndex:

    def __init__(self):
        self._chunks: list[FileChunk] = []

    def clear(self) -> None:
        self._chunks.clear()

    def add(self, chunks: list[FileChunk]) -> None:
        self._chunks.extend(chunks)

    def all(self) -> list[FileChunk]:
        return list(self._chunks)

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[FileSearchResult]:

        terms = [
            term.lower()
            for term in re.findall(r"\w+", query)
            if term.strip()
        ]

        if not terms:
            return []

        results = []

        for chunk in self._chunks:

            words = re.findall(
                r"\w+",
                chunk.content.lower(),
            )

            counts = Counter(words)

            score = sum(
                counts.get(term, 0)
                for term in terms
            )

            if score > 0:
                results.append(
                    FileSearchResult(
                        chunk=chunk,
                        score=float(score),
                    )
                )

        results.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return results[:limit]
