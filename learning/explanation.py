from dataclasses import dataclass

from learning.models import Difficulty, LearningProfile, Topic


@dataclass(frozen=True)
class ExplanationPlan:
    level: Difficulty
    use_simple_language: bool
    include_example: bool
    include_analogy: bool
    include_practical_application: bool
    include_technical_detail: bool


class ExplanationPlanner:

    def build(
        self,
        topic: Topic,
        profile: LearningProfile,
    ) -> ExplanationPlan:

        level = profile.current_level_by_subject.get(
            topic.name,
            topic.difficulty,
        )

        include_technical = (
            level in (
                Difficulty.ADVANCED,
                Difficulty.EXPERT,
            )
        )

        return ExplanationPlan(
            level=level,
            use_simple_language=True,
            include_example=True,
            include_analogy=True,
            include_practical_application=True,
            include_technical_detail=include_technical,
        )


def alternative_explanation_number(
    attempts: int,
) -> int:

    if attempts <= 1:
        return 1

    if attempts == 2:
        return 2

    if attempts == 3:
        return 3

    return 4
