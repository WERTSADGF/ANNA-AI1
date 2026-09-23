from dataclasses import dataclass

from research.models import ResearchMode, ResearchObjective


@dataclass(frozen=True)
class SearchPlan:
    objective: ResearchObjective
    subquestions: tuple[str, ...]
    source_goals: tuple[str, ...]


class ResearchPlanner:

    def create(
        self,
        question: str,
        mode: ResearchMode = ResearchMode.NORMAL,
    ) -> SearchPlan:

        cleaned = question.strip()

        if not cleaned:
            raise ValueError(
                "Research question cannot be empty."
            )

        if mode == ResearchMode.DEEP:

            return SearchPlan(
                objective=ResearchObjective(
                    question=cleaned,
                    mode=ResearchMode.DEEP,
                ),
                subquestions=(
                    cleaned,
                    f"Evidence supporting: {cleaned}",
                    f"Evidence challenging or qualifying: {cleaned}",
                ),
                source_goals=(
                    "Primary or official sources where available.",
                    "Independent reputable sources for cross-checking.",
                    "Sources that expose uncertainty or disagreement.",
                ),
            )

        return SearchPlan(
            objective=ResearchObjective(
                question=cleaned,
                mode=ResearchMode.NORMAL,
            ),
            subquestions=(cleaned,),
            source_goals=(
                "Relevant authoritative or primary source where available.",
                "Additional source when cross-checking is useful.",
            ),
        )
