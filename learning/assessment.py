from learning.models import Difficulty, LearningProfile


def normalize_level(value: str | None) -> Difficulty:
    if not value:
        return Difficulty.BEGINNER

    normalized = value.strip().lower()

    mapping = {
        "beginner": Difficulty.BEGINNER,
        "basic": Difficulty.BEGINNER,
        "intermediate": Difficulty.INTERMEDIATE,
        "advanced": Difficulty.ADVANCED,
        "expert": Difficulty.EXPERT,
    }

    return mapping.get(
        normalized,
        Difficulty.BEGINNER,
    )


class LevelAssessor:

    def assess(
        self,
        subject: str,
        profile: LearningProfile,
    ) -> Difficulty:

        return profile.current_level_by_subject.get(
            subject,
            Difficulty.BEGINNER,
        )

    def set_level(
        self,
        subject: str,
        level: Difficulty,
        profile: LearningProfile,
    ) -> LearningProfile:

        profile.current_level_by_subject[subject] = level

        return profile
