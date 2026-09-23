from learning.assessment import LevelAssessor
from learning.curriculum import CurriculumBuilder, LearningRoadmap
from learning.explanation import ExplanationPlanner
from learning.feedback import FeedbackEngine
from learning.gaps import KnowledgeGapDetector
from learning.lesson import LessonEngine
from learning.models import (
    Difficulty,
    LearningGoal,
    LearningProfile,
    LearningSession,
    Lesson,
    Topic,
)
from learning.progress import ProgressTracker
from learning.questions import QuestionEngine


class TutorEngine:

    def __init__(
        self,
        profile: LearningProfile | None = None,
    ):
        self.profile = profile or LearningProfile()
        self.assessor = LevelAssessor()
        self.curriculum = CurriculumBuilder()
        self.lesson_engine = LessonEngine()
        self.questions = QuestionEngine()
        self.feedback = FeedbackEngine()
        self.gaps = KnowledgeGapDetector()
        self.progress = ProgressTracker()
        self.explanations = ExplanationPlanner()

    def assess_level(
        self,
        subject: str,
    ) -> Difficulty:

        return self.assessor.assess(
            subject,
            self.profile,
        )

    def create_roadmap(
        self,
        subject: str,
        goal: str,
        level: Difficulty | None = None,
    ) -> LearningRoadmap:

        chosen_level = (
            level
            or self.assess_level(subject)
        )

        return self.curriculum.build(
            subject=subject,
            goal=goal,
            level=chosen_level,
        )

    def start_lesson(
        self,
        session: LearningSession,
        topic: Topic,
    ) -> Lesson:

        lesson = self.lesson_engine.start(
            topic
        )

        session.subject = session.subject or topic.name
        session.current_topic = topic.name
        session.current_lesson_state = lesson.state

        return lesson

    def create_question(
        self,
        lesson: Lesson,
    ):

        question = self.questions.next_question(
            lesson
        )

        return question

    def evaluate_answer(
        self,
        lesson: Lesson,
        correct: bool,
        explanation: str = "",
        correction: str = "",
    ):

        feedback = self.feedback.evaluate(
            lesson=lesson,
            correct=correct,
            explanation=explanation,
            correction=correction,
        )

        self.progress.update(
            lesson,
            self.profile,
        )

        return feedback

    def detect_gaps(
        self,
        lessons: list[Lesson],
    ):

        return self.gaps.detect(
            lessons,
            self.profile,
        )

    def complete_lesson(
        self,
        lesson: Lesson,
    ) -> Lesson:

        completed = self.lesson_engine.complete(
            lesson
        )

        self.progress.update(
            completed,
            self.profile,
        )

        return completed

    def mark_for_revision(
        self,
        lesson: Lesson,
    ) -> Lesson:

        revised = self.lesson_engine.mark_revision(
            lesson
        )

        self.progress.update(
            revised,
            self.profile,
        )

        return revised

    def explanation_plan(
        self,
        topic: Topic,
    ):

        return self.explanations.build(
            topic,
            self.profile,
        )
