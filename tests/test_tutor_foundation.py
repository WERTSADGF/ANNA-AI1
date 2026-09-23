import unittest

from learning.assessment import LevelAssessor
from learning.curriculum import CurriculumBuilder
from learning.explanation import (
    ExplanationPlanner,
    alternative_explanation_number,
)
from learning.feedback import FeedbackEngine
from learning.gaps import KnowledgeGapDetector
from learning.lesson import LessonEngine
from learning.models import (
    Difficulty,
    LearningProfile,
    LearningSession,
    LessonState,
    QuestionType,
    Topic,
)
from learning.progress import ProgressTracker
from learning.questions import QuestionEngine
from learning.tutor import TutorEngine


class TestTutorFoundation(unittest.TestCase):

    def test_default_level_is_beginner(self):
        assessor = LevelAssessor()
        profile = LearningProfile()

        level = assessor.assess(
            "Python",
            profile,
        )

        self.assertEqual(
            level,
            Difficulty.BEGINNER,
        )

    def test_set_level(self):
        assessor = LevelAssessor()
        profile = LearningProfile()

        assessor.set_level(
            "Python",
            Difficulty.INTERMEDIATE,
            profile,
        )

        self.assertEqual(
            profile.current_level_by_subject["Python"],
            Difficulty.INTERMEDIATE,
        )

    def test_curriculum(self):
        builder = CurriculumBuilder()

        roadmap = builder.build(
            subject="Python",
            goal="Learn Python fundamentals",
            level=Difficulty.BEGINNER,
        )

        self.assertEqual(
            roadmap.goal.subject,
            "Python",
        )

        self.assertGreaterEqual(
            len(roadmap.topics),
            3,
        )

        self.assertTrue(
            roadmap.topics[1].prerequisites
        )

    def test_lesson_start(self):
        engine = LessonEngine()

        topic = Topic(
            name="Python variables",
            description="Variables store values.",
        )

        lesson = engine.start(topic)

        self.assertEqual(
            lesson.state,
            LessonState.IN_PROGRESS,
        )

    def test_question_cycle(self):
        questions = QuestionEngine()

        topic = Topic(
            name="Python variables",
            description="Variables store values.",
        )

        lesson = LessonEngine().start(topic)

        first = questions.next_question(
            lesson
        )

        self.assertEqual(
            first.question_type,
            QuestionType.RECALL,
        )

        lesson.total_answers = 1
        lesson.correct_answers = 0

        second = questions.next_question(
            lesson
        )

        self.assertEqual(
            second.question_type,
            QuestionType.UNDERSTANDING,
        )

    def test_correct_answer(self):
        lesson = LessonEngine().start(
            Topic(
                name="Python",
                description="Programming.",
            )
        )

        feedback = FeedbackEngine().evaluate(
            lesson=lesson,
            correct=True,
        )

        self.assertTrue(
            feedback.correct
        )

        self.assertEqual(
            lesson.total_answers,
            1,
        )

        self.assertEqual(
            lesson.correct_answers,
            1,
        )

    def test_wrong_answer_creates_revision_need(self):
        lesson = LessonEngine().start(
            Topic(
                name="Python",
                description="Programming.",
            )
        )

        feedback = FeedbackEngine().evaluate(
            lesson=lesson,
            correct=False,
            explanation="Let's try a different example.",
            correction="Review variables.",
        )

        self.assertFalse(
            feedback.correct
        )

        self.assertTrue(
            lesson.needs_revision
        )

        self.assertEqual(
            feedback.next_action,
            "practice_again",
        )

    def test_progress_tracking(self):
        lesson = LessonEngine().start(
            Topic(
                name="Python",
                description="Programming.",
            )
        )

        lesson.total_answers = 5
        lesson.correct_answers = 5

        profile = LearningProfile()

        ProgressTracker().update(
            lesson,
            profile,
        )

        self.assertEqual(
            profile.progress_by_topic["Python"],
            1.0,
        )

        self.assertIn(
            "Python",
            profile.strong_areas,
        )

    def test_gap_detection(self):
        lesson = LessonEngine().start(
            Topic(
                name="Python functions",
                description="Functions.",
            )
        )

        lesson.total_answers = 4
        lesson.correct_answers = 1
        lesson.needs_revision = True

        profile = LearningProfile()

        gaps = KnowledgeGapDetector().detect(
            [lesson],
            profile,
        )

        self.assertIn(
            "Python functions",
            gaps,
        )

        self.assertIn(
            "Python functions",
            profile.revision_topics,
        )

    def test_explanation_plan(self):
        topic = Topic(
            name="Python variables",
            description="Variables.",
            difficulty=Difficulty.BEGINNER,
        )

        profile = LearningProfile()

        plan = ExplanationPlanner().build(
            topic,
            profile,
        )

        self.assertTrue(
            plan.use_simple_language
        )

        self.assertTrue(
            plan.include_example
        )

        self.assertTrue(
            plan.include_analogy
        )

        self.assertTrue(
            plan.include_practical_application
        )

        self.assertFalse(
            plan.include_technical_detail
        )

    def test_alternative_explanations(self):
        self.assertEqual(
            alternative_explanation_number(1),
            1,
        )

        self.assertEqual(
            alternative_explanation_number(2),
            2,
        )

        self.assertEqual(
            alternative_explanation_number(3),
            3,
        )

        self.assertEqual(
            alternative_explanation_number(5),
            4,
        )

    def test_tutor_engine(self):
        tutor = TutorEngine()

        roadmap = tutor.create_roadmap(
            subject="Python",
            goal="Learn Python",
        )

        self.assertGreater(
            len(roadmap.topics),
            0,
        )

        session = LearningSession()

        lesson = tutor.start_lesson(
            session,
            roadmap.topics[0],
        )

        question = tutor.create_question(
            lesson
        )

        self.assertEqual(
            question.question_type,
            QuestionType.RECALL,
        )

        feedback = tutor.evaluate_answer(
            lesson=lesson,
            correct=False,
            correction="Try another example.",
        )

        self.assertFalse(
            feedback.correct
        )

        tutor.mark_for_revision(
            lesson
        )

        gaps = tutor.detect_gaps(
            [lesson]
        )

        self.assertIn(
            lesson.topic.name,
            gaps,
        )

    def test_completion(self):
        tutor = TutorEngine()

        topic = Topic(
            name="Python basics",
            description="Basics.",
        )

        lesson = LessonEngine().start(
            topic
        )

        lesson.total_answers = 5
        lesson.correct_answers = 5

        completed = tutor.complete_lesson(
            lesson
        )

        self.assertEqual(
            completed.state,
            LessonState.COMPLETED,
        )

        self.assertIn(
            "Python basics",
            tutor.profile.completed_topics,
        )


if __name__ == "__main__":
    unittest.main()
