from learning.models import (
    Lesson,
    TutorFeedback,
)


class FeedbackEngine:

    def evaluate(
        self,
        lesson: Lesson,
        correct: bool,
        explanation: str = "",
        correction: str = "",
    ) -> TutorFeedback:

        lesson.total_answers += 1
        lesson.practice_attempts += 1

        if correct:
            lesson.correct_answers += 1

            return TutorFeedback(
                correct=True,
                explanation=(
                    explanation
                    or "Good. Your answer is correct."
                ),
                correction="",
                next_action="continue",
            )

        lesson.needs_revision = True

        return TutorFeedback(
            correct=False,
            explanation=(
                explanation
                or "Let's look at this from another angle."
            ),
            correction=correction,
            next_action="practice_again",
        )
