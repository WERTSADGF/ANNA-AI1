import unittest

from chat.models import ChatMessage, ChatResponse
from chat.service import ChatService
from learning.models import Difficulty, LessonState, QuestionType
from learning.tutor import TutorEngine


class RecordingProvider:
    def __init__(self):
        self.requests = []

    def generate(self, request):
        self.requests.append(request)
        return ChatResponse(
            message=ChatMessage(
                role="assistant",
                content="ANNA tutor lesson response",
            ),
            provider="recording",
            model="test-model",
        )


class TestChatTutorIntegration(unittest.TestCase):

    def test_default_chat_service_has_tutor(self):
        service = ChatService(
            provider=RecordingProvider()
        )

        self.assertIsInstance(
            service.tutor,
            TutorEngine,
        )

    def test_start_tutor_creates_roadmap_and_session(self):
        service = ChatService(
            provider=RecordingProvider()
        )

        roadmap = service.start_tutor(
            subject="Python",
            goal="Learn Python fundamentals",
        )

        self.assertEqual(
            roadmap.goal.subject,
            "Python",
        )

        self.assertEqual(
            service.learning_session.subject,
            "Python",
        )

        self.assertGreaterEqual(
            len(roadmap.topics),
            3,
        )

    def test_tutor_lesson_question_and_feedback_cycle(self):
        service = ChatService(
            provider=RecordingProvider()
        )

        roadmap = service.start_tutor(
            subject="Python",
            goal="Learn Python",
        )

        lesson = service.start_tutor_lesson()

        self.assertEqual(
            lesson.state,
            LessonState.IN_PROGRESS,
        )

        question = service.next_tutor_question(
            lesson
        )

        self.assertEqual(
            question.question_type,
            QuestionType.RECALL,
        )

        feedback = service.evaluate_tutor_answer(
            correct=False,
            correction="Review the concept and try again.",
            lesson=lesson,
        )

        self.assertFalse(
            feedback.correct
        )

        self.assertTrue(
            lesson.needs_revision
        )

        gaps = service.detect_tutor_gaps()

        self.assertIn(
            roadmap.topics[0].name,
            gaps,
        )

    def test_teaching_uses_tutor_context(self):
        provider = RecordingProvider()

        service = ChatService(
            provider=provider
        )

        service.start_tutor(
            subject="Python",
            goal="Learn Python",
            level=Difficulty.BEGINNER,
        )

        lesson = service.start_tutor_lesson()

        response = service.teach_tutor_lesson(
            lesson
        )

        self.assertEqual(
            response.message.content,
            "ANNA tutor lesson response",
        )

        self.assertEqual(
            len(provider.requests),
            1,
        )

        messages = provider.requests[0].messages

        self.assertEqual(
            messages[0].role,
            "system",
        )

        self.assertIn(
            "ANNA tutor context:",
            messages[0].content,
        )

        self.assertIn(
            lesson.topic.name,
            messages[0].content,
        )

        self.assertEqual(
            messages[-1].role,
            "user",
        )


if __name__ == "__main__":
    unittest.main()
