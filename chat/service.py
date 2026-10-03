from assistant.models import Project, Reminder, Task, TaskStatus
from assistant.service import AssistantService
from agent.models import AgentPlan, AgentRun
from agent.service import AgentService
from chat.models import ChatMessage, ChatRequest, ChatResponse
from chat.providers import ChatModelProvider
from chat.session import ChatSession
from companion.engine import CompanionEngine
from core.model_router import ModelRouter
from files.service import FileService
from language.context import build_language_context
from language.models import (
    LanguagePreference,
    LanguageSignal,
    LanguageSource,
)
from learning.curriculum import LearningRoadmap
from learning.models import (
    Difficulty,
    LearningProfile,
    LearningSession,
    Lesson,
    Topic,
    TutorFeedback,
    TutorQuestion,
)
from learning.tutor import TutorEngine
from memory.manager import MemoryManager
from research.engine import ResearchEngine
from research.models import ResearchMode
from voice.models import SpeechInput, SpeechOutput, VoiceLanguage
from voice.service import VoiceService
from tools.service import ToolService


class ChatService:

    def __init__(
        self,
        provider: ChatModelProvider | None = None,
        companion: CompanionEngine | None = None,
        session: ChatSession | None = None,
        router: ModelRouter | None = None,
        memory: MemoryManager | None = None,
        language_preference: LanguagePreference | None = None,
        files: FileService | None = None,
        research: ResearchEngine | None = None,
        voice: VoiceService | None = None,
        tutor: TutorEngine | None = None,
        assistant: AssistantService | None = None,

        tool_service: ToolService | None = None,
        agent: AgentService | None = None,
    ):
        self.router = router or ModelRouter()
        self.provider = provider or self.router.get_chat_provider()
        self.companion = companion or CompanionEngine()
        self.session = session or ChatSession()
        self.memory = memory
        self.language_preference = language_preference
        self.files = files
        self.research_engine = research
        self.voice = voice

        self.assistant = assistant or AssistantService()
        self.tool_service = tool_service or ToolService()
        self.agent = agent or AgentService(self.tool_service)
        self.tutor = tutor or TutorEngine()
        self.learning_session = LearningSession()
        self.learning_roadmap: LearningRoadmap | None = None
        self.learning_lessons: list[Lesson] = []

        self._previous_language: LanguageSignal | None = None

    def ingest_file(self, path: str):
        if self.files is None:
            raise RuntimeError("File service is not configured.")

        return self.files.ingest(path)

    def process_voice_input(
        self,
        audio: bytes,
        language: VoiceLanguage,
    ) -> tuple[SpeechInput, ChatResponse, SpeechOutput]:

        if self.voice is None:
            raise RuntimeError("Voice service is not configured.")

        speech_input = self.voice.process_audio(
            audio=audio,
            language=language,
        )

        response = self.respond(
            speech_input.text
        )

        speech_output = self.voice.speak(
            text=response.message.content,
            language=language,
        )

        return speech_input, response, speech_output

    def tool_system_info(self):
        return self.tool_service.system_info()

    def tool_inspect_python(self, path: str):
        return self.tool_service.inspect_python(path)

    def tool_run_tests(self, dry_run: bool = True):
        return self.tool_service.run_tests(
            dry_run=dry_run
        )

    def tool_list_directory(self, path: str = "."):
        return self.tool_service.list_directory(path)

    def tool_create_directory(
        self,
        path: str,
        dry_run: bool = True,
    ):
        return self.tool_service.create_directory(
            path=path,
            dry_run=dry_run,
        )

    def tool_launch_application(
        self,
        name: str,
        dry_run: bool = True,
        confirmed: bool = False,
    ):
        return self.tool_service.launch_application(
            name=name,
            dry_run=dry_run,
            confirmed=confirmed,
        )
    def agent_plan(
        self,
        goal: str,
        max_steps: int = 8,
    ) -> AgentPlan:
        return self.agent.plan(
            goal=goal,
            max_steps=max_steps,
        )

    def agent_run(
        self,
        goal: str,
        max_steps: int = 8,
        confirmed: bool = False,
        dry_run: bool = False,
    ) -> AgentRun:
        return self.agent.run(
            goal=goal,
            max_steps=max_steps,
            confirmed=confirmed,
            dry_run=dry_run,
        )

    def create_assistant_task(
        self,
        title: str,
        description: str = "",
        project_id: str | None = None,
        due_at=None,
    ) -> Task:

        return self.assistant.create_task(
            title=title,
            description=description,
            project_id=project_id,
            due_at=due_at,
        )

    def set_assistant_task_status(
        self,
        task_id: str,
        status: TaskStatus,
    ) -> Task:

        return self.assistant.set_task_status(
            task_id=task_id,
            status=status,
        )

    def create_assistant_reminder(
        self,
        title: str,
        due_at,
    ) -> Reminder:

        return self.assistant.create_reminder(
            title=title,
            due_at=due_at,
        )

    def complete_assistant_reminder(
        self,
        reminder_id: str,
    ) -> Reminder:

        return self.assistant.complete_reminder(
            reminder_id=reminder_id,
        )

    def create_assistant_project(
        self,
        name: str,
        description: str = "",
    ) -> Project:

        return self.assistant.create_project(
            name=name,
            description=description,
        )

    def delete_assistant_project(
        self,
        project_id: str,
        confirmed: bool = False,
    ) -> None:

        self.assistant.delete_project(
            project_id=project_id,
            confirmed=confirmed,
        )

    def assistant_tasks(
        self,
    ) -> tuple[Task, ...]:

        return self.assistant.list_tasks()

    def assistant_reminders(
        self,
    ) -> tuple[Reminder, ...]:

        return self.assistant.list_reminders()

    def assistant_projects(
        self,
    ) -> tuple[Project, ...]:

        return self.assistant.list_projects()

    def assistant_due_reminders(
        self,
        now=None,
    ) -> tuple[Reminder, ...]:

        return self.assistant.due_reminders(
            now=now
        )
    def start_tutor(
        self,
        subject: str,
        goal: str,
        level: Difficulty | None = None,
    ) -> LearningRoadmap:

        roadmap = self.tutor.create_roadmap(
            subject=subject,
            goal=goal,
            level=level,
        )

        self.learning_roadmap = roadmap
        self.learning_session = LearningSession(
            subject=subject.strip(),
            goal=goal.strip(),
        )
        self.learning_lessons = []

        return roadmap

    def start_tutor_lesson(
        self,
        topic_index: int = 0,
    ) -> Lesson:

        if self.learning_roadmap is None:
            raise RuntimeError(
                "Start a tutor session before starting a lesson."
            )

        if (
            topic_index < 0
            or topic_index >= len(self.learning_roadmap.topics)
        ):
            raise IndexError(
                "Tutor topic index is out of range."
            )

        topic = self.learning_roadmap.topics[topic_index]

        lesson = self.tutor.start_lesson(
            self.learning_session,
            topic,
        )

        self.learning_lessons.append(lesson)

        return lesson

    def teach_tutor_lesson(
        self,
        lesson: Lesson | None = None,
    ) -> ChatResponse:

        target = lesson

        if target is None:
            if not self.learning_lessons:
                raise RuntimeError(
                    "Start a tutor lesson before teaching it."
                )
            target = self.learning_lessons[-1]

        plan = self.tutor.explanation_plan(
            target.topic
        )

        language_context = build_language_context(
            user_text=(
                f"Teach me {target.topic.name} "
                "as my personal tutor."
            ),
            preference=self.language_preference,
            previous_language=self._previous_language,
        )

        decision = language_context.decision

        tutor_message = ChatMessage(
            role="system",
            content=(
                "ANNA tutor context: "
                f"subject={target.topic.name}; "
                f"difficulty={plan.level.value}; "
                f"simple_language={plan.use_simple_language}; "
                f"example={plan.include_example}; "
                f"analogy={plan.include_analogy}; "
                f"practical_application="
                f"{plan.include_practical_application}; "
                f"technical_detail={plan.include_technical_detail}; "
                f"response_language="
                f"{decision.response_language.value}; "
                f"teaching_style=simple-first"
            ),
        )

        user_message = ChatMessage(
            role="user",
            content=(
                f"Teach me {target.topic.name}. "
                "Explain the concept, give an example, "
                "use an analogy, and show a practical application."
            ),
        )

        request = ChatRequest(
            messages=(
                (tutor_message,)
                + (user_message,)
            ),
        )

        response = self.provider.generate(
            request
        )

        self.tutor.lesson_engine.explain(
            target,
            response.message.content,
        )

        return response

    def next_tutor_question(
        self,
        lesson: Lesson | None = None,
    ) -> TutorQuestion:

        target = lesson

        if target is None:
            if not self.learning_lessons:
                raise RuntimeError(
                    "Start a tutor lesson before requesting a question."
                )
            target = self.learning_lessons[-1]

        question = self.tutor.create_question(
            target
        )

        self.learning_session.current_question = question

        return question

    def evaluate_tutor_answer(
        self,
        correct: bool,
        explanation: str = "",
        correction: str = "",
        lesson: Lesson | None = None,
    ) -> TutorFeedback:

        target = lesson

        if target is None:
            if not self.learning_lessons:
                raise RuntimeError(
                    "Start a tutor lesson before evaluating an answer."
                )
            target = self.learning_lessons[-1]

        feedback = self.tutor.evaluate_answer(
            lesson=target,
            correct=correct,
            explanation=explanation,
            correction=correction,
        )

        self.learning_session.current_lesson_state = target.state

        return feedback

    def complete_tutor_lesson(
        self,
        lesson: Lesson | None = None,
    ) -> Lesson:

        target = lesson

        if target is None:
            if not self.learning_lessons:
                raise RuntimeError(
                    "Start a tutor lesson before completing it."
                )
            target = self.learning_lessons[-1]

        completed = self.tutor.complete_lesson(
            target
        )

        self.learning_session.current_lesson_state = (
            completed.state
        )

        return completed

    def mark_tutor_for_revision(
        self,
        lesson: Lesson | None = None,
    ) -> Lesson:

        target = lesson

        if target is None:
            if not self.learning_lessons:
                raise RuntimeError(
                    "Start a tutor lesson before marking revision."
                )
            target = self.learning_lessons[-1]

        revised = self.tutor.mark_for_revision(
            target
        )

        self.learning_session.current_lesson_state = (
            revised.state
        )

        return revised

    def detect_tutor_gaps(self) -> list[str]:

        return self.tutor.detect_gaps(
            self.learning_lessons
        )

    def tutor_profile(self) -> LearningProfile:

        return self.tutor.profile

    def research(
        self,
        question: str,
        mode: ResearchMode = ResearchMode.NORMAL,
    ) -> ChatResponse:

        cleaned_question = question.strip()

        if not cleaned_question:
            raise ValueError("Research question cannot be empty.")

        if self.research_engine is None:
            raise RuntimeError("Research engine is not configured.")

        language_context = build_language_context(
            user_text=cleaned_question,
            preference=self.language_preference,
            previous_language=self._previous_language,
        )

        companion_context = self.companion.build_context(
            cleaned_question
        )

        guidance = companion_context.guidance
        decision = language_context.decision

        plan, sources = self.research_engine.collect_sources(
            cleaned_question,
            mode=mode,
        )

        source_messages = tuple(
            ChatMessage(
                role="system",
                content=(
                    "ANNA research source: "
                    f"title={source.title}; "
                    f"url={source.url}; "
                    f"accessed={source.accessed}"
                ),
            )
            for source in sources
        )

        research_message = ChatMessage(
            role="system",
            content=(
                "ANNA research context: "
                f"mode={plan.objective.mode.value}; "
                f"subquestions={len(plan.subquestions)}; "
                "Sources listed below are collection results. "
                "Do not claim a source was verified or inspected "
                "unless a successful source read actually occurred."
            ),
        )

        language_message = ChatMessage(
            role="system",
            content=(
                f"ANNA language guidance: "
                f"response_language={decision.response_language.value}; "
                f"language_source={decision.source.value}; "
                f"mixed_response={decision.mixed_response}; "
                f"tone={guidance.tone}; "
                f"style={guidance.style}"
            ),
        )

        user_message = ChatMessage(
            role="user",
            content=cleaned_question,
        )

        request = ChatRequest(
            messages=(
                (research_message,)
                + (language_message,)
                + source_messages
                + (user_message,)
            ),
        )

        response = self.provider.generate(request)

        self.session.add_message(user_message)
        self.session.add_message(response.message)

        self._previous_language = LanguageSignal(
            language=decision.response_language,
            confidence=1.0,
            mixed=decision.mixed_response,
            source=LanguageSource.CONTEXT,
        )

        return response

    def respond(
        self,
        user_text: str,
        previous_messages: tuple[ChatMessage, ...] = (),
    ) -> ChatResponse:

        cleaned_text = user_text.strip()

        if not cleaned_text:
            raise ValueError("User message cannot be empty.")

        language_context = build_language_context(
            user_text=cleaned_text,
            preference=self.language_preference,
            previous_language=self._previous_language,
        )

        companion_context = self.companion.build_context(
            cleaned_text
        )

        conversation = (
            previous_messages
            if previous_messages
            else self.session.history()
        )

        guidance = companion_context.guidance
        decision = language_context.decision

        companion_message = ChatMessage(
            role="system",
            content=(
                f"ANNA companion guidance: "
                f"identity={companion_context.profile.name} "
                f"({companion_context.profile.identity}); "
                f"response_language={decision.response_language.value}; "
                f"language_source={decision.source.value}; "
                f"mixed_response={decision.mixed_response}; "
                f"tone={guidance.tone}; "
                f"style={guidance.style}; "
                f"ai_identity_transparency="
                f"{guidance.disclose_ai_identity_when_relevant}"
            ),
        )

        memory_messages: tuple[ChatMessage, ...] = ()

        if self.memory is not None:
            memories = self.memory.retrieve(
                query=cleaned_text,
                allow_sensitive=False,
                limit=5,
            )

            memory_messages = tuple(
                ChatMessage(
                    role="system",
                    content=(
                        "ANNA memory context: "
                        f"type={getattr(memory.memory_type, 'value', memory.memory_type)}; "
                        f"confidence={memory.confidence}; "
                        f"importance={memory.importance}; "
                        f"content={memory.content}"
                    ),
                )
                for memory in memories
            )

        file_messages: tuple[ChatMessage, ...] = ()

        if self.files is not None:
            file_results = self.files.search(
                query=cleaned_text,
                limit=5,
            )

            file_messages = tuple(
                ChatMessage(
                    role="system",
                    content=(
                        "ANNA file context: "
                        f"file={result.chunk.file_path}; "
                        f"lines={result.chunk.start_line}-{result.chunk.end_line}; "
                        f"score={result.score}; "
                        f"content={result.chunk.content}"
                    ),
                )
                for result in file_results
            )

        user_message = ChatMessage(
            role="user",
            content=cleaned_text,
        )

        request = ChatRequest(
            messages=(
                (companion_message,)
                + memory_messages
                + file_messages
                + conversation
                + (user_message,)
            ),
        )

        response = self.provider.generate(request)

        self.session.add_message(user_message)
        self.session.add_message(response.message)

        self._previous_language = LanguageSignal(
            language=decision.response_language,
            confidence=1.0,
            mixed=decision.mixed_response,
            source=LanguageSource.CONTEXT,
        )

        return response
