from typing import Protocol

from research.models import ResearchObjective, Source


class SourceProvider(Protocol):

    @property
    def provider_name(self) -> str:
        ...

    def search(
        self,
        objective: ResearchObjective,
    ) -> list[Source]:
        ...


class MockSourceProvider:

    @property
    def provider_name(self) -> str:
        return "mock"

    def search(
        self,
        objective: ResearchObjective,
    ) -> list[Source]:

        return [
            Source(
                url="https://example.invalid/source-one",
                title="Mock Source One",
                retrieved_at="TEST",
                publisher="Mock",
                source_type="test",
                accessed=True,
            ),
            Source(
                url="https://example.invalid/source-two",
                title="Mock Source Two",
                retrieved_at="TEST",
                publisher="Mock",
                source_type="test",
                accessed=True,
            ),
        ]
