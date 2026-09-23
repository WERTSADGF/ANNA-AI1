from dataclasses import dataclass

from learning.models import Difficulty, LearningGoal, Topic


@dataclass(frozen=True)
class LearningRoadmap:
    goal: LearningGoal
    topics: tuple[Topic, ...]


class CurriculumBuilder:

    def build(
        self,
        subject: str,
        goal: str,
        level: Difficulty,
    ) -> LearningRoadmap:

        if not subject.strip():
            raise ValueError(
                "Subject cannot be empty."
            )

        if not goal.strip():
            raise ValueError(
                "Learning goal cannot be empty."
            )

        topics = self._default_topics(
            subject=subject,
            level=level,
        )

        return LearningRoadmap(
            goal=LearningGoal(
                subject=subject,
                goal=goal,
                target_level=level,
            ),
            topics=tuple(topics),
        )

    def _default_topics(
        self,
        subject: str,
        level: Difficulty,
    ) -> list[Topic]:

        subject_name = subject.strip()

        return [
            Topic(
                name=f"{subject_name} foundations",
                description=(
                    f"Core concepts and vocabulary for {subject_name}."
                ),
                prerequisites=(),
                difficulty=Difficulty.BEGINNER,
            ),
            Topic(
                name=f"{subject_name} core concepts",
                description=(
                    f"Essential working concepts in {subject_name}."
                ),
                prerequisites=(
                    f"{subject_name} foundations",
                ),
                difficulty=min_level(
                    level,
                    Difficulty.INTERMEDIATE,
                ),
            ),
            Topic(
                name=f"{subject_name} practical application",
                description=(
                    f"Using {subject_name} in practical situations."
                ),
                prerequisites=(
                    f"{subject_name} core concepts",
                ),
                difficulty=level,
            ),
        ]


def min_level(
    requested: Difficulty,
    maximum: Difficulty,
) -> Difficulty:

    order = {
        Difficulty.BEGINNER: 0,
        Difficulty.INTERMEDIATE: 1,
        Difficulty.ADVANCED: 2,
        Difficulty.EXPERT: 3,
    }

    if order[requested] <= order[maximum]:
        return requested

    return maximum
