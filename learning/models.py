from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from uuid import uuid4


class Difficulty(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class LessonState(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    NEEDS_REVISION = "needs_revision"


class QuestionType(str, Enum):
    RECALL = "recall"
    UNDERSTANDING = "understanding"
    APPLICATION = "application"
    PRACTICE = "practice"


@dataclass(frozen=True)
class LearningGoal:
    subject: str
    goal: str
    target_level: Difficulty


@dataclass(frozen=True)
class Topic:
    name: str
    description: str
    prerequisites: tuple[str, ...] = ()
    difficulty: Difficulty = Difficulty.BEGINNER


@dataclass
class Lesson:
    topic: Topic
    state: LessonState = LessonState.NOT_STARTED
    explanation_attempts: int = 0
    practice_attempts: int = 0
    correct_answers: int = 0
    total_answers: int = 0
    needs_revision: bool = False


@dataclass(frozen=True)
class TutorQuestion:
    question: str
    question_type: QuestionType
    topic: str


@dataclass(frozen=True)
class TutorFeedback:
    correct: bool
    explanation: str
    correction: str = ""
    next_action: str = "continue"


@dataclass
class LearningProfile:
    preferred_explanation_style: str = "simple-first"
    preferred_pace: str = "adaptive"
    preferred_language: str = "english"
    current_level_by_subject: dict[str, Difficulty] = field(
        default_factory=dict
    )
    strong_areas: dict[str, float] = field(default_factory=dict)
    weak_areas: dict[str, float] = field(default_factory=dict)
    difficult_concepts: set[str] = field(default_factory=set)
    common_mistakes: dict[str, list[str]] = field(default_factory=dict)
    revision_topics: set[str] = field(default_factory=set)
    completed_topics: set[str] = field(default_factory=set)
    progress_by_topic: dict[str, float] = field(default_factory=dict)


@dataclass
class LearningSession:
    session_id: str = field(default_factory=lambda: str(uuid4()))
    subject: Optional[str] = None
    goal: Optional[str] = None
    current_topic: Optional[str] = None
    current_lesson_state: LessonState = LessonState.NOT_STARTED
    concept_explanation: Optional[str] = None
    example: Optional[str] = None
    analogy: Optional[str] = None
    practical_application: Optional[str] = None
    current_question: Optional[TutorQuestion] = None
