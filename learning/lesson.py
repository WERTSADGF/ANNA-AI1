from learning.models import (
    Difficulty,
    Lesson,
    LessonState,
    Topic,
)


class LessonEngine:

    def start(self, topic: Topic) -> Lesson:
        return Lesson(
            topic=topic,
            state=LessonState.IN_PROGRESS,
        )

    def explain(
        self,
        lesson: Lesson,
        explanation: str,
    ) -> Lesson:

        lesson.explanation_attempts += 1
        lesson.state = LessonState.IN_PROGRESS

        return lesson

    def mark_revision(
        self,
        lesson: Lesson,
    ) -> Lesson:

        lesson.needs_revision = True
        lesson.state = LessonState.NEEDS_REVISION

        return lesson

    def complete(
        self,
        lesson: Lesson,
    ) -> Lesson:

        lesson.state = LessonState.COMPLETED
        lesson.needs_revision = False

        return lesson

    def next_difficulty(
        self,
        lesson: Lesson,
    ) -> Difficulty:

        if lesson.total_answers == 0:
            return lesson.topic.difficulty

        accuracy = (
            lesson.correct_answers
            / lesson.total_answers
        )

        if accuracy >= 0.90:
            if lesson.topic.difficulty == Difficulty.BEGINNER:
                return Difficulty.INTERMEDIATE

            if lesson.topic.difficulty == Difficulty.INTERMEDIATE:
                return Difficulty.ADVANCED

            if lesson.topic.difficulty == Difficulty.ADVANCED:
                return Difficulty.EXPERT

        if accuracy < 0.50:
            return Difficulty.BEGINNER

        return lesson.topic.difficulty
