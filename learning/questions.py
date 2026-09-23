from learning.models import (
    Lesson,
    QuestionType,
    Topic,
    TutorQuestion,
)


class QuestionEngine:

    def create_recall(
        self,
        topic: Topic,
    ) -> TutorQuestion:

        return TutorQuestion(
            question=(
                f"What is one important idea from {topic.name}?"
            ),
            question_type=QuestionType.RECALL,
            topic=topic.name,
        )

    def create_understanding(
        self,
        topic: Topic,
    ) -> TutorQuestion:

        return TutorQuestion(
            question=(
                f"Explain {topic.name} in your own words."
            ),
            question_type=QuestionType.UNDERSTANDING,
            topic=topic.name,
        )

    def create_application(
        self,
        topic: Topic,
    ) -> TutorQuestion:

        return TutorQuestion(
            question=(
                f"How would you apply {topic.name} "
                f"in a practical situation?"
            ),
            question_type=QuestionType.APPLICATION,
            topic=topic.name,
        )

    def create_practice(
        self,
        topic: Topic,
    ) -> TutorQuestion:

        return TutorQuestion(
            question=(
                f"Try this practice task about {topic.name}."
            ),
            question_type=QuestionType.PRACTICE,
            topic=topic.name,
        )

    def next_question(
        self,
        lesson: Lesson,
    ) -> TutorQuestion:

        if lesson.total_answers == 0:
            return self.create_recall(
                lesson.topic
            )

        if lesson.correct_answers == 0:
            return self.create_understanding(
                lesson.topic
            )

        if lesson.correct_answers < 2:
            return self.create_application(
                lesson.topic
            )

        return self.create_practice(
            lesson.topic
        )
